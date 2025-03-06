document
  .getElementById("recommendationForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    console.log("🔍 Fetching recommendations...");
    const query = document.getElementById("skinQuery").value;
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (!query) {
      resultsDiv.innerHTML = "<p>Please enter a query!</p>";
      return;
    }

    try {
      const response = await fetch(
        `/recommend?query=${encodeURIComponent(query)}`
      );
      console.log("📡 Server Response:", response);
      if (!response.ok) throw new Error("Error fetching recommendations");

      const recommendations = await response.json();

      if (recommendations.length === 0) {
        resultsDiv.innerHTML =
          "<p>No recommendations found. Try a different query!</p>";
      } else {
        recommendations.forEach((product) => {
          const productDiv = document.createElement("div");
          productDiv.className = "product";
          productDiv.innerHTML = `
                    <h2>${product.Name}</h2>
                    <p><strong>Ingredients:</strong> ${product.Ingredients}</p>
                `;
          resultsDiv.appendChild(productDiv);
        });
      }
    } catch (error) {
      resultsDiv.innerHTML =
        "<p>Could not fetch recommendations. Make sure the server is running.</p>";
      console.error("Error:", error);
    }
  });

// 🔹 Clear recommendations in UI
function clearRecommendations() {
  document.getElementById("results").innerHTML = "";
}

// 🔹 AI Chatbot Function
async function askAI(imageTextData = null) {
  const question = document.getElementById("questionInput").value;
  const chatResponse = document.getElementById("chatResponse");

  console.log("🔍 Calling AI with question:", question);

  if (!question.trim() && !imageTextData) {
    alert("Please enter a question or upload an image.");
    return;
  }

  try {
    let prompt = question;
    if (imageTextData) {
      prompt = `Look at the ingredient list below:\n${imageTextData}\n${question}`;
    }

    const response = await fetch("/ask-ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: prompt }),
    });

    const data = await response.json();
    console.log("💬 AI Response:", data);

    if (data.answer) {
      chatResponse.innerText = data.answer;
    } else {
      chatResponse.innerText = "AI did not return an answer.";
    }
  } catch (error) {
    console.error("Error:", error);
    chatResponse.innerText = "Failed to get an answer. Try again.";
  }
}

// 🔹 Image Upload and AI Call
async function processChat() {
  const imageInput = document.getElementById("imageInput");

  if (imageInput.files.length > 0) {
    console.log("📸 Image detected, extracting text...");
    const imageTextData = await analyzeImage();
    console.log("Extracted Text:", imageTextData);
    await askAI(imageTextData);
  } else {
    await askAI(); // Call AI directly if no image is uploaded
  }
}

// 🔹 Image Upload for Ingredient Extraction
async function analyzeImage() {
  const imageInput = document.getElementById("imageInput");
  const chatResponse = document.getElementById("chatResponse");

  if (imageInput.files.length === 0) {
    console.warn("⚠️ No image selected!");
    return null;
  }

  const formData = new FormData();
  formData.append("image", imageInput.files[0]);

  try {
    const response = await fetch("/analyze-image", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("🔍 Image Analysis Response:", data);
    return data.analysis || null;
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}
