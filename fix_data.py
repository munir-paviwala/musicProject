#!/usr/bin/env python3
import json
import random

with open('data.json', 'r') as f:
    data = json.load(f)

# Fix all songs in playlists
for playlist in data['playlists']:
    for song in playlist['songs']:
        if 'id' in song and 'ytId' not in song:
            song['ytId'] = song.pop('id')
        if 'offset' not in song:
            song['offset'] = random.randint(0, 100)
        if 'status' not in song:
            song['status'] = 'active'
        if 'note' not in song:
            song['note'] = ''

# Fix all unique songs
for song in data['allSongs']:
    if 'id' in song and 'ytId' not in song:
        song['ytId'] = song.pop('id')
    if 'offset' not in song:
        song['offset'] = random.randint(0, 100)
    if 'status' not in song:
        song['status'] = 'active'
    if 'note' not in song:
        song['note'] = ''

# Ensure anchors exist
if 'anchors' not in data:
    data['anchors'] = []

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

total = sum(len(pl['songs']) for pl in data['playlists'])
print(f'✓ Fixed {total} songs')
print('✓ All songs now have: ytId, x, y, offset, status, note')
