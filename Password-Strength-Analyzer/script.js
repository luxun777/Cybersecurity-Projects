document.addEventListener('DOMContentLoaded', () => {
    const passwordInput = document.getElementById('password-input');
    const toggleVisibilityBtn = document.getElementById('toggle-visibility');
    const visibilityIcon = document.getElementById('visibility-icon');
    const copyBtn = document.getElementById('copy-btn');
    const generateBtn = document.getElementById('generate-btn');
    
    const progressBar = document.getElementById('progress-bar');
    const strengthText = document.getElementById('strength-text');
    const scoreText = document.getElementById('score-text');
    const suggestionsList = document.getElementById('suggestions-list');
    const toast = document.getElementById('toast');
    let debounceTimer;
    // Toggle Password Visibility
    toggleVisibilityBtn.addEventListener('click', () => {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            visibilityIcon.classList.remove('fa-eye');
            visibilityIcon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            visibilityIcon.classList.remove('fa-eye-slash');
            visibilityIcon.classList.add('fa-eye');
        }
    });
    // Copy Password
    copyBtn.addEventListener('click', async () => {
        if (!passwordInput.value) return;
        
        try {
            await navigator.clipboard.writeText(passwordInput.value);
            showToast('Password copied to clipboard!');
        } catch (err) {
            console.error('Failed to copy text: ', err);
            // Fallback for older browsers
            passwordInput.select();
            document.execCommand('copy');
            showToast('Password copied to clipboard!');
        }
    });
    // Generate Strong Password
    generateBtn.addEventListener('click', async () => {
        // Visual feedback
        generateBtn.disabled = true;
        const originalContent = generateBtn.innerHTML;
        generateBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating...';
        
        try {
            const response = await fetch('/generate');
            const data = await response.json();
            
            passwordInput.value = data.password;
            
            // Trigger input event to re-evaluate the new password
            passwordInput.dispatchEvent(new Event('input'));
            
        } catch (error) {
            console.error('Error generating password:', error);
            showToast('Error generating password');
        } finally {
            // Restore button state
            generateBtn.disabled = false;
            generateBtn.innerHTML = originalContent;
        }
    });
    // Real-time Validation with Debounce
    passwordInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        
        const password = passwordInput.value;
        
        if (!password) {
            updateUI({
                score: 0,
                strength: "Empty",
                suggestions: ["Please enter a password."]
            });
            return;
        }
        // Delay the API call slightly to avoid spamming the server while typing fast
        debounceTimer = setTimeout(async () => {
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ password })
                });
                
                const result = await response.json();
                updateUI(result);
            } catch (error) {
                console.error('Error analyzing password:', error);
            }
        }, 150);
    });
    // Update the UI dynamically based on backend analysis
    function updateUI(result) {
        // Update texts
        scoreText.textContent = result.score;
        strengthText.textContent = result.strength;
        
        // Update Progress Bar
        const percentage = (result.score / 5) * 100;
        progressBar.style.width = `${percentage}%`;
        
        // Reset dynamic styles
        progressBar.style.backgroundColor = 'var(--color-empty)';
        progressBar.style.boxShadow = 'none';
        strengthText.style.color = 'var(--text-main)';
        // Apply strength-specific styles
        if (result.strength === "Weak") {
            progressBar.style.backgroundColor = 'var(--color-weak)';
            progressBar.style.boxShadow = '0 0 10px var(--color-weak)';
            strengthText.style.color = 'var(--color-weak)';
        } else if (result.strength === "Medium") {
            progressBar.style.backgroundColor = 'var(--color-medium)';
            progressBar.style.boxShadow = '0 0 10px var(--color-medium)';
            strengthText.style.color = 'var(--color-medium)';
        } else if (result.strength === "Strong") {
            progressBar.style.backgroundColor = 'var(--color-strong)';
            progressBar.style.boxShadow = '0 0 10px var(--color-strong)';
            strengthText.style.color = 'var(--color-strong)';
        }
        // Update Suggestions List
        suggestionsList.innerHTML = '';
        if (result.suggestions && result.suggestions.length > 0) {
            result.suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.textContent = suggestion;
                suggestionsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = "Your password looks great!";
            li.style.color = 'var(--color-strong)';
            suggestionsList.appendChild(li);
        }
    }
    // Utility function to show toast notifications
    function showToast(message) {
        toast.textContent = message;
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});
