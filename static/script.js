const chatBox = document.getElementById("chat-box");
const sendBtn = document.getElementById("send-btn");
const questionInput = document.getElementById("question");


function addMessage(message, sender) {

    const div = document.createElement("div");

    div.className = sender;

    if (sender === "bot") {
        // Convert Markdown-style response into HTML
        div.innerHTML = markdownToHtml(message);
    } else {
        // User messages should remain plain text
        div.innerText = message;
    }

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}


/*
 * Simple Markdown renderer
 *
 * Handles:
 * - **bold**
 * - ### headings
 * - ## headings
 * - # headings
 * - bullet points
 * - numbered lists
 * - line breaks
 */

function markdownToHtml(text) {

    let html = text;

    // Escape HTML first for safety
    html = html
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");


    // Bold: **text**
    html = html.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );


    // Headings
    html = html.replace(
        /^### (.*)$/gm,
        "<h4>$1</h4>"
    );

    html = html.replace(
        /^## (.*)$/gm,
        "<h3>$1</h3>"
    );

    html = html.replace(
        /^# (.*)$/gm,
        "<h2>$1</h2>"
    );


    // Bullet points
    html = html.replace(
        /^\s*\*\s+(.*)$/gm,
        "<li>$1</li>"
    );

    html = html.replace(
        /^\s*-\s+(.*)$/gm,
        "<li>$1</li>"
    );


    // Numbered lists
    html = html.replace(
        /^\s*\d+\.\s+(.*)$/gm,
        "<li>$1</li>"
    );


    // Convert consecutive <li> elements into a list
    html = html.replace(
        /((?:<li>.*?<\/li>\s*)+)/gs,
        "<ul>$1</ul>"
    );


    // Horizontal rule
    html = html.replace(
        /^---$/gm,
        "<hr>"
    );


    // Convert remaining line breaks
    html = html.replace(
        /\n/g,
        "<br>"
    );


    return html;
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
                question: question
            })
        });


        const data = await response.json();


        // Remove "Thinking..."
        chatBox.removeChild(chatBox.lastChild);


        if (data.success) {

            addMessage(data.answer, "bot");

        } else {

            addMessage(data.answer, "bot");

        }


    } catch (error) {

        chatBox.removeChild(chatBox.lastChild);

        addMessage(
            "Error connecting to server.",
            "bot"
        );

        console.error(error);
    }


    sendBtn.disabled = false;

    questionInput.focus();
}


sendBtn.addEventListener(
    "click",
    sendQuestion
);


questionInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendQuestion();
        }
    }
);