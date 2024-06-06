export function checkServerStatus(url) {
    return fetch(url)
        .then(response => response.ok)
        .catch(error => {
            console.error('Error checking server status:', error);
            return false;
        });
}