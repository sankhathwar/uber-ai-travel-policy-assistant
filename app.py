from flask import Flask, render_template, request, jsonify

from src.agent import agent

app = Flask(__name__)

import traceback
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("question", "")
    if not question:
        return jsonify(
         {
            "success": False,
            "answer": "Please enter a question."
            }
    )

    try:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question,
                    }
                ]
            }
        )

        answer = response["messages"][-1].content

        # Gemini may sometimes return a list instead of plain text
        if isinstance(answer, list):
            answer = "\n".join(
                item.get("text", "")
                for item in answer
                if isinstance(item, dict)
            )

        return jsonify(
            {
                "success": True,
                "answer": answer,
            }
        )

    except Exception:

        traceback.print_exc()

        return jsonify(
        {
            "success": False,
            "answer": traceback.format_exc(),
        }
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )