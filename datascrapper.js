// =========================================================
// YOUTUBE PLAYLIST SCRAPER (THE ARCHIVIST TOOL)
// =========================================================
// Instructions:
// 1. Go to a YouTube Playlist or Video Page.
// 2. Scroll down to load all videos.
// 3. Press F12 (or Right Click -> Inspect).
// 4. Go to "Console" tab.
// 5. Paste this entire script and hit ENTER.
// =========================================================

(function() {
    console.log("🔍 Scanning for videos...");

    // 1. Find all links that look like videos
    const links = document.querySelectorAll('a[href*="/watch?v="]');
    const uniqueVideos = new Map();
    const bannedWords = ["play all", "shuffle", "mix -", "queue"];

    links.forEach((link) => {
        // Get the raw text title
        let title = link.innerText || link.title || link.getAttribute('aria-label');
        let href = link.href;

        // Extract the 11-character Video ID
        let idMatch = href.match(/[?&]v=([^&]+)/);

        if (idMatch && title) {
            let vidId = idMatch[1];
            let cleanTitle = title.trim();

            // FILTER: Check if it's a real song or a UI button
            let isJunk = bannedWords.some(word => cleanTitle.toLowerCase().includes(word));
            
            // FILTER: Ensure title is long enough to be real
            if (!isJunk && cleanTitle.length > 2 && !uniqueVideos.has(vidId)) {
                uniqueVideos.set(vidId, {
                    title: cleanTitle.replace(/\n/g, "").substring(0, 50), // Clean formatting
                    id: vidId
                });
            }
        }
    });

    // 2. Format for Sonic Gallery
    let output = [];
    let i = 0;
    
    uniqueVideos.forEach((video) => {
        // Random Position Generator (Spread out over 2000px)
        let randX = Math.round((Math.random() - 0.5) * 2000);
        let randY = Math.round((Math.random() - 0.5) * 2000);

        output.push({
            id: "IMP_" + Date.now() + "_" + i, // Unique Import ID
            ytId: video.id,
            x: randX, 
            y: randY, 
            title: video.title,
            note: "Imported from YouTube", // Default note
            offset: Math.round(Math.random() * 100) // Random bobbing animation
        });
        i++;
    });

    // 3. Output the result
    console.clear();
    console.log(`✅ Found ${output.length} unique songs.`);
    console.log("⬇️ COPY THE JSON BELOW ⬇️");
    console.log(JSON.stringify(output, null, 2));
    console.log("⬆️ PASTE THIS INTO YOUR data.json FILE ⬆️");
})();