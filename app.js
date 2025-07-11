function handleKey(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // evita salto de línea y GET innecesario
        sendQuestion();
    }
}

async function sendQuestion() {
    const question = document.getElementById("question").value.trim();
    const responseBox = document.getElementById("response");

    if (!question) {
        responseBox.innerHTML = "⚠️ <b>Error:</b> Escribe una pregunta primero.";
        return;
    }

    responseBox.innerHTML = "⏳ <i>Consultando al agente...</i>";

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question }),
        });

        const data = await res.json();

        if (data.success) {
            responseBox.innerHTML = `✅ <b>Respuesta:</b>\n${data.response}`;
        } else {
            responseBox.innerHTML = `❌ <b>Error:</b> ${data.error}`;
        }
    } catch (error) {
        responseBox.innerHTML = "🔥 <b>Error de conexión con el backend.</b>";
    }
}
