from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# In-memory storage — no database needed
poll = {
    "question": "What is your favourite programming language?",
    "options": {
        "Python": 0,
        "JavaScript": 0,
        "Java": 0,
        "Go": 0
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/poll', methods=['GET'])
def get_poll():
    return jsonify({
        "question": poll["question"],
        "options": list(poll["options"].keys())
    })

@app.route('/poll/vote', methods=['POST'])
def vote():
    data = request.get_json()
    option = data.get("option")

    if not option:
        return jsonify({"error": "option is required"}), 400

    if option not in poll["options"]:
        return jsonify({"error": f"'{option}' is not a valid option"}), 400

    poll["options"][option] += 1
    return jsonify({"message": f"Vote for '{option}' recorded!"}), 200

@app.route('/poll/results', methods=['GET'])
def results():
    total = sum(poll["options"].values())
    return jsonify({
        "question": poll["question"],
        "results": poll["options"],
        "total_votes": total
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
