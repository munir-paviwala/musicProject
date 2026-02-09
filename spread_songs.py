#!/usr/bin/env python3
import json
import random
import math

with open('data.json', 'r') as f:
    data = json.load(f)

def spread_coords(index, total):
    """Spread songs in a circular/spiral pattern across a large area"""
    # Use golden angle spiral for better distribution
    angle = index * 2.39996  # Golden angle in radians
    radius = 100 + math.sqrt(index) * 80  # Exponential spiral
    
    x = int(math.cos(angle) * radius)
    y = int(math.sin(angle) * radius)
    
    # Add some random jitter to avoid perfect circles
    x += random.randint(-30, 30)
    y += random.randint(-30, 30)
    
    return x, y

# Spread allSongs more widely
total_songs = len(data['allSongs'])
for i, song in enumerate(data['allSongs']):
    x, y = spread_coords(i, total_songs)
    song['x'] = x
    song['y'] = y

# Also update playlists to match
playlist_song_map = {}
for playlist in data['playlists']:
    for song in playlist['songs']:
        ytId = song.get('ytId')
        if ytId:
            # Find matching song in allSongs and copy coordinates
            for all_song in data['allSongs']:
                if all_song.get('ytId') == ytId:
                    song['x'] = all_song['x']
                    song['y'] = all_song['y']
                    break

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Spread {total_songs} songs across a wider area")
print(f"✓ Max distance from origin: ~{int(math.sqrt(total_songs) * 80)} units")
print(f"✓ Songs should no longer overlap")
