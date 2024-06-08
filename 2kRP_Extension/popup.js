// popup.js
const SERVER_URL = 'http://localhost:7789/status';

async function checkServerStatus(url) {
    try {
        const response = await fetch(url);
        return response.ok;
    } catch (error) {
        console.error('Error checking server status:', error);
        return false;
    }
}

function updateServerStatus(isServerActive) {
    const serverStatus = document.getElementById('server-status');
    if (isServerActive) {
        serverStatus.textContent = 'Server is up and running!';
        serverStatus.style.color = 'green';
    } else {
        serverStatus.textContent = 'Server is inactive! Be sure the receiver app is running.';
        serverStatus.style.color = 'red';
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    const toggleSwitch = document.getElementById('toggle-switch');

    // Restore the switch state from storage
    chrome.storage.sync.get('extensionEnabled', function (data) {
        toggleSwitch.checked = data.extensionEnabled !== false;
    });

    // Check server status
    const isServerActive = await checkServerStatus(SERVER_URL);
    updateServerStatus(isServerActive);

    toggleSwitch.addEventListener('change', function () {
        const isEnabled = toggleSwitch.checked;
        chrome.storage.sync.set({ extensionEnabled: isEnabled });

        // Send message to content script to start or stop the collection
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {
                type: 'TOGGLE_EXTENSION',
                enabled: isEnabled,
            });
        });
    });
});