import string
import secrets
def evaluate_password(password):
    """
    Evaluates password strength based on length and complexity rules.
    Returns a dictionary with score, strength level, and suggestions.
    """
    score = 0
    suggestions = []
    
    # 1. Length Validation
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Increase password length to at least 8 characters.")
        
    # 2. Uppercase Validation
    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")
        
    # 3. Lowercase Validation
    if any(char.islower() for char in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")
        
    # 4. Number Validation
    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append("Add numbers.")
        
    # 5. Special Character Validation
    special_chars = set(string.punctuation)
    if any(char in special_chars for char in password):
        score += 1
    else:
        suggestions.append("Add special characters (e.g., !, @, #, $, %).")
        
    # Strength Classification
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"
        
    return {
        "score": score,
        "strength": strength,
        "suggestions": suggestions
    }
def generate_strong_password(length=16):
    """
    Generates a secure random password that meets all complexity requirements.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        # Ensure it meets all criteria
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        if has_lower and has_upper and has_digit and has_special:
            return password
