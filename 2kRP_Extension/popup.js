function checkServerStatus(url) {
    return fetch(url)
        .then(response => response.ok)
        .catch(error => {
            console.error('Error checking server status:', error);
            return false;
        });
}

document.addEventListener('DOMContentLoaded', function () {
    const toggleSwitch = document.getElementById('toggle-switch');
    const serverStatus = document.getElementById('server-status');

    // Restore the switch state from storage
    chrome.storage.sync.get('extensionEnabled', function (data) {
        toggleSwitch.checked = data.extensionEnabled !== false;
    });

    // Check server status
    checkServerStatus('http://localhost:3000/status').then(isServerActive => {
        if (isServerActive) {
            serverStatus.textContent = 'Server is up and running!';
            serverStatus.style.color = 'green';
        } else {
            serverStatus.textContent =
                'Server is inactive! Be sure the receiver app is running.';
            serverStatus.style.color = 'red';
        }
    });

    toggleSwitch.addEventListener('change', function () {
        const isEnabled = toggleSwitch.checked;
        chrome.storage.sync.set({ extensionEnabled: isEnabled });

        // Send message to content script to start or stop the collection
        chrome.tabs.query(
            { active: true, currentWindow: true },
            function (tabs) {
                chrome.tabs.sendMessage(tabs[0].id, {
                    type: 'TOGGLE_EXTENSION',
                    enabled: isEnabled,
                });
            }
        );
    });
});
