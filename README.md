# 🎵 Music Galaxy

Welcome to **Music Galaxy**, a beautiful, interactive, and open-source web application that visualizes your favorite YouTube playlists as a navigable star map. 

This repository is designed as a **Template**. You can fork it, add your own music, and deploy it for free in less than 5 minutes—no coding required!

---

## 🚀 How to Create Your Own Galaxy

Follow these simple steps to launch your personalized Music Galaxy using GitHub Pages and automated background scripts.

### Step 1: Create Your Repository
1. Click the green **"Use this template"** button at the top right of this repository.
2. Select **"Create a new repository"**.
3. Give your repository a name (e.g., `my-music-galaxy`) and make sure it is set to **Public** (required for free GitHub Pages).
4. Click **"Create repository"**.

### Step 2: Enable GitHub Pages
By default, GitHub Pages uses classic branches. We use modern GitHub Actions for automatic deployment.
1. In your new repository, go to the **Settings** tab.
2. Click on **Pages** in the left sidebar.
3. Under the **Build and deployment** section, look for the **Source** dropdown.
4. Change the source from *Deploy from a branch* to **GitHub Actions**.

### Step 3: Personalize Your App
1. Open the file `user_config.js` in your repository.
2. Click the pencil icon (✏️) to edit the file.
3. Change the `pageTitle`, `curatorName`, and `introText` to match your vibe.
4. Commit your changes.

### Step 4: Add Your Music!
This is where the magic happens. You never have to calculate coordinates or run Python scripts yourself.
1. Open the file `playlists.txt`.
2. Click the pencil icon (✏️) to edit the file.
3. Paste the URLs of the **YouTube Playlists** you want to include, one per line.
4. Commit your changes.

**Wait for the Robots!** 🤖
As soon as you commit changes to `playlists.txt`, a hidden GitHub Action will automatically:
- Spin up a server.
- Safely scrape the song metadata (Title, ID, Channel) using `yt-dlp` without downloading any media.
- Run a complex spatial algorithm to group your playlists into clusters.
- Update the `data.json` database.
- Deploy the updated website to GitHub Pages!

You can watch the progress in the **Actions** tab. Once the build finishes, your live galaxy will be available at:
`https://[YOUR_USERNAME].github.io/[YOUR_REPO_NAME]/`

---

## 📝 Curator Notes
Want to add descriptions or context to your playlists? 
1. Visit your live deployed website.
2. Click the **"⚙️ Manage Data"** button in the top right corner.
3. Under **Curator Notes**, click **"📝 Edit Notes"**.
4. Type your descriptions for each cluster.
5. Click **"📋 Copy 'data.json'"**.
6. Come back to your GitHub repository, open `data.json`, edit it, and paste your copied text to save your notes permanently!

---

## ⚖️ Disclaimer & Compliance
This project functions as a specialized, interactive YouTube embed player and strictly adheres to the YouTube Embed API Terms of Service. **No audio files, video files, or copyrighted media are stored on this server or in this repository.** All music is streamed directly from YouTube's servers in real-time. This is a free, non-commercial, open-source personal project designed for educational and artistic purposes.

*Original visual engine and framework created by [Munir Paviwala](https://github.com/munir-paviwala).*
