"""
Mini Grammar Correction Model & JFLEG Dataset Analysis
"""
import pandas as pd
from sklearn.model_selection import train_test_split

# Load JFLEG train.csv
DATA_PATH = "jfleg-dataset/versions/1/train.csv"
df = pd.read_csv(DATA_PATH)

# Show basic info
print("Rows:", len(df))
print("Columns:", df.columns)
print(df.head())

# Example: Show a few original/corrected pairs
for i in range(3):
    print(f"Original: {df.iloc[i,0]}")
    print(f"Corrected: {df.iloc[i,1]}")
    print()

# Prepare data for a simple ML model (e.g., TF-IDF + Ridge regression for demonstration)
# For real grammar correction, use seq2seq models (T5, BART, etc.)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge

# Use only first 1000 samples for quick demo
X = df.iloc[:1000,0].astype(str)
Y = df.iloc[:1000,1].astype(str)

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)
Y_vec = vectorizer.fit_transform(Y)

# Split data
X_train, X_test, Y_train, Y_test = train_test_split(X_vec, Y_vec, test_size=0.2, random_state=42)

# Train a Ridge regression model (for demonstration, not true grammar correction)
model = Ridge()
model.fit(X_train, Y_train.toarray())

print("Demo model trained. This is NOT a true grammar correction model, but shows how to start.")

# For real grammar correction, use Hugging Face Transformers and fine-tune a seq2seq model.
