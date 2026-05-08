import re

def extract_features(text):
    features = []
    
    # Detect URLs
    url_pattern = re.compile(r'https?://[^\s]+')
    urls = url_pattern.findall(text)
    if urls:
        features.append(f"Suspicious URL(s) detected: {', '.join(urls)}")

    # Detect urgent keywords
    urgent_keywords = ['urgent', 'immediate', 'action required', 'alert', 'suspended', 'locked']
    found_urgent = [kw for kw in urgent_keywords if kw in text.lower()]
    if found_urgent:
        features.append(f"Urgent wording found: {', '.join(found_urgent)}")

    # Detect financial terms
    financial_terms = ['bank', 'account', 'invoice', 'payment', 'transfer', 'crypto', 'wallet', 'purchase', '$']
    found_financial = [term for term in financial_terms if term in text.lower()]
    if found_financial:
        features.append(f"Financial keyword(s) found: {', '.join(found_financial)}")

    # Detect fake login phrases
    login_phrases = ['verify', 'confirm your identity', 'update your password', 'click here to', 'login', 'reset']
    found_login = [phrase for phrase in login_phrases if phrase in text.lower()]
    if found_login:
        features.append(f"Suspicious action request found: {', '.join(found_login)}")

    # Detect excessive punctuation
    if text.count('!') > 2 or text.count('?') > 2:
        features.append("Excessive punctuation detected (! or ?).")
        
    return features
