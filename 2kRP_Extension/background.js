const SERVER_URL = 'http://localhost:7789';

async function checkServerStatus(url) {
    try {
        const response = await fetch(url);
        return response.ok;
    } catch (error) {
        console.error('Error checking server status:', error);
        return false;
    }
}

async function sendDataToServer(data) {
    try {
        const response = await fetch(`${SERVER_URL}/receive_from_2kki`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Failed to send data to server');
        }
        console.log('Data sent successfully');
    } catch (error) {
        console.error('Error:', error);
    }
}

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.type === '2KKI_DATA') {
        const isServerActive = await checkServerStatus(`${SERVER_URL}/status`);

        if (isServerActive) {
            await sendDataToServer({
                gameType: message.gameType,
                location: message.location,
                badgeImageUrl: message.badgeImageUrl,
                playersOnline: message.playersOnline,
                playersOnMap: message.playersOnMap,
                wikiPageUrl: message.wikiPageUrl
            });
        } else {
            console.error('Server is not active');
        }
    }
});
