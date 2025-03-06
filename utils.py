import os
import openai
import pytesseract
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load environment variables
load_dotenv()

# Configure Tesseract OCR path
# Check if the OS is Windows
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH 

# Load the dataset
try:
    df = pd.read_csv("./resources/cosmetics.csv")
    df["text"] = df["Name"].fillna("") + " " + df["Ingredients"].fillna("")
    
    # Fit TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["text"])
    
    print("✅ Dataset loaded successfully.")
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    df = None

# 🔹 Product Recommendation System
def recommend_products(query, top_n=5):
    """Returns top skincare product recommendations based on user query."""
    if df is None:
        return []

    query_vec = vectorizer.transform([query])
    sim_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = sim_scores.argsort()[-top_n:][::-1]
    return df.iloc[top_indices][["Name", "Ingredients"]].to_dict(orient="records")

# 🔹 OpenAI API for Skincare Q&A
openai_api_key = os.getenv("OPENAI_API_KEY")  

client = openai.OpenAI(api_key=openai_api_key) if openai_api_key else None

def ask_openai(question):
    if not client:
        return {"error": "OpenAI API key is missing"}
    try:
        print(f"User Question: {question}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a skincare expert."},
                {"role": "user", "content": question},
            ],
        )
        return {"answer": response.choices[0].message.content if response.choices else "AI did not return an answer."}
    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return {"error": str(e)}


def analyze_uploaded_image(image):
    image_path = "uploaded_image.png"
    image.save(image_path)

    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        os.remove(image_path)  # Clean up after extraction
        print(f"Extracted Text: {text}")
        return {"analysis": text.strip()}
    except Exception as e:
        return {"error": str(e)}
