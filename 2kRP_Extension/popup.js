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
        serverStatus.style.color = '#4caf50';
    } else {
        serverStatus.textContent = 'Server is not running!';
        serverStatus.style.color = '#e91e63';
        serverStatus.style.fontWeight = 'bold';
    }
}

document.addEventListener('DOMContentLoaded', async function () {
    const toggleSwitch = document.getElementById('toggle-switch');

    // Restore the switch state from storage
    chrome.storage.sync.get('extensionEnabled', function (data) {
        toggleSwitch.checked = data.extensionEnabled !== false;
    });

    // Popup navigation buttons behavior
    document.getElementById('settings-button').addEventListener('click', function() {
        document.getElementById('popup-content').style.display = 'none';
        document.getElementById('settings-content').style.display = 'block';
    });
    
    document.getElementById('back-button').addEventListener('click', function() {
        document.getElementById('settings-content').style.display = 'none';
        document.getElementById('popup-content').style.display = 'block';
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