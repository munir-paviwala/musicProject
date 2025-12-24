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
    let titles = Array.from(document.querySelectorAll('#video-title')).map(el => el.innerText.trim());
    let ids = Array.from(document.querySelectorAll('a#thumbnail')).map(el => {
        let match = el.href.match(/[?&]v=([^&]+)/);
        return match ? match[1] : null;
    }).filter(id => id);

    let output = ids.map((id, i) => ({
        id: "IMP_" + Date.now() + "_" + i,
        ytId: id,
        x: Math.round((Math.random() - 0.5) * 3000),
        y: Math.round((Math.random() - 0.5) * 3000),
        title: titles[i] || "Unknown Song",
        note: "Manually Imported",
        offset: Math.random() * 100
    }));

    console.log(JSON.stringify(output, null, 2));
})();
