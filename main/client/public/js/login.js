document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('loginForm').addEventListener('submit', async function (e) {
        e.preventDefault(); // Prevent form from refreshing the page

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('error-message');

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();
            if (response.ok) {
                alert('Login successful! Redirecting to dashboard...');
                window.location.href = "/landing.html"; // ✅ Redirect to dashboard
            } else {
                errorMessage.textContent = data.error || 'Invalid credentials.';
            }
        } catch (error) {
            console.error('Login error:', error);
            errorMessage.textContent = 'Something went wrong. Try again.';
        }
    });
});
