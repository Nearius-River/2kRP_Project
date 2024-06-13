let intervalId = null;
const supportedGameTypes = [
    'unconscious',
    '2kki'
] // TODO: check for more compatibility

/**
 * Extracts the first number found in a string
 * @param {string} inputString
 * @returns {string}
 */
function extractCount(inputString) {
    const match = inputString.match(/\d+/);
    return match ? match[0] : '0';
}

/**
 * Determines the game type based on the URL path
 * @returns {string|null}
 */
function getGameType() {
    const pathname = window.location.pathname;
    
    if (pathname.startsWith('/unconscious/')) {
        return 'unconscious';
    } else if (pathname.startsWith('/2kki/')) {
        return '2kki';
    } else {
        return null;
    }
}

/**
 * Retrieves the location text and the URL from the location span
 * @returns {{location: string|null, wikiPageUrl: string|null}}
 */
function getLocationData() {
    const spanElement = document.getElementById('locationText');
    if (spanElement) {
        const linkElement = spanElement.querySelector('a');
        if (linkElement) {
            return {
                location: linkElement.innerText,
                wikiPageUrl: linkElement.href
            };
        }
    }
    return { location: null, wikiPageUrl: null };
}

/**
 * Retrieves the player count from a specified element by ID
 * @param {string} elementId
 * @returns {string}
 */
function getPlayerCount(elementId) {
    const element = document.getElementById(elementId);
    return element ? extractCount(element.innerText) : '0';
}

/**
 * Retrieves the background image URL of a specified element
 * @param {Element} element
 * @returns {string|null}
 */
function getBackgroundImageUrl(element) {
    const style = window.getComputedStyle(element);
    const backgroundImage = style.backgroundImage;
    const urlMatch = backgroundImage.match(/url\(["']?([^"']*)["']?\)/);
    return urlMatch ? urlMatch[1] : null;
}

/**
 * Sends all collected data to the background script
 */
function sendAllData() {
    const gameType = getGameType()

    if (supportedGameTypes.includes(gameType)) {
        const { location, wikiPageUrl } = getLocationData();
        const playersOnline = getPlayerCount('playerCountLabel');
        const playersOnMap = getPlayerCount('mapPlayerCountLabel');
        let badgeImageUrl = null;
        const badgeElement = document.querySelector('#badgeButton .badge');
    
        if (badgeElement) {
            badgeImageUrl = getBackgroundImageUrl(badgeElement);
        }
    
        chrome.runtime.sendMessage({
            type: '2KKI_DATA',
            gameType,
            location,
            badgeImageUrl,
            playersOnline,
            playersOnMap,
            wikiPageUrl
        });
    } else {
        return console.warn('Current game is not supported! Data not sent.')
    }
}

/**
 * Starts the data collection at regular intervals
 */
function startCollecting() {
    if (!intervalId) {
        intervalId = setInterval(sendAllData, 15000);
    }
}

/**
 * Stops the data collection
 */
function stopCollecting() {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
}

// Listens for messages to toggle the extension's data collection
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'TOGGLE_EXTENSION') {
        if (message.enabled) {
            startCollecting();
        } else {
            stopCollecting();
        }
    }
});

// Initializes the extension based on the stored enabled state
chrome.storage.sync.get('extensionEnabled', function (data) {
    if (data.extensionEnabled !== false) {
        startCollecting();
    }
});