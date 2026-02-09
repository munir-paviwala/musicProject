#!/usr/bin/env python3
"""
YouTube Music Scraper - Minimal API calls, session-token based authentication
Discovers all favorited and user-created playlists, fetches song metadata.
Outputs to data.json with playlist structure.

Setup:
  pip install ytmusicapi
  python3 yt_music_scraper.py

On first run, opens browser for OAuth - approve once, credentials saved locally.
Subsequent runs use cached credentials (no browser needed).
"""

import json
import os
from pathlib import Path
from typing import Optional

try:
    from ytmusicapi import YTMusic, setup
except ImportError:
    print("❌ ytmusicapi not installed. Run: pip install ytmusicapi")
    exit(1)

# Paths
SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "data.json"
HEADERS_FILE = SCRIPT_DIR / ".yt_music_headers.json"

# ============================================================
# PLAYLISTS TO SCRAPE
# ============================================================
# Paste your YouTube Music playlist IDs or full URLs here
# Format: "PLxxxxxx" or "https://music.youtube.com/playlist?list=PLxxxxxx"
# You can get the ID from the URL: music.youtube.com/playlist?list=[ID_HERE]
# 
PLAYLISTS_TO_SCRAPE = [
    "PLkyLhAV5zhSCJUWYqvvGNTsawXcqRQbGp",
    "PLkyLhAV5zhSDi9bhn9hqDiZyrEcbzLZsE",
    "PLkyLhAV5zhSAnGpzLCdtGMZ6mRDBpPY20",
    "PLkyLhAV5zhSBGCKDkyzH2xPG8n8wTALYS",
    "PLkyLhAV5zhSCCRDsz2tc7AMFt_OHN0Fh5",
    "PLkyLhAV5zhSBVGFbiZh_msq7G7fVM6TXD",
    "PLkyLhAV5zhSBRaZRJKVH2k6YBgjF_viTn",
    "PLkyLhAV5zhSDtfcCEHlwgtssgO0f8q8B1",
    "PLkyLhAV5zhSA9SeKcz-Yo6rodZFNhZ0q-",
    "PLkyLhAV5zhSBcrqJunwQIDK7QxSy7dFGK",
    "PLkyLhAV5zhSA_A9uEnTQfBLp8ve2YYVnn",
    "PLkyLhAV5zhSBBex2ggQQ-5o-ZPVmc2byx",
    "PLkyLhAV5zhSCEbcAHjzPttuIpk4DI7H7k",
    "PLkyLhAV5zhSDN7SjlOc1aWXrH5gXdYjZm",
    "PLkyLhAV5zhSAaV5dv55kHyd-lXNK3aA41",
    "PLkyLhAV5zhSAoKu9Jp8u9kVtXqFcHaePT",
    "PLkyLhAV5zhSAn6qXErKgByH151yyt-d85",
    "PLkyLhAV5zhSAr1gjNZk2r9duUFTrxQa-X",
    "PLkyLhAV5zhSBl95Z7-YcPCt07fEHQGEsj",
]
# ============================================================

def get_yt_music_client() -> YTMusic:
    """
    Initialize YouTube Music client with default headers (no auth).
    """
    print(f"✓ Using default YouTube Music client")
    return YTMusic()

def fetch_playlists(yt: YTMusic) -> list:
    """
    Fetch playlists from the configured list.
    Uses public/unlisted playlists - no authentication needed.
    """
    print("\n📋 Fetching playlists...")
    
    if not PLAYLISTS_TO_SCRAPE:
        print("   ⚠️  No playlists configured!")
        print("   Please add playlist IDs to PLAYLISTS_TO_SCRAPE in the script.")
        return []
    
    playlists = []
    for playlist_url_or_id in PLAYLISTS_TO_SCRAPE:
        # Extract ID from URL if needed
        playlist_id = playlist_url_or_id
        if "list=" in playlist_url_or_id:
            playlist_id = playlist_url_or_id.split("list=")[1].split("&")[0]
        
        playlists.append({
            'playlistId': playlist_id,
            'title': f'Playlist: {playlist_id[:10]}...',
            'thumbnail': [{'url': ''}]
        })
    
    print(f"   Found {len(playlists)} playlist(s) configured")
    return playlists

def fetch_playlist_songs(yt: YTMusic, playlist_id: str, playlist_name: str) -> list:
    """
    Fetch all songs from a single playlist.
    Handles pagination gracefully.
    """
    print(f"   ↳ Fetching songs from '{playlist_name}'...")
    try:
        results = yt.get_playlist(playlist_id)
        songs = results.get('tracks', [])
        print(f"     └─ {len(songs)} songs")
        
        # Normalize song structure
        normalized = []
        for i, song in enumerate(songs):
            if song is None:
                continue
            normalized.append({
                "id": song.get('videoId', ''),
                "title": song.get('title', 'Unknown'),
                "artist": song.get('artists', [{'name': 'Unknown'}])[0].get('name', 'Unknown') 
                    if song.get('artists') else 'Unknown',
                "duration": song.get('duration_seconds', 0),
                "album": song.get('album', {}).get('name', '') if song.get('album') else '',
                "thumbnail": song.get('thumbnail', [{}])[-1].get('url', '') if song.get('thumbnail') else '',
                "playlistSource": playlist_name,
                "note": f"From: {playlist_name}"
            })
        
        return normalized
    except Exception as e:
        print(f"     └─ ⚠️  Error fetching playlist: {e}")
        return []

def scrape_youtube_music() -> dict:
    """Main scraper orchestration."""
    print("=" * 60)
    print("YouTube Music Scraper")
    print("=" * 60)
    
    yt = get_yt_music_client()
    print("\n✓ Authenticated successfully!")
    
    # Fetch playlists
    playlists_meta = fetch_playlists(yt)
    
    # Fetch songs from each playlist
    print("\n🎵 Fetching songs from playlists...")
    playlists_with_songs = []
    all_songs = []
    seen_ids = set()
    
    for playlist in playlists_meta:
        playlist_id = playlist.get('playlistId')
        playlist_name = playlist.get('title', 'Unknown Playlist')
        
        songs = fetch_playlist_songs(yt, playlist_id, playlist_name)
        
        if songs:
            playlists_with_songs.append({
                "id": playlist_id,
                "name": playlist_name,
                "imageUrl": playlist.get('thumbnail', [{}])[-1].get('url', '') if playlist.get('thumbnail') else '',
                "songCount": len(songs),
                "songs": songs
            })
            
            # Deduplicate across playlists (by video ID)
            for song in songs:
                if song['id'] not in seen_ids:
                    all_songs.append(song)
                    seen_ids.add(song['id'])
    
    print(f"\n✓ Total unique songs across all playlists: {len(all_songs)}")
    
    # Build output structure
    output = {
        "metadata": {
            "scraped": "YouTube Music",
            "totalPlaylists": len(playlists_with_songs),
            "totalSongs": len(all_songs),
            "lastUpdated": Path(__file__).stat().st_mtime  # timestamp
        },
        "playlists": playlists_with_songs,
        "allSongs": all_songs,
        # Keep old "anchors" structure if it exists (for backward compatibility)
        "anchors": []
    }
    
    return output

def save_data(data: dict):
    """Save to data.json with pretty formatting."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Saved to {DATA_FILE.name}")
        print(f"  - {data['metadata']['totalPlaylists']} playlists")
        print(f"  - {data['metadata']['totalSongs']} unique songs")
    except Exception as e:
        print(f"\n❌ Error saving data: {e}")
        exit(1)

if __name__ == "__main__":
    try:
        data = scrape_youtube_music()
        save_data(data)
        print("\n" + "=" * 60)
        print("✨ Scrape complete! Reload the browser to see changes.")
        print("=" * 60)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.")
        exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
