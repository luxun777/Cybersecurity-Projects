import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import joblib
import os
import json

def train():
    print("Loading data...")
    # Handle running from root or model/ dir
    data_path = 'data/phishing_dataset.csv'
    if not os.path.exists(data_path):
        data_path = '../data/phishing_dataset.csv'
        
    df = pd.read_csv(data_path)
    
    X = df['text']
    y = df['label']

    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_vec = vectorizer.fit_transform(X)

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

    print("Training model...")
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred).tolist()

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    
    # Save metrics for the dashboard
    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "confusion_matrix": cm
    }

    os.makedirs('model', exist_ok=True)
    with open('model/metrics.json', 'w') as f:
        json.dump(metrics, f)

    print("Saving model and vectorizer...")
    joblib.dump(model, 'model/model.pkl')
    joblib.dump(vectorizer, 'model/vectorizer.pkl')
    print("Training complete!")

if __name__ == "__main__":
    train()
