let intervalId = null;

function getLocation() {
    const spanElement = document.getElementById('locationText');
    if (spanElement) {
        const linkElement = locationText.querySelector('a');
        if (linkElement) {
            const location = linkElement.innerText;
            return location;
        }
    }

    return null;
}

function sendAllData() {
    const location = getLocation();

    const data = { location: location };

    chrome.runtime.sendMessage({ type: '2KKI_DATA', data });
}

function startCollecting() {
    if (!intervalId) {
        intervalId = setInterval(sendAllData, 2000);
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