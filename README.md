# Password Strength Analyzer 🛡️
A professional, modern, and interactive web application to evaluate password strength based on cybersecurity best practices. Built with Python Flask, HTML5, CSS3, and JavaScript, featuring a sleek glassmorphism dark mode UI.
## 🌟 Features
- **Real-Time Validation:** Get instant feedback on your password strength as you type.
- **Detailed Complexity Checks:** Evaluates passwords based on length, uppercase, lowercase, numbers, and special characters.
- **Dynamic Strength Meter:** Visual progress bar indicating Weak (Red), Medium (Orange), or Strong (Green) passwords.
- **Actionable Suggestions:** Provides specific advice on how to improve your password.
- **Secure Password Generator:** Automatically generate strong, cryptographically secure random passwords.
- **Visibility Toggle:** Easily show or hide your password input.
- **One-Click Copy:** Conveniently copy generated passwords to your clipboard.
- **Responsive UI:** Fully mobile-compatible, centered, card-style layout with modern cyber aesthetics.
## 🛠️ Technologies Used
- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Styling:** Custom CSS with CSS Variables, Glassmorphism effects, Flexbox
- **Icons & Typography:** FontAwesome 6, Google Fonts (Inter)
## 📂 Folder Structure
```text
PasswordStrengthAnalyzer/
│
├── app.py                   # Main Flask application file
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
│
├── templates/
│   └── index.html           # Main HTML structure
│
├── static/
│   ├── style.css            # Custom CSS styles
│   └── script.js            # Frontend logic and API integration
│
└── utils/
    └── password_checker.py  # Core backend validation and generation logic
```
## 🚀 Installation & Setup
Follow these steps to run the application locally:
1. **Clone the repository** (or download the files):
   ```bash
   git clone <your-repo-url>
   cd PasswordStrengthAnalyzer
   ```
2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Flask Application**:
   ```bash
   python app.py
   ```
5. **Open your browser**:
   Navigate to `http://127.0.0.1:5000/` to view the app.
## 📸 Screenshots
*(Save your screenshots in a `screenshots/` folder and link them below)*
- `![App Main UI](screenshots/main.png)`
## 🔮 Future Improvements
- Add password entropy calculation.
- Integrate "Have I Been Pwned" API to check if the password has been breached.
- Implement a dark/light mode toggle.
## 👨‍💻 Author
Created as a beginner cybersecurity project.
