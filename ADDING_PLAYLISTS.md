# Adding More Playlists to Munir's Music Gallery

This guide explains how to add new YouTube Music playlists to your music gallery.

## Process Overview

The workflow has 4 simple steps:
1. **Scrape** playlists from YouTube Music
2. **Merge** song data into data.json
3. **Auto-arrange** using the clustering script
4. **Refresh** and explore!

---

## Step 1: Scrape YouTube Music Playlists

You have a JavaScript scraper built-in that extracts videos from YouTube Music.

### Instructions:

1. **Open YouTube Music** in your browser
   - Navigate to the playlist you want to scrape
   - Ensure all songs are loaded (scroll to the bottom if needed)

2. **Open Developer Tools**
   - Press **F12** (Windows/Linux) or **Cmd+Option+I** (Mac)
   - Navigate to the **Console** tab

3. **Copy and run the scraper**
   - Open [`datascrapper.js`](datascrapper.js)
   - Copy the entire code
   - Paste into the browser console
   - Press Enter

4. **Follow the prompts**
   - **Center X**: X-coordinate for the cluster (e.g., `-500`, `0`, `500`)
   - **Center Y**: Y-coordinate for the cluster (e.g., `500`, `-300`)
   - **Note**: A description for this batch (e.g., "K-pop favorites", "Chill vibes")

5. **Copy the output**
   - The script will output JSON with all songs
   - Copy the entire JSON output

---

## Step 2: Merge into data.json

You have two options:

### Option A: Use the Built-in Editor (Recommended)

1. **Open** `22DecTry.html` in your browser
2. **Toggle Editor Mode**
   - Press **Shift+E** to enable editor
   - You'll see a blue panel on the right side
3. **Import the data**
   - Paste the scraped JSON in the "**IMPORT DATA**" box
   - Click "**⬇ MERGE INTO ARCHIVE**"
4. **Export the updated data**
   - Click "**📋 COPY FULL JSON**"
   - You'll get a confirmation message
5. **Manually update** `data.json`
   - Replace the entire contents with the copied JSON
   - Save the file

### Option B: Manual Edit

1. **Open** `data.json` in your editor
2. **Add to the playlists array**
   - Follow the existing structure
3. **Template for a new playlist:**

```json
{
  "id": "YOUTUBE_PLAYLIST_ID",
  "name": "Your Playlist Name",
  "imageUrl": "",
  "songCount": 15,
  "songs": [
    {
      "title": "Song Title",
      "artist": "Artist Name",
      "duration": 180,
      "album": "Album Name",
      "thumbnail": "",
      "playlistSource": "Your Playlist Name",
      "x": 0,
      "y": 0,
      "status": "active",
      "ytId": "YOUTUBE_VIDEO_ID",
      "offset": 0,
      "note": ""
    }
  ]
}
```

**Field Explanations:**
- `id`: YouTube playlist ID (from URL)
- `name`: Display name for the playlist
- `songCount`: Total number of songs
- `songs`: Array of song objects
  - `ytId`: YouTube video ID
  - `title`, `artist`, `album`: Song metadata
  - `duration`: Length in seconds
  - `status`: "active" for playable, or "error" for broken links
  - `x`, `y`: Will be recalculated by the script
  - `offset`: Random offset for animation (0-100)

---

## Step 3: Auto-Position & Cluster

The magic happens here! Run the clustering script to automatically position everything:

```bash
python3 cluster_playlists.py
```

### What the script does:

✅ **Randomly scatters playlist clusters** across the map  
✅ **Positions songs within each cluster** (guaranteed no overlaps!)  
✅ **Assigns distinct colors** to each playlist zone  
✅ **Calculates anchor sizes** based on playlist density  
✅ **Updates x, y coordinates** for all songs  
✅ **Updates data.json** automatically  

**No manual positioning needed!** The algorithm handles all the spatial arrangement.

### Example Output:
```
✅ Data updated successfully!

Created 19 anchors for 19 playlists:
  PL7: Playlist: K-Pop Favorites
    Position: (1078, 1701)
    Color: #00E5FF, Radius: 1830
  PL8: Playlist: Chill Vibes
    Position: (-1777, -640)
    Color: #1DE9B6, Radius: 1510
```

---

## Step 4: Refresh & Explore

1. **Refresh** your browser (F5 or Cmd+R)
2. **Click "ENTER THE MUSIC GALLERY"**
3. **Explore!**
   - Use WASD or drag to move
   - Walk into colored zones to discover songs
   - Use "Guide Me Somewhere" for guided tours (20-25 songs!)

---

## Advanced Options

### Editing Existing Playlists

1. Open `22DecTry.html`
2. Press **Shift+E** for editor mode
3. Click on any bubble to edit its title and notes
4. Changes are temporary until you export

### Removing Playlists

1. Open `data.json`
2. Find the playlist in the `playlists` array
3. Delete the entire object
4. Run `python3 cluster_playlists.py` to recalculate

### Custom Colors

Edit `cluster_playlists.py` to change the color palette:

```python
colors = [
    "#FF1744",  # Deep red
    "#F50057",  # Hot pink
    ...
]
```

---

## Troubleshooting

### Songs aren't showing up
- Run `python3 cluster_playlists.py` again
- Clear browser cache (Ctrl+Shift+Delete)
- Check that `status` is "active" for songs

### Bubbles overlapping
- This shouldn't happen! The collision detection prevents it
- If it does, re-run the clustering script

### YouTube videos unavailable
- The HTML marks these as "error" (red bubbles)
- They won't play but won't crash the app
- Safe to ignore

---

## Tips for Best Results

1. **Keep playlists of similar size together**
   - Mix of 15 and 99 song playlists works fine
   - The script adapts anchor sizes automatically

2. **Add notes to songs**
   - In editor mode, add personal notes
   - Helps you remember why you love a track

3. **Use meaningful playlist names**
   - Shows up in the gallery UI
   - Helps with navigation

4. **Regular updates**
   - Re-run the clustering after adding/removing songs
   - Everything recalculates automatically

---

## File Reference

| File | Purpose |
|------|---------|
| `data.json` | Main data store (playlists, songs, anchors) |
| `datascrapper.js` | Browser scraper for YouTube Music |
| `cluster_playlists.py` | Auto-positioning and clustering algorithm |
| `22DecTry.html` | Main interactive gallery |
| `ADDING_PLAYLISTS.md` | This guide! |

---

## Questions?

- Check the clustering output for any warnings
- Verify JSON is valid (use a JSON validator if stuck)
- All coordinates are automatically calculated - no manual math needed!

Enjoy building your music gallery! 🎵✨
