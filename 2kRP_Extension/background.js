chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === '2KKI_DATA') {
        fetch('http://localhost:3000/receive_from_2kki', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ location: message.location, badgeImageUrl: message.badgeImageUrl, playersOnline: message.playersOnline, playersOnMap: message.playersOnMap }),
        })
            .catch(error => console.error('Error:', error));
    }
});