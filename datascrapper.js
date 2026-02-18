(function () {
    /**
     * MUSIC GALLERY SCRAPER (Bookmarklet Version)
     * Extract songs from YouTube Playlist page
     */

    console.log("🚀 Scanning for music...");
    const songs = [];
    const seen = new Set();
    const groupName = prompt("Name this playlist batch:", document.title.replace(" - YouTube", "") || "Imported Music");
    if (!groupName) return; // Cancelled

    // Selectors for different YouTube views
    const selectors = [
        'ytd-playlist-video-renderer',
        'ytd-rich-item-renderer',
        'ytd-video-renderer'
    ];

    document.querySelectorAll(selectors.join(',')).forEach(card => {
        const titleEl = card.querySelector('#video-title');
        const linkEl = card.querySelector('a#thumbnail') || card.querySelector('a');
        const timeEl = card.querySelector('ytd-thumbnail-overlay-time-status-renderer span');

        if (titleEl && linkEl) {
            let title = titleEl.innerText.trim();
            let href = linkEl.href;
            let ytIdMatch = href.match(/[?&]v=([^&]+)/);

            if (ytIdMatch) {
                let ytId = ytIdMatch[1];
                if (seen.has(ytId)) return;
                seen.add(ytId);

                // Basic Cleanup
                if (title.toLowerCase().includes("deleted video")) return;
                if (title.toLowerCase().includes("private video")) return;

                songs.push({
                    ytId: ytId,
                    title: title,
                    note: groupName,
                    duration: timeEl ? timeEl.innerText : "",
                    // Default values for the engine to fill later
                    x: 0,
                    y: 0,
                    offset: 0,
                    status: 'active'
                });
            }
        }
    });

    if (songs.length === 0) {
        alert("No songs found! Make sure you scrolled down to load them all.");
        return;
    }

    // Copy to clipboard
    const json = JSON.stringify(songs, null, 2);

    // Create a temporary text area to copy from (more reliable than nav.clipboard in some contexts)
    const el = document.createElement('textarea');
    el.value = json;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);

    alert(`✅ copied ${songs.length} songs!\n\nNow open your Music Gallery,\nclick 'Manage' -> 'Import Data',\nand paste!`);

})();