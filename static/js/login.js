const loginForm = document.getElementById('loginForm'); 
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const errorMessage = document.getElementById('errorMessage'); 

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault(); 

    const username = usernameInput.value;
    const password = passwordInput.value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, password: password })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.message); 
        }

        // Handle successful login (e.g., redirect to profile page)
        window.location.href = '/profile'; 

    } catch (error) {
        errorMessage.textContent = error.message; 
    }
});