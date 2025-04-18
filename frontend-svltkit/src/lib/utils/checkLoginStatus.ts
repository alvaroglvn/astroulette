export async function checkLoginStatus() {
    try {
        const response = await fetch('user/me', {
            credentials: 'include'
        });
        if (response.ok) {
            return true;
        }
    } catch (e) {
        console.error(e);
    }
    return false;
}