let messages = {
  history: [],
}

async function sendMessage() {
  const userMessage = document.querySelector('.chat-window input').value;
  console.log("User message in sendMessage:", userMessage);

  if (userMessage.trim().length) {
      // Clear input & show user bubble
      document.querySelector(".chat-window input").value = "";
      document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend", `
          <div class="user">
              <p>${userMessage}</p>
          </div>
      `);

      // Show a loader/spinner
      document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend", `
          <div class="loader"></div>
      `);

      try {
          // Make a POST request to the Flask endpoint
          const response = await fetch("/ollama_chat", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify({ prompt: userMessage })
          });

          if (!response.ok) {
              throw new Error("Network response was not ok");
          }

          const data = await response.json();
          const modelResponse = data.content || "No response";

          // Remove the loader
          document.querySelector(".chat-window .chat .loader").remove();

          // Insert the model's response bubble
          document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend", `
              <div class="model">
                  <p>${modelResponse}</p>
              </div>
          `);

          // Optionally store the conversation in messages.history
          messages.history.push({
              role: "user",
              parts: [{ text: userMessage }],
          });
          messages.history.push({
              role: "model",
              parts: [{ text: modelResponse }],
          });

      } catch (error) {
          console.error("Error sending message:", error);
          document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend", `
              <div class="error">
                  <p>The message could not be sent. Please try again.</p>
              </div>
          `);
      }
  }
}
  
  // Chat button (to open chat)
  document.querySelector(".chat-button").addEventListener("click", () => {
    const body = document.querySelector("body");
    const chatWindow = document.querySelector(".chat-window");
    
    if (!body.classList.contains("chat-open")) {
      console.log("Opening chat...");
      body.classList.add("chat-open"); // Add the class to open the chat
      chatWindow.style.display = "flex"; // Ensure visibility
    } else {
      console.log("Chat is already open.");
    }
  });
  
  // Send message button inside the chat window
  document.querySelector(".chat-window .input-area button").addEventListener("click", () => sendMessage());
  
  // Close button inside the chat window
  document.querySelector(".chat-window button.close").addEventListener("click", () => {
    const body = document.querySelector("body");
    const chatWindow = document.querySelector(".chat-window");
    
    console.log("Closing chat...");
    body.classList.remove("chat-open"); // Remove the chat-open class to close the chat
    chatWindow.style.display = "none"; // Hide the chat window
  });
  
  // Option buttons to trigger chat and send messages
  const optionButtons = document.querySelectorAll(".options .option");
  
  optionButtons.forEach(button => {
    button.addEventListener("click", function () {
      const buttonText = this.textContent.trim();
      const chatInput = document.querySelector('.chat-window input');
      const body = document.querySelector("body");
      const chatWindow = document.querySelector(".chat-window");
  
      console.log("Button clicked:", buttonText);
      
      // Set the button's text content to the chat window input
      chatInput.value = buttonText;
      console.log("Value set to input:", chatInput.value);
  
      // Send the message
      sendMessage();
  
      // Ensure the chat box is open
      if (!body.classList.contains("chat-open")) {
        console.log("Reopening chat...");
        body.classList.add("chat-open");
        chatWindow.style.display = "flex"; // Ensure visibility
      }
    });
  });