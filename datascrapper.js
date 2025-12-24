(function() {
    // 1. SETUP & INPUTS
    console.clear();
    let inputX = prompt("🎯 Enter Center X (e.g., -500):", "0");
    let inputY = prompt("🎯 Enter Center Y (e.g., 500):", "0");
    let groupNote = prompt("📝 Note for this batch:", "Imported Playlist");

    let centerX = parseInt(inputX) || 0;
    let centerY = parseInt(inputY) || 0;
    const scatterRadius = 500; 

    console.log("🚀 Scanning containers...");

    // 2. FIND VIDEO CONTAINERS (The Parent Elements)
    // We look for common YouTube video row selectors
    const selectors = [
        'ytd-playlist-video-renderer', // Playlist Row
        'ytd-rich-item-renderer',      // Home/Grid View
        'ytd-compact-video-renderer',  // Sidebar/Next Up
        'ytd-video-renderer'           // Search Results
    ];
    
    // Grab all potential video cards
    const containers = document.querySelectorAll(selectors.join(','));
    const uniqueVideos = new Map();
    const bannedWords = ["play all", "shuffle", "mix -"];

    // 3. EXTRACT FROM EACH CONTAINER
    containers.forEach(card => {
        // Look inside THIS specific card for title and link
        const titleEl = card.querySelector('#video-title');
        const linkEl = card.querySelector('a#thumbnail') || card.querySelector('a');

        if (titleEl && linkEl) {
            let title = titleEl.innerText.trim();
            let href = linkEl.href;
            let idMatch = href.match(/[?&]v=([^&]+)/);

            if (idMatch && title.length > 2) {
                let vidId = idMatch[1];
                
                // Filter junk
                let isJunk = bannedWords.some(w => title.toLowerCase().includes(w));
                
                if (!isJunk && !uniqueVideos.has(vidId)) {
                    uniqueVideos.set(vidId, title);
                }
            }
        }
    });

    // 4. FORMAT OUTPUT
    let output = Array.from(uniqueVideos).map(([id, title], i) => ({
        id: "IMP_" + Date.now() + "_" + i,
        ytId: id,
        x: centerX + Math.round((Math.random() - 0.5) * scatterRadius),
        y: centerY + Math.round((Math.random() - 0.5) * scatterRadius),
        title: title.replace(/\n/g, "").substring(0, 60), // Clean formatting
        note: groupNote,
        offset: Math.round(Math.random() * 100),
        status: "active"
    }));

    // 5. COPY TO CLIPBOARD
    // Try to copy automatically; if it fails, log to console
    try {
        copy(output); 
        console.log(`✅ Success! Copied ${output.length} songs to clipboard.`);
    } catch(e) {
        console.log(`✅ Success! Found ${output.length} songs.`);
        console.log("⬇️ MANUALLY COPY BELOW ⬇️");
        console.log(JSON.stringify(output, null, 2));
    }
})();