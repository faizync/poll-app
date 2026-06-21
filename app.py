from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

POLLS = {
    "1": {
        "question": "What is your favourite programming language?",
        "category": "Technology",
        "options": {"Python": 0, "JavaScript": 0, "Go": 0, "Rust": 0},
    },
    "2": {
        "question": "Which code editor do you use most?",
        "category": "Technology",
        "options": {"VS Code": 0, "Vim / Neovim": 0, "JetBrains IDE": 0, "Sublime Text": 0},
    },
    "3": {
        "question": "Preferred cloud provider?",
        "category": "Technology",
        "options": {"AWS": 0, "Google Cloud": 0, "Azure": 0, "I self-host": 0},
    },
    "4": {
        "question": "What is your favourite cuisine?",
        "category": "Food",
        "options": {"Italian": 0, "Japanese": 0, "Mexican": 0, "Indian": 0},
    },
    "5": {
        "question": "Coffee or tea?",
        "category": "Food",
        "options": {"Coffee": 0, "Tea": 0, "Both": 0, "Neither": 0},
    },
    "6": {
        "question": "What do you usually have for breakfast?",
        "category": "Food",
        "options": {"Eggs & Bacon": 0, "Cereal": 0, "Pancakes": 0, "I skip breakfast": 0},
    },
    "7": {
        "question": "Favourite movie genre?",
        "category": "Entertainment",
        "options": {"Action": 0, "Sci-Fi": 0, "Comedy": 0, "Drama": 0},
    },
    "8": {
        "question": "Which streaming service do you use most?",
        "category": "Entertainment",
        "options": {"Netflix": 0, "YouTube": 0, "Disney+": 0, "Amazon Prime": 0},
    },
    "9": {
        "question": "Favourite gaming platform?",
        "category": "Entertainment",
        "options": {"PC": 0, "PlayStation": 0, "Xbox": 0, "Mobile": 0},
    },
    "10": {
        "question": "Favourite sport to watch?",
        "category": "Sports",
        "options": {"Football": 0, "Basketball": 0, "Tennis": 0, "Formula 1": 0},
    },
    "11": {
        "question": "How often do you exercise?",
        "category": "Sports",
        "options": {"Daily": 0, "A few times a week": 0, "Rarely": 0, "Never": 0},
    },
    "12": {
        "question": "Are you a morning or night person?",
        "category": "Lifestyle",
        "options": {"Morning person": 0, "Night owl": 0, "Depends on the day": 0},
    },
    "13": {
        "question": "What is your preferred work style?",
        "category": "Lifestyle",
        "options": {"Fully remote": 0, "Hybrid": 0, "In-office": 0},
    },
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/polls")
def list_polls():
    category = request.args.get("category", "").strip()
    polls_list = []
    for poll_id, poll in POLLS.items():
        if category and poll["category"].lower() != category.lower():
            continue
        polls_list.append({
            "id": poll_id,
            "question": poll["question"],
            "category": poll["category"],
            "total_votes": sum(poll["options"].values()),
            "option_count": len(poll["options"]),
        })
    return jsonify({"polls": polls_list})


@app.route("/api/categories")
def list_categories():
    categories = sorted(set(p["category"] for p in POLLS.values()))
    return jsonify({"categories": categories})


@app.route("/api/polls/<poll_id>")
def get_poll(poll_id):
    poll = POLLS.get(poll_id)
    if not poll:
        return jsonify({"error": "Poll not found"}), 404
    return jsonify({
        "id": poll_id,
        "question": poll["question"],
        "category": poll["category"],
        "options": list(poll["options"].keys()),
    })


@app.route("/api/polls/<poll_id>/vote", methods=["POST"])
def vote(poll_id):
    poll = POLLS.get(poll_id)
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    data = request.get_json()
    option = data.get("option") if data else None

    if not option:
        return jsonify({"error": "option is required"}), 400

    if option not in poll["options"]:
        return jsonify({"error": f"'{option}' is not a valid option"}), 400

    poll["options"][option] += 1
    return jsonify({"message": "Vote recorded!"}), 200


@app.route("/api/polls/<poll_id>/results")
def results(poll_id):
    poll = POLLS.get(poll_id)
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    total = sum(poll["options"].values())
    return jsonify({
        "question": poll["question"],
        "results": poll["options"],
        "total_votes": total,
    })


@app.route("/api/polls/<poll_id>/reset", methods=["POST"])
def reset_poll(poll_id):
    poll = POLLS.get(poll_id)
    if not poll:
        return jsonify({"error": "Poll not found"}), 404

    for key in poll["options"]:
        poll["options"][key] = 0
    return jsonify({"message": "Poll has been reset."}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
