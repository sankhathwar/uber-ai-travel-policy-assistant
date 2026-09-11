import os
import uuid
import traceback

from flask import Flask, render_template, request, jsonify, session

from src.agent import agent


app = Flask(__name__)

# Secret key is required for Flask sessions
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "dev-secret-key"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({
            "success": False,
            "answer": "Please enter a question."
        })

    try:

        # -------------------------------------------------
        # Get or create a conversation ID
        # -------------------------------------------------

        if "conversation_id" not in session:

            session["conversation_id"] = str(uuid.uuid4())

        conversation_id = session["conversation_id"]


        # -------------------------------------------------
        # Send question to LangGraph
        # -------------------------------------------------

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question,
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": conversation_id
                }
            }
        )


        # -------------------------------------------------
        # Get final assistant response
        # -------------------------------------------------

        answer = response["messages"][-1].content


        # Handle Gemini response format if required
        if isinstance(answer, list):

            answer = "\n".join(
                item.get("text", "")
                for item in answer
                if isinstance(item, dict)
            )


        return jsonify({
            "success": True,
            "answer": answer
        })


    except Exception:

        traceback.print_exc()

        return jsonify({
            "success": False,
            "answer": traceback.format_exc()
        })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )