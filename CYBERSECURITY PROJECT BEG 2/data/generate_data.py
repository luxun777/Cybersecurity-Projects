import csv
import random
import os

# A quick script to generate a basic synthetic phishing dataset
safe_templates = [
    "Hi {name}, just a reminder that our weekly meeting is at {time} tomorrow. Please review the attached agenda. Best, {sender}.",
    "Can you please send me the latest quarterly report when you have a chance? Thanks!",
    "Your Amazon order has been shipped. Track your package here: https://amazon.com/track/{id}.",
    "Let's grab lunch later today. Are you free around {time}?",
    "The project deadline has been extended to next {day}. Please adjust your schedules accordingly.",
    "I've reviewed your pull request and left some comments. Please address them before we merge.",
    "Happy birthday! Hope you have a great day.",
    "Please find the attached invoice for your records.",
    "Are we still on for the call at {time}?",
    "Thanks for reaching out. I'll get back to you as soon as possible.",
    "Looking forward to the conference next {day}.",
    "Can we reschedule our meeting to {day} at {time}?",
    "The server maintenance will happen this {day}. Please save your work.",
    "Here are the meeting notes from yesterday's sync."
]

phishing_templates = [
    "URGENT: Your bank account will be suspended in 24 hours. Verify your information immediately at http://secure-update-bank.com/login.",
    "Dear Customer, your Apple ID has been locked for security reasons. Click here to unlock: http://apple-support-verify.com.",
    "You have won a $1000 Walmart gift card! Click the link to claim your prize now. Limited time offer!",
    "Please review the attached invoice for your recent purchase of $599.99. If you did not authorize this, contact us immediately.",
    "Update your password immediately! Your account has been compromised. Visit http://reset-password-now.com to secure your account.",
    "We noticed suspicious login attempts on your account. Please confirm your identity by clicking this link.",
    "Act now! Exclusive investment opportunity with 500% returns in 1 week. Send funds to the provided crypto wallet.",
    "Your Microsoft 365 password expires today. Retain your current password by verifying here: http://login-microsoft-secure.com",
    "URGENT ACTION REQUIRED: Verify your email address to prevent account deletion.",
    "You have an unread secure message. Click here to read it: http://secure-message-portal.com",
    "We have received a request to terminate your account. To cancel this request, click the link below.",
    "Your package could not be delivered due to an unpaid shipping fee. Pay $1.99 here: http://post-office-pay.com",
    "Congratulations! You've been selected for a free iPhone 15. Claim your prize here: http://free-iphone-winner.com",
    "Invoice #49281 attached. Please pay immediately to avoid late fees."
]

names = ["John", "Sarah", "Mike", "Emily", "David", "Jessica"]
times = ["10 AM", "1 PM", "3:30 PM", "9 AM", "12 PM"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
senders = ["Alice", "Bob", "Charlie", "Diana"]
ids = ["12345", "98765", "A1B2C", "X9Y8Z"]

data = []

# Generate 200 safe emails
for _ in range(200):
    template = random.choice(safe_templates)
    text = template.format(name=random.choice(names), time=random.choice(times), day=random.choice(days), sender=random.choice(senders), id=random.choice(ids))
    data.append({'text': text, 'label': 0})

# Generate 200 phishing emails
for _ in range(200):
    template = random.choice(phishing_templates)
    text = template.format(name=random.choice(names), time=random.choice(times), day=random.choice(days), sender=random.choice(senders), id=random.choice(ids))
    data.append({'text': text, 'label': 1})

# Shuffle
random.shuffle(data)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Save
with open("data/phishing_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "label"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("Generated synthetic dataset 'data/phishing_dataset.csv' with", len(data), "samples.")
