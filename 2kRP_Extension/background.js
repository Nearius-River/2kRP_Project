function checkServerStatus(url) {
    return fetch(url)
        .then(response => response.ok)
        .catch(error => {
            console.error('Error checking server status:', error);
            return false;
        });
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === '2KKI_DATA') {
        checkServerStatus('http://localhost:7789/status')
            .then(isServerActive => {
                if (isServerActive) {
                    return fetch('http://localhost:7789/receive_from_2kki', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            location: message.location,
                            badgeImageUrl: message.badgeImageUrl,
                            playersOnline: message.playersOnline,
                            playersOnMap: message.playersOnMap,
                        }),
                    });
                } else {
                    throw new Error('Server is not active');
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to send data to server');
                }
                console.log('Data sent successfully');
            })
            .catch(error => console.error('Error:', error));
    }
});