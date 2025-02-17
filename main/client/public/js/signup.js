document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('signupForm').addEventListener('submit', async function (e) {
        e.preventDefault(); // ✅ Prevent page reload

        const username = document.querySelector('input[placeholder="Full Name"]').value;
        const email = document.querySelector('input[placeholder="Email Address"]').value;
        const password = document.querySelector('input[placeholder="Password"]').value;

        if (!username || !email || !password) {
            alert("Please fill out all fields.");
            return;
        }

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();
            if (response.ok) {
                alert('Signup successful! Redirecting to login...');
                window.location.href = "/login.html"; // ✅ Redirect to login
            } else {
                alert(data.error || "Signup failed.");
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong.');
        }
    });
});
