
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from utils import recommend_products, ask_openai, analyze_uploaded_image

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Store recommendations temporarily in memory
recommendation_cache = []



# 🔹 Serve Frontend
@app.route("/")
def serve_index():
    return render_template("index.html")

@app.route("/recommend", methods=["GET"])
def get_recommendations():
    global recommendation_cache  # Use a cache to store last results
    query = request.args.get("query", "").strip()

    if not query:
        return jsonify({"error": "No query provided"}), 400

    recs = recommend_products(query)
    recommendation_cache = recs  # Store recommendations

    if recs:
        return jsonify(recs)
    else:
        print("⚠️ No matching products found.")
        return jsonify({"message": "No matching products found"}), 404


# 🔹 API: Ask AI Skincare Questions
@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = ask_openai(question)
    return jsonify(response)

# 🔹 API: Analyze Image for Ingredients
@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    response = analyze_uploaded_image(request.files["image"])
    return jsonify(response)

# 🔹 Run Flask App
if __name__ == "__main__":
    app.run(debug=True, port=5001)
