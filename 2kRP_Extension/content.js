let intervalId = null;

function extractCount(inputString) {
    const match = inputString.match(/\d+/);
    return match ? match[0] : null;
}

function getLocation() {
    const spanElement = document.getElementById('locationText');
    if (spanElement) {
        const linkElement = spanElement.querySelector('a');
        if (linkElement) {
            return linkElement.innerText;
        }
    }
    return null;
}

function getWikiPageUrl() {
    const spanElement = document.getElementById('locationText');
    if (spanElement) {
        const linkElement = spanElement.querySelector('a');
        if (linkElement) {
            return linkElement.href
        }
    }
    return null
}

function getPlayerCount(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        return extractCount(element.innerText) || '0';
    }
    return '0';
}

function getBackgroundImageUrl(element) {
    const style = window.getComputedStyle(element);
    const backgroundImage = style.backgroundImage;
    const urlMatch = backgroundImage.match(/url\(["']?([^"']*)["']?\)/);
    return urlMatch ? urlMatch[1] : null;
}

function sendAllData() {
    const location = getLocation();
    const playersOnline = getPlayerCount('playerCountLabel');
    const playersOnMap = getPlayerCount('mapPlayerCountLabel');
    let badgeImageUrl = null;
    const badgeElement = document.querySelector('#badgeButton .badge');
    const wikiPageUrl = getWikiPageUrl()

    if (badgeElement) {
        badgeImageUrl = getBackgroundImageUrl(badgeElement);
    }

    chrome.runtime.sendMessage({ 
        type: '2KKI_DATA', 
        location, 
        badgeImageUrl, 
        playersOnline, 
        playersOnMap,
        wikiPageUrl
    });
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

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'TOGGLE_EXTENSION') {
        if (message.enabled) {
            startCollecting();
        } else {
            stopCollecting();
        }
    }
});

chrome.storage.sync.get('extensionEnabled', function (data) {
    if (data.extensionEnabled !== false) {
        startCollecting();
    }
});