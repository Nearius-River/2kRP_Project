let intervalId = null;

function extractCount(inputString) {
    var match = inputString.match(/\d+/);
    
    if (match) {
        return match[0];
    } else {
        return null;
    }
}

function getLocation() {
    const spanElement = document.getElementById('locationText');
    if (spanElement) {
        const linkElement = spanElement.querySelector('a');
        if (linkElement) {
            const location = linkElement.innerText;
            return location;
        }
    }

    return null;
}

function getPlayersOnline() {
    const totalPlayersOnlineElement = document.getElementById('playerCountLabel');
    var totalPlayersOnline;

    try {
        totalPlayersOnline = extractCount(totalPlayersOnlineElement.innerText);
    } catch {
        totalPlayersOnline = '0'
    }

    return totalPlayersOnline
}

function getMapPlayers() {
    const playersOnMapElement = document.getElementById('mapPlayerCountLabel');
    var playersOnMap;

    try {
        playersOnMap = extractCount(playersOnMapElement.innerText);
    } catch{
        playersOnMap = '0';
    }

    return playersOnMap
}

function getBackgroundImageUrl(element) {
    const style = window.getComputedStyle(element);
    const backgroundImage = style.backgroundImage;

    const urlMatch = backgroundImage.match(/url\(["']?([^"']*)["']?\)/);
    return urlMatch ? urlMatch[1] : null;
}

function sendAllData() {
    const location = getLocation();
    const playersOnline = getPlayersOnline()
    const playersOnMap = getMapPlayers()

    // Badge image
    var badgeImageUrl = null;
    const badgeElement = document.querySelector('#badgeButton .badge');

    if (badgeElement) {
        imageUrl = getBackgroundImageUrl(badgeElement);

        if (imageUrl) {
            badgeImageUrl = imageUrl;
        }
    }

    chrome.runtime.sendMessage({ type: '2KKI_DATA', location: location, badgeImageUrl: badgeImageUrl, playersOnline: playersOnline, playersOnMap: playersOnMap });
}

function startCollecting() {
    if (!intervalId) {
        intervalId = setInterval(sendAllData, 15000);
    }
}

function stopCollecting() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'TOGGLE_EXTENSION') {
        if (message.enabled) {
            startCollecting();
        } else {
            stopCollecting();
        }
    }
});

// Initialize the extension based on the stored state
chrome.storage.sync.get('extensionEnabled', function (data) {
    if (data.extensionEnabled !== false) {
        startCollecting();
    }
});
