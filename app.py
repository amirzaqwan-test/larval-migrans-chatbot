from flask import Flask, render_template, request
import json

app = Flask(__name__)

# =========================
# GLOBAL MODE
# =========================
current_mode = "learning"

# =========================
# LOAD Q&A DATA
# =========================
with open("qa.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# =========================
# CHATBOT LOGIC
# =========================
def get_answer(user_input):
    user_input = user_input.lower()

    for item in qa_data:
        for q in item["question"]:
            if q in user_input:
                if current_mode == "learning":
                    answer = item.get("learning", "No learning answer available.")
                    tag = "\n\n📘 Answer based on lecture slides (Learning Mode)."
                else:
                    answer = item.get("exam", "No exam answer available.")
                    tag = "\n\n📝 Exam-oriented answer based on lecture slides."

                return answer + tag

    return "Sorry, I cannot find the answer in the lecture slides."

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form["user_input"]
    reply = get_answer(user_input)
    return reply

@app.route("/mode", methods=["POST"])
def mode():
    global current_mode
    current_mode = request.form["mode"]
    return f"Switched to {current_mode.upper()} mode."

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

