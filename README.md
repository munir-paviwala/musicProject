# Munir's Music Gallery

A spatial, interactive archive of music playlists visualized as a galaxy of sound.

## 🚀 How to Run

Since modern browsers restrict file access (CORS), you need a simple local server to run this project.

### Method 1: Python (Easiest)
Run this command in your terminal:
```bash
python3 -m http.server 8000
```
Then open: **http://localhost:8000**

### Method 2: GitHub Pages
Simply push this repository to GitHub and enable GitHub Pages in Settings. It works out of the box.

## 🎵 How to Add Music

1.  Open the **Manage Data** panel (Gear icon).
2.  Drag the **"🎵 Scrape Playlist"** button to your bookmarks bar.
3.  Go to any **YouTube Playlist**.
4.  Click the bookmarklet button to capture the song data.
5.  Go back to the Gallery and paste the data into the **Import** box.
6.  Click **Import & Merge**, then **Regenerate Layout**.
7.  Save your changes by copying the JSON to `data.json`.
