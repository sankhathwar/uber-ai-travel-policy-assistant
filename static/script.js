const chatBox = document.getElementById("chat-box");
const sendBtn = document.getElementById("send-btn");
const questionInput = document.getElementById("question");

function addMessage(message, sender) {
    const div = document.createElement("div");
    div.className = sender;
    div.innerText = message;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendQuestion() {
    const question = questionInput.value.trim();

    if (question === "") {
        return;
    }

    addMessage(question, "user");

    questionInput.value = "";

    sendBtn.disabled = true;

    addMessage("Thinking...", "bot");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question      // <-- FIXED HERE
            })
        });

        const data = await response.json();

        chatBox.removeChild(chatBox.lastChild);

        addMessage(data.answer, "bot");

    } catch (error) {

        chatBox.removeChild(chatBox.lastChild);

        addMessage("Error connecting to server.", "bot");

        console.error(error);

    }

    sendBtn.disabled = false;

    questionInput.focus();
}

sendBtn.addEventListener("click", sendQuestion);

questionInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendQuestion();
    }
});