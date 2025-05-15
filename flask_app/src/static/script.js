document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    function addMessage(text, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
    }

    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === "") return;

        addMessage(messageText, "user");
        userInput.value = ""; // Clear input field
        userInput.disabled = true;
        sendButton.disabled = true;

        try {
            // Adiciona uma mensagem de "Bot está digitando..."
            const typingMessageDiv = document.createElement("div");
            typingMessageDiv.classList.add("message", "bot-message", "typing-indicator");
            typingMessageDiv.textContent = "Bot está digitando...";
            chatMessages.appendChild(typingMessageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: messageText }),
            });

            // Remove a mensagem de "Bot está digitando..."
            chatMessages.removeChild(typingMessageDiv);

            if (!response.ok) {
                const errorData = await response.json().catch(() => null); // Tenta pegar o JSON do erro
                const errorMessage = errorData && errorData.error ? errorData.error : `Erro HTTP: ${response.status}`;
                addMessage(`Erro ao contatar o servidor: ${errorMessage}`, "bot");
                console.error("Server error:", errorData || response.status);
                return;
            }

            const data = await response.json();
            if (data.reply) {
                addMessage(data.reply, "bot");
            } else if (data.error) {
                addMessage(`Erro do servidor: ${data.error}`, "bot");
            } else {
                addMessage("Resposta inesperada do servidor.", "bot");
            }

        } catch (error) {
            // Remove a mensagem de "Bot está digitando..." em caso de erro de rede
            const typingIndicator = chatMessages.querySelector(".typing-indicator");
            if (typingIndicator) {
                chatMessages.removeChild(typingIndicator);
            }
            addMessage("Não foi possível conectar ao servidor. Verifique sua conexão.", "bot");
            console.error("Fetch error:", error);
        } finally {
            userInput.disabled = false;
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Adiciona uma mensagem inicial do bot
    addMessage("Olá! Como posso te ajudar hoje?", "bot");
    userInput.focus();
});

