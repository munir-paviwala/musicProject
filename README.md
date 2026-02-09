# 🎵 Munir's Music Gallery

A spatial, interactive music visualization that turns your YouTube Music library into an immersive exploration experience. Walk through a 2D canvas where songs are positioned as discoverable entities within colored emotional zones. View all your playlists in an analytics dashboard.

## ✨ Features

### 🗺️ Spatial Explorer
- **2D Canvas Navigation**: Walk through an infinite landscape using WASD or drag controls
- **Proximity-Based Playback**: Enter a song's zone to play it automatically
- **Guided Tours**: Two pathfinding algorithms for discovering distant songs
- **Autopilot Mode**: Auto-navigate and queue songs for continuous listening
- **Emotional Zones**: Color-coded "anchors" create atmospheric regions
- **Path Tracing**: Visual history of your exploration journey

### 📊 Playlist Dashboard
- View all your favorited and user-created playlists
- Statistics: song count, total duration per playlist
- Click any playlist card to play a random song from it
- Toggle between dashboard and explorer views

### 🎨 Dynamic Background
- **Breathing Cosmos**: Animated particle system with pulsing opacity
- Layered gradient backgrounds (navy → purple → teal)
- Responsive to viewport changes
- Smooth, non-intrusive ambient effects

### 🔧 Data Management
- **Import/Export**: Edit and merge song batches via JSON
- **Scatter Function**: Randomize clustered song positions
- **Editor Mode**: Shift+E to edit individual songs

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- `pip` package manager
- A YouTube Music account

### Installation & Setup

1. **Clone or navigate to the project**:
   ```bash
   cd /path/to/musicProject
   ```

2. **Install Python dependencies**:
   ```bash
   pip install ytmusicapi
   ```

3. **Run the scraper** (first time):
   ```bash
   python3 yt_music_scraper.py
   ```
   
   On first run:
   - Opens your browser for OAuth authentication
   - Approve access to your YouTube Music account
   - Credentials are cached locally in `.yt_music_headers.json` (not shared)
   - Subsequent runs use cached credentials (no browser needed)

4. **View in browser**:
   ```bash
   # Open index.html or 22DecTry.html in a web browser
   # If using local server:
   python3 -m http.server 8000
   # Then visit http://localhost:8000
   ```

---

## 📋 How to Use

### Exploring the Gallery

**Navigation**:
- `W/A/S/D` → Move around the canvas
- **Mouse Drag** → Pan the view
- **Scroll Wheel** → Zoom in/out

**Interacting with Songs**:
- Walk into a song bubble to play it
- **Shift+E** → Enter Editor Mode to rename/reposition songs
- **Click bubbles** in Editor Mode to select and edit

**Guided Tours**:
- **🎲 Guide Me Somewhere** → Choose a random distant song with optimized path
- **🏘️ Explore Neighborhood** → Spiral outward discovering nearby songs
- **▶ Start Tour / ⏸ Pause Tour** → Auto-navigate the guided path
- **⏭ Skip to Next** → Jump to the next song in tour (during listening)
- **❌ Stop Guide** → Cancel the tour

**Dashboard**:
- Click the **📊 Dashboard** button (top-left)
- View all your playlists and statistics
- Click any playlist card to play a random song
- Click **📊 Dashboard** again to return to explorer view

---

## 📊 Data Format

### New Format (Playlist-Aware)
The scraper outputs `data.json` in this structure:

```json
{
  "metadata": {
    "scraped": "YouTube Music",
    "totalPlaylists": 5,
    "totalSongs": 120,
    "lastUpdated": 1706000000
  },
  "playlists": [
    {
      "id": "RDCLAK...",
      "name": "My Favorite Bollywood",
      "imageUrl": "https://...",
      "songCount": 25,
      "songs": [
        {
          "id": "abc123",
          "title": "Song Name",
          "artist": "Artist Name",
          "duration": 180,
          "album": "Album Name",
          "thumbnail": "https://...",
          "playlistSource": "My Favorite Bollywood",
          "note": "From: My Favorite Bollywood"
        }
      ]
    }
  ],
  "allSongs": [...],  // Flattened, deduplicated across playlists
  "anchors": [...]    // Color zones (unchanged)
}
```

### Legacy Format
Old data with flat `songs` array is automatically converted to the new format on load.

---

## 🔄 Updating Your Music

To refresh your library with new songs from YouTube Music:

```bash
python3 yt_music_scraper.py
```

This will:
1. Discover your favorited and user-created playlists (already cached, minimal API calls)
2. Fetch all songs from each playlist with metadata
3. Deduplicate across playlists
4. Overwrite `data.json`
5. **Reload your browser** to see changes

**Frequency**: Designed for annual or semi-annual updates from your account only. Rate limiting is intentionally minimal to avoid YouTube Music API restrictions.

---

## 🛠️ Advanced Usage

### Editor Mode (Shift+E)

In Editor Mode you can:
- **Click songs** to select and edit their title/note
- **Drag songs** to reposition them
- **Import JSON** → Paste song data from external sources
- **Export JSON** → Save your entire archive as JSON
- **Scatter Pile** → Randomize positions of clustered songs

### Manual Song Import

If you want to add songs without running the scraper:

1. Press **Shift+E** to enter Editor Mode
2. In the "IMPORT DATA" section, paste a JSON array of songs:
   ```json
   [
     {
       "id": "unique-id",
       "ytId": "youtube-video-id",
       "x": 100,
       "y": 200,
       "title": "Song Title",
       "note": "Optional notes",
       "offset": 0
     }
   ]
   ```
3. Click **⬇ MERGE INTO ARCHIVE**
4. Click **📋 COPY FULL JSON** to save the updated data
5. Replace `data.json` contents and reload

---

## 🎨 Customization

### Color Zones (Anchors)
Edit the `anchors` array in `data.json`:

```json
{
  "x": 0,
  "y": 0,
  "color": "#ff6b6b",
  "radius": 400,
  "name": "Warm Red"
}
```

### Background Particles
In `22DecTry.html`, find the `initParticles()` function to adjust:
- `particleCount`: Number of floating particles
- `size`: Particle diameter
- `opacity`: Visibility (0-1)
- Colors in `drawBackground()` gradient

---

## ⚠️ Important Notes

### Authentication & Privacy
- **One-Time Setup**: First run opens your browser for OAuth approval
- **Local Credentials**: Auth tokens stored in `.yt_music_headers.json` (never uploaded)
- **No Data Sharing**: Your playlists are only stored locally in `data.json`
- **User-Only Access**: Designed for single-account personal use

### Rate Limiting
- The scraper uses `ytmusicapi`, which minimizes API calls
- Designed to be run ~once per year per account
- If you exceed YouTube's rate limits, wait 24 hours and try again

### Broken Videos
- Unavailable videos are marked with a red circle
- They're automatically skipped during autopilot
- Edit mode shows them clearly for removal

---

## 🐛 Troubleshooting

### "❌ ytmusicapi not installed"
```bash
pip install ytmusicapi
```

### "Browser didn't open for authentication"
Manually run:
```bash
python3 -c "from ytmusicapi import YTMusic; YTMusic.setup(filepath='.yt_music_headers.json')"
```
Then approve in the browser window that opens.

### Songs not loading in browser
- Check browser console for errors (F12 → Console)
- Ensure `data.json` exists and has valid JSON
- Try hard-refreshing (Ctrl+Shift+R or Cmd+Shift+R)

### No playlists appearing in dashboard
- Run the scraper again: `python3 yt_music_scraper.py`
- Check that `data.json` has a `playlists` array (not just legacy `songs`)

---

## 📝 Architecture

- **[22DecTry.html](22DecTry.html)** – Main app (canvas explorer + dashboard + background)
- **[index.html](index.html)** – Redirect to 22DecTry.html
- **[yt_music_scraper.py](yt_music_scraper.py)** – YouTube Music scraper (local Python script)
- **[data.json](data.json)** – Your music library (playlists + songs + zones)
- **[datascrapper.js](datascrapper.js)** – Legacy browser-based scraper (reference only)

---

## 🎯 Roadmap

- [ ] Mood/tempo-based automatic color assignment
- [ ] Weighted clustering by artist/genre
- [ ] Heatmap visualization of play frequency
- [ ] Touch controls for mobile
- [ ] Audio waveform visualization
- [ ] Spotify/Apple Music integration

---

## 📄 License

Personal project. Feel free to modify for your own use.

---

## 💬 Questions?

This gallery is designed to be personal and evolving. Update it yearly with fresh music discoveries, explore the spatial arrangement, and enjoy the ambient experience of walking through your musical landscape.

**Happy exploring! 🎵✨**
