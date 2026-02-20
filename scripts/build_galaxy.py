import json
import math
import yt_dlp
import os
import sys

# Seeded random for matching JS layout exactly
_seed = 1

def py_imul(a, b):
    # Simulate JS Math.imul
    return ((a & 0xffff) * b + (((a >> 16) * b) & 0xffff) << 16) & 0xffffffff

def hash_str(s):
    h = 0x811c9dc5
    for c in s:
        h ^= ord(c)
        h = py_imul(h, 0x01000193)
    return h & 0xffffffff

def seed_random(s):
    global _seed
    _seed = hash_str(s)

def rand():
    global _seed
    _seed = (_seed * 1664525 + 1013904223) % 4294967296
    return _seed / 4294967296

COLORS = [
    "#FF1744", "#F50057", "#D500F9", "#651FFF", "#2979F3", "#00B0FF",
    "#00E5FF", "#1DE9B6", "#00E676", "#76FF03", "#FFEA00", "#FFC400",
    "#FF9100", "#FF3D00", "#FF5252", "#FF80AB", "#E040FB", "#536DFE"
]

def load_curator_notes():
    # Read existing data.json to preserve descriptions
    notes = {}
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            try:
                data = json.load(f)
                for a in data.get("anchors", []):
                    if a.get("description"):
                        notes[a["id"]] = a["description"]
            except Exception:
                pass
    return notes

def fetch_playlist_data():
    if not os.path.exists("playlists.txt"):
        print("playlists.txt not found. Please create it and add YouTube playlist URLs.")
        sys.exit(1)

    urls = []
    with open("playlists.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)

    playlists = []
    individual_songs = []
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
    }

    print(f"Fetching metadata for {len(urls)} playlists...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"Scraping {url}...")
                info = ydl.extract_info(url, download=False)
                if not info:
                    continue
                
                if 'entries' not in info:
                    # It's a single video, not a playlist
                    song_id = info.get('id')
                    title = info.get('title')
                    if song_id and title:
                        individual_songs.append({
                            'ytId': song_id,
                            'title': title,
                            'artist': info.get('uploader', 'Unknown Artist'),
                            'duration': info.get('duration', 0) if info.get('duration') is not None else 0,
                            'status': 'active',
                            'thumbnail': f"https://img.youtube.com/vi/{song_id}/maxresdefault.jpg"
                        })
                    continue
                
                playlist_id = info.get('id', 'unknown')
                playlist_name = info.get('title', 'Unknown Playlist')
                playlist_author = info.get('uploader', 'Unknown Author')
                
                songs = []
                for entry in info['entries']:
                    if not entry:
                        continue
                    song_id = entry.get('id')
                    title = entry.get('title')
                    if song_id and title:
                        songs.append({
                            'ytId': song_id,
                            'title': title,
                            'artist': entry.get('uploader', playlist_author),
                            'duration': entry.get('duration', 0) if entry.get('duration') is not None else 0,
                            'status': 'active',
                            'thumbnail': f"https://img.youtube.com/vi/{song_id}/maxresdefault.jpg"
                        })
                
                if songs:
                    playlists.append({
                        'id': playlist_id,
                        'name': playlist_name,
                        'author': playlist_author,
                        'url': url,
                        'songCount': len(songs),
                        'songs': songs
                    })
            except Exception as e:
                print(f"Error fetching {url}: {e}")

    if individual_songs:
        playlists.append({
            'id': 'individual_songs',
            'name': 'Individual Songs',
            'author': 'Various Artists',
            'url': 'System Generated',
            'songCount': len(individual_songs),
            'songs': individual_songs
        })

    return playlists

def cluster_simulation(playlists, curator_notes):
    print("Running Clustering Simulation...")
    seed_random("MunirMusicGalaxy")
    
    # Sort: Largest playlists first
    sorted_p = sorted(enumerate(playlists), key=lambda x: x[1]['songCount'], reverse=True)
    
    radii = [220 + (p['songCount'] / 50) * 450 for p in playlists]
    
    placed = []
    anchors = []
    p_positions = [None] * len(playlists)
    
    for sort_order, (original_idx, p) in enumerate(sorted_p):
        radius = radii[original_idx]
        x, y = 0, 0
        found = False
        
        if sort_order == 0:
            x, y = 0, 0
            found = True
        else:
            attempt = 0
            ring_start = 600
            while not found and attempt < 2000:
                attempt += 1
                search_dist = ring_start + (attempt * 5)
                angle = rand() * math.pi * 2
                tx = math.cos(angle) * search_dist
                ty = math.sin(angle) * search_dist
                
                overlaps = False
                for exist in placed:
                    dist = math.hypot(tx - exist['x'], ty - exist['y'])
                    if dist < (radius + exist['radius'] + 400):
                        overlaps = True
                        break
                
                if not overlaps:
                    x, y = tx, ty
                    found = True
        
        placed.append({'x': x, 'y': y, 'radius': radius})
        color = COLORS[original_idx % len(COLORS)]
        p_positions[original_idx] = {'x': x, 'y': y, 'radius': radius}
        
        anchor_data = {
            'id': p['id'],
            'name': p['name'],
            'x': round(x),
            'y': round(y),
            'color': color,
            'radius': round(radius)
        }
        
        # Restore curator notes if they exist
        if p['id'] in curator_notes:
            anchor_data['description'] = curator_notes[p['id']]
            
        anchors.append(anchor_data)

    # Place Songs
    for idx, p in enumerate(playlists):
        center = p_positions[idx]
        if not center:
            continue
            
        placed_songs = []
        for song in p['songs']:
            sx, sy = center['x'], center['y']
            placed_s = False
            
            min_r = 120
            max_r = center['radius'] * 1.1
            
            s_attempt = 0
            while not placed_s and s_attempt < 300:
                s_attempt += 1
                r = min_r + math.sqrt(rand()) * (max_r - min_r)
                th = rand() * math.pi * 2
                tx = center['x'] + math.cos(th) * r
                ty = center['y'] + math.sin(th) * r
                
                claps = any(math.hypot(tx - ps['x'], ty - ps['y']) < 85 for ps in placed_songs)
                if not claps:
                    sx, sy = tx, ty
                    placed_s = True
            
            if not placed_s:
                spiral_angle = 0
                spiral_dist = min_r
                spiral_limit = 0
                while not placed_s and spiral_limit < 5000:
                    spiral_limit += 1
                    spiral_angle += 0.3
                    spiral_dist += 2
                    
                    tx = center['x'] + math.cos(spiral_angle) * spiral_dist
                    ty = center['y'] + math.sin(spiral_angle) * spiral_dist
                    
                    claps = any(math.hypot(tx - ps['x'], ty - ps['y']) < 85 for ps in placed_songs)
                    if not claps:
                        sx, sy = tx, ty
                        placed_s = True
                        if spiral_dist > center['radius']:
                            center['radius'] = spiral_dist
                            # Update anchor radius if expanded
                            for a in anchors:
                                if a['id'] == p['id']:
                                    a['radius'] = round(spiral_dist)
            
            song['x'] = round(sx)
            song['y'] = round(sy)
            placed_songs.append({'x': sx, 'y': sy})

        # Process collisions slightly
        for _ in range(3):
            for i in range(len(placed_songs)):
                for j in range(i + 1, len(placed_songs)):
                    dx = placed_songs[j]['x'] - placed_songs[i]['x']
                    dy = placed_songs[j]['y'] - placed_songs[i]['y']
                    dist = math.hypot(dx, dy)
                    if dist < 85 and dist > 0:
                        push = (85 - dist) / 2
                        placed_songs[i]['x'] -= (dx / dist) * push
                        placed_songs[i]['y'] -= (dy / dist) * push
                        placed_songs[j]['x'] += (dx / dist) * push
                        placed_songs[j]['y'] += (dy / dist) * push
        
        # Map back to song objects
        for s_idx, song in enumerate(p['songs']):
            song['x'] = round(placed_songs[s_idx]['x'])
            song['y'] = round(placed_songs[s_idx]['y'])
            song['offset'] = round(rand() * 100)
            
            # Map the color from the parent anchor
            for a in anchors:
                if a['id'] == p['id']:
                    song['color'] = a['color']
                    break

    # Final pass to ensure anchors contain all their songs
    for a in anchors:
        max_dist = 0
        p = next((pl for pl in playlists if pl['id'] == a['id']), None)
        if p:
            for s in p['songs']:
                d = math.hypot(s['x'] - a['x'], s['y'] - a['y'])
                if d > max_dist:
                    max_dist = d
            a['radius'] = round(max_dist + 150)

    print("Clustering complete.")
    return playlists, anchors

def main():
    curator_notes = load_curator_notes()
    playlists = fetch_playlist_data()
    
    if not playlists:
        print("No playlists fetched. Exiting.")
        sys.exit(1)
        
    playlists, anchors = cluster_simulation(playlists, curator_notes)
    
    output = {
        "playlists": playlists,
        "anchors": anchors
    }
    
    with open("data.json", "w") as f:
        json.dump(output, f, indent=2)
        
    print("Successfully wrote data.json!")

if __name__ == "__main__":
    main()
