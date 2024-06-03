chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === '2KKI_DATA') {
        fetch('http://localhost:3000/receive_from_2kki', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: message.data }),
        })
            .then(response => response.json())
            .then(data => console.log('Success:', data))
            .catch(error => console.error('Error:', error));
    }
});