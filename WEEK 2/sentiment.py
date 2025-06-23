import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK data
nltk.download('vader_lexicon')

# Load the dataset
df = pd.read_csv("D:/python data/reviews.csv")

# Rename columns if necessary (you can skip this if your columns are already clean)
df.columns = [col.strip().lower() for col in df.columns]  # Make all column names lowercase

# Check if the correct column exists
if 'review' not in df.columns:
    raise ValueError("The dataset must have a 'review' column.")

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Apply sentiment analysis to each review
df['compound_score'] = df['review'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
df['sentiment'] = df['compound_score'].apply(
    lambda score: 'positive' if score > 0.05 else 'negative' if score < -0.05 else 'neutral'
)

# Output sentiment counts
print("Sentiment distribution:\n", df['sentiment'].value_counts())

# Plot the sentiment distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='sentiment', order=['positive', 'neutral', 'negative'], palette='coolwarm')
plt.title('Sentiment Analysis using VADER')
plt.xlabel('Sentiment')
plt.ylabel('Number of Reviews')
plt.tight_layout()
plt.show()
