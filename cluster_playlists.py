import json
import math
import random

# Load data
with open('data.json', 'r') as f:
    data = json.load(f)

playlists = data['playlists']
num_playlists = len(playlists)

# Vibrant colors that work well on black background
colors = [
    "#FF1744",  # Deep red
    "#F50057",  # Hot pink
    "#D500F9",  # Purple
    "#651FFF",  # Deep purple blue
    "#2979F3",  # Bright blue
    "#00B0FF",  # Light blue
    "#00E5FF",  # Cyan
    "#1DE9B6",  # Teal
    "#00E676",  # Bright green
    "#76FF03",  # Lime green
    "#FFEA00",  # Golden yellow
    "#FFC400",  # Amber
    "#FF9100",  # Orange
    "#FF3D00",  # Deep orange
    "#FF5252",  # Red accent
    "#FF80AB",  # Pink accent
    "#E040FB",  # Purple accent
    "#536DFE",  # Blue accent
    "#448AFF"   # Light blue accent
]

# Arrange playlists closer together around the origin
# Sort playlists by size for better packing
sorted_indices = sorted(range(num_playlists), key=lambda i: playlists[i]['songCount'], reverse=True)

anchors = []
playlist_positions = []

# Calculate radii first
radii = []
for i, playlist in enumerate(playlists):
    song_count = playlist['songCount']
    radius = 200 + (song_count / 99) * 250  # Smaller radii (200-450)
    radii.append(radius)

# Place larger clusters first using random placement with constraints
placed_positions = []  # List of (x, y, radius) tuples

for idx, i in enumerate(sorted_indices):
    playlist = playlists[i]
    song_count = playlist['songCount']
    radius = radii[i]
    
    # Try random positions until we find a non-overlapping spot
    placed = False
    attempts = 0
    while not placed and attempts < 200:
        # Random angle and distance with preference for larger distances
        angle = random.uniform(0, 2 * math.pi)
        # Weighted random to prefer further distances
        base_dist = random.uniform(400, 3500)
        
        x = base_dist * math.cos(angle)
        y = base_dist * math.sin(angle)
        
        # Check if this position overlaps with any existing clusters
        overlaps = False
        for px, py, pr in placed_positions:
            center_dist = math.sqrt((x - px)**2 + (y - py)**2)
            if center_dist < (radius + pr + 150):  # 150px minimum separation
                overlaps = True
                break
        
        if not overlaps:
            placed_positions.append((x, y, radius))
            placed = True
        
        attempts += 1
    
    # If still not placed after random attempts, force it at a safe distance
    if not placed:
        angle = random.uniform(0, 2 * math.pi)
        dist = 3500 + random.uniform(500, 1500)
        x = dist * math.cos(angle)
        y = dist * math.sin(angle)
        placed_positions.append((x, y, radius))

# Create anchors and map positions back to original playlist indices
playlist_positions = [None] * num_playlists  # Array to hold positions by original index

for idx, i in enumerate(sorted_indices):
    color = colors[i % len(colors)]
    x, y, radius = placed_positions[idx]
    
    # Create anchor
    anchor = {
        "id": f"PL{i+1}",
        "x": round(x),
        "y": round(y),
        "color": color,
        "radius": round(radius),  # This will be updated after songs are placed
        "name": playlists[i]['name']
    }
    anchors.append(anchor)
    
    # Store position by original index
    playlist_positions[i] = {
        "index": i,
        "x": x,
        "y": y,
        "radius": radius,
        "song_count": playlists[i]['songCount'],
        "anchor_id": f"PL{i+1}"
    }

# Now update song positions within each cluster with collision avoidance
for i, playlist in enumerate(playlists):
    pos = playlist_positions[i]
    if pos is None:
        continue
    cx, cy = pos['x'], pos['y']
    songs = playlist['songs']
    song_count = len(songs)
    
    # Distribute songs with guaranteed no overlap
    # Bubble radius is 35px, plus 6px animation movement, so need 82px minimum between centers
    BUBBLE_RADIUS = 35
    ANIMATION_MOVEMENT = 6
    MIN_DISTANCE_BETWEEN = BUBBLE_RADIUS * 2 + ANIMATION_MOVEMENT * 2 + 10  # 92px minimum
    
    song_positions = []  # Track (x, y) of placed songs
    
    for j, song in enumerate(songs):
        if song_count == 1:
            song['x'] = round(cx)
            song['y'] = round(cy)
        else:
            placed = False
            # Calculate how many songs fit in a circle at different radii
            for ring in range(20):  # Try up to 20 rings
                # Ring distance from center - ensure big gaps between rings
                ring_distance = 200 + ring * 120  # 200, 320, 440, 560... (120px between rings)
                
                # Max songs that fit in this ring (circumference / min spacing)
                circumference = 2 * math.pi * ring_distance
                max_in_ring = max(1, int(circumference / MIN_DISTANCE_BETWEEN))
                
                # Skip if we already have enough songs for this ring
                if j < ring * max_in_ring:
                    continue
                
                # Position within this ring
                position_in_ring = j - (ring * max_in_ring)
                if position_in_ring < max_in_ring:
                    angle = (position_in_ring / max_in_ring) * 2 * math.pi
                    x = cx + ring_distance * math.cos(angle)
                    y = cy + ring_distance * math.sin(angle)
                    
                    # Verify no collision with previously placed songs
                    collision = False
                    for px, py in song_positions:
                        dist = math.sqrt((x - px)**2 + (y - py)**2)
                        if dist < MIN_DISTANCE_BETWEEN:
                            collision = True
                            break
                    
                    if not collision:
                        song['x'] = round(x)
                        song['y'] = round(y)
                        song_positions.append((x, y))
                        placed = True
                        break
            
            # Fallback: find safe spot even if algorithm fails
            if not placed:
                # Spiral outward until we find space
                for attempt in range(500):
                    angle = (attempt * 0.618) * 2 * math.pi
                    dist = 100 + (attempt // 3) * 80
                    x = cx + dist * math.cos(angle)
                    y = cy + dist * math.sin(angle)
                    
                    collision = False
                    for px, py in song_positions:
                        if math.sqrt((x - px)**2 + (y - py)**2) < MIN_DISTANCE_BETWEEN:
                            collision = True
                            break
                    
                    if not collision:
                        song['x'] = round(x)
                        song['y'] = round(y)
                        song_positions.append((x, y))
                        placed = True
                        break

# Update anchor radii based on actual song concentration
# Calculate the maximum distance from cluster center to furthest song
for i, playlist in enumerate(playlists):
    if playlist_positions[i] is None:
        continue
    
    cx, cy = playlist_positions[i]['x'], playlist_positions[i]['y']
    songs = playlist['songs']
    
    if len(songs) == 0:
        continue
    
    # Find the furthest song from cluster center
    max_distance = 0
    for song in songs:
        dist = math.sqrt((song['x'] - cx)**2 + (song['y'] - cy)**2)
        max_distance = max(max_distance, dist)
    
    # Update the anchor radius to encompass all songs with buffer
    # Buffer is 50px to give room for the glowing effect
    new_radius = max_distance + 50
    
    # Find the anchor for this playlist and update it
    anchor_id = playlist_positions[i]['anchor_id']
    for anchor in anchors:
        if anchor['id'] == anchor_id:
            anchor['radius'] = round(new_radius)
            break

# Update data with new anchors
data['anchors'] = anchors

# Save updated data
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Data updated successfully!")
print(f"\nCreated {len(anchors)} anchors for {num_playlists} playlists:")
for anchor in anchors:
    print(f"  {anchor['id']}: {anchor['name']}")
    print(f"    Position: ({anchor['x']}, {anchor['y']})")
    print(f"    Color: {anchor['color']}, Radius: {anchor['radius']}")
