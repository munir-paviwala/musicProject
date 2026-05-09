import json

with open('/Users/munirmahedipaviwala/github/musicProject/data.json', 'r') as f:
    data = json.load(f)

# Deduplicate playlists
seen_p = set()
new_p = []
for p in data.get('playlists', []):
    if p['id'] not in seen_p:
        new_p.append(p)
        seen_p.add(p['id'])
data['playlists'] = new_p

# Deduplicate anchors and fix radii
seen_a = set()
new_a = []
for a in data.get('anchors', []):
    if a['id'] not in seen_a:
        # Cap radius at something reasonable if it's crazy high
        if a.get('radius', 0) > 2000:
            print(f"Fixing radius for {a['name']}: {a['radius']} -> 600")
            a['radius'] = 600
        new_a.append(a)
        seen_a.add(a['id'])
    else:
        print(f"Removing duplicate anchor: {a['name']} ({a['id']})")

data['anchors'] = new_a

with open('/Users/munirmahedipaviwala/github/musicProject/data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Deduplication and radius fix complete.")
