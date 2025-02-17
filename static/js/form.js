
function handleStorageChange(selectElement) {
  updateStorageTool(selectElement);
  updateScreenStorageTool(selectElement);
}

function handleIntermediateChange(selectElement) {
  updateIntermediateTool(selectElement);
  updateScreenIntermediateTool(selectElement);
}

function handleStructuredChange(selectElement) {
  updateStructuredTool(selectElement);
  updateScreenStructuredTool(selectElement);
}

function handleSemiChange(selectElement) {
  updateSemiTool(selectElement);
  updateScreenSemiTool(selectElement);
}

function handleOrchestrationChange(selectElement) {
  updateOrchestrationTool(selectElement);
  updateScreenOrchestrationTool(selectElement);
}

function handleFinalStructuredChange(selectElement){
  updateFinalStructuredTool(selectElement);
  updateScreenFinalStructuredTool(selectElement);
}

function handleFinalSemiChange(selectElement){
  updateFinalSemiTool(selectElement);
  updateScreenFinalSemiTool(selectElement);
}

function handleProcessingChange(selectElement) {
  updateProcessingTool(selectElement);
  updateScreenProcessingTool(selectElement);

}


function updateOrchestrationTool(selectElement) {
  document.getElementById('orchestration_tool_value_temp').value = document.getElementById('orchestration_tool_value').value
  document.getElementById('orchestration_tool_value').value = selectElement.value;
  console.log("Storage tool value successfully updated to:", selectElement.value);
}
function updateStorageTool(selectElement) {
  document.getElementById('storage_tool_value_temp').value = document.getElementById('storage_tool_value').value
  document.getElementById('storage_tool_value').value = selectElement.value;
  console.log("Storage tool value successfully updated to:", selectElement.value);
}

function updateIntermediateTool(selectElement) {
    document.getElementById('intermediate_storage_tool_value_temp').value = document.getElementById('intermediate_storage_tool_value').value
    document.getElementById('intermediate_storage_tool_value').value = selectElement.value;
    console.log("Ingestion tool value successfully updated to:", selectElement.value);
  }
function updateStructuredTool(selectElement) {
  document.getElementById('structured_tool_value_temp').value = document.getElementById('structured_tool_value').value
  document.getElementById('structured_tool_value').value = selectElement.value;
  console.log("Ingestion tool value successfully updated to:", selectElement.value);
}

function updateSemiTool(selectElement) {
    document.getElementById('semi_structured_tool_value_temp').value = document.getElementById('semi_structured_tool_value').value
    document.getElementById('semi_structured_tool_value').value = selectElement.value;
    console.log("Ingestion tool value successfully updated to:", selectElement.value);
  }
  
function updateFinalSemiTool(selectElement) {
    document.getElementById('semi_structured_tool_final_value_temp').value = document.getElementById('semi_structured_tool_final_value').value
    document.getElementById('semi_structured_tool_final_value').value = selectElement.value;
    console.log("final semi tool value successfully updated to:", selectElement.value);
  }
  
function updateFinalStructuredTool(selectElement) {
    document.getElementById('structured_tool_final_value_temp').value = document.getElementById('structured_tool_final_value').value
    document.getElementById('structured_tool_final_value').value = selectElement.value;
    console.log("final structured tool value successfully updated to:", selectElement.value);
  }
  
function updateProcessingTool(selectElement) {
    document.getElementById('processing_tool_value_temp').value = document.getElementById('processing_tool_value').value
    document.getElementById('processing_tool_value').value = selectElement.value;
    console.log("Processing tool value successfully updated to:", selectElement.value);
  }
  

  function updateScreenStorageTool(selectElement) {
      const selectedTool = selectElement.value;
      const previousTool = document.getElementById('storage_tool_value_temp').value;
      // currentStorageTool = selectedTool;
      const storageToolElement = document.getElementById('storage-tool');
      storageToolElement.innerHTML = `
      <img src="/static/images/${selectedTool}.svg" alt="${selectedTool} Icon" style="width: 40px; height: 40px;"/>
      ${selectedTool}
      `;

      const option = document.createElement('option');
      option.value = previousTool;
      option.textContent = previousTool;
      selectElement.appendChild(option);
      selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
      selectElement.selectedIndex = 0;
    }

    
function updateScreenIntermediateTool(selectElement) {
    const selectedTool = selectElement.value;
    const previousTool = document.getElementById('intermediate_storage_tool_value_temp').value;
    currentIntermediateTool = selectedTool;
    const intermediateToolElement = document.getElementById('intermediate-storage-tool');
    intermediateToolElement.innerHTML = `
    <img src="/static/images/${currentIntermediateTool}.svg" alt="${currentIntermediateTool} Icon" style="width: 40px; height: 40px;"/>
    ${currentIntermediateTool}
    `;

    const option = document.createElement('option');
    option.value = previousTool;
    option.textContent = previousTool;
    selectElement.appendChild(option);
    selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
    selectElement.selectedIndex = 0;
  }

function updateScreenOrchestrationTool(selectElement) {
    const selectedTool = selectElement.value;
    const previousTool = document.getElementById('orchestration_tool_value_temp').value;
    currentOrchestrationTool = selectedTool;
    const OrchestrationToolElement = document.getElementById('orchestration-tool');
    OrchestrationToolElement.innerHTML = `
    <img src="/static/images/${currentOrchestrationTool}.svg" alt="${currentOrchestrationTool} Icon" style="width: 40px; height: 40px;"/>
    ${currentOrchestrationTool}
    `;

    const option = document.createElement('option');
    option.value = previousTool;
    option.textContent = previousTool;
    selectElement.appendChild(option);
    selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
    selectElement.selectedIndex = 0;
  }


function updateScreenStructuredTool(selectElement) {
  const selectedTool = selectElement.value;
  const previousTool = document.getElementById('structured_tool_value_temp').value;
  currentStructuredTool = selectedTool;
  const structuredToolElement = document.getElementById('structured-tool');
  structuredToolElement.innerHTML = `
    <img src="/static/images/${currentStructuredTool}.svg" alt="${currentStructuredTool} Icon" style="width: 40px; height: 40px;"/>
    ${currentStructuredTool}
    `;

  const option = document.createElement('option');
  option.value = previousTool;
  option.textContent = previousTool;
  selectElement.appendChild(option);
  selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
  selectElement.selectedIndex = 0;
}


function updateScreenSemiTool(selectElement) {
  const selectedTool = selectElement.value;
  const previousTool = document.getElementById('semi_structured_tool_value_temp').value;
  currentSemiTool = selectedTool;
  const semiToolElement = document.getElementById('semi-tool');
  semiToolElement.innerHTML = `
    <img src="/static/images/${currentSemiTool}.svg" alt="${currentSemiTool} Icon" style="width: 40px; height: 40px;"/>
    ${currentSemiTool}
    `;

  const option = document.createElement('option');
  option.value = previousTool;
  option.textContent = previousTool;
  selectElement.appendChild(option);
  selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
  selectElement.selectedIndex = 0;
}

function updateScreenFinalSemiTool(selectElement) {
  const selectedTool = selectElement.value;
  const previousTool = document.getElementById('semi_structured_tool_final_value_temp').value;
  currentSemiTool = selectedTool;
  const semiToolElement = document.getElementById('final-semi-tool');
  semiToolElement.innerHTML = `
    <img src="/static/images/${currentSemiTool}.svg" alt="${currentSemiTool} Icon" style="width: 40px; height: 40px;"/>
    ${currentSemiTool}
    `;

  const option = document.createElement('option');
  option.value = previousTool;
  option.textContent = previousTool;
  selectElement.appendChild(option);
  selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
  selectElement.selectedIndex = 0;
}

function updateScreenFinalStructuredTool(selectElement) {
  const selectedTool = selectElement.value;
  const previousTool = document.getElementById('structured_tool_final_value_temp').value;
  currentSemiTool = selectedTool;
  const semiToolElement = document.getElementById('final-structured-tool');
  semiToolElement.innerHTML = `
    <img src="/static/images/${currentSemiTool}.svg" alt="${currentSemiTool} Icon" style="width: 40px; height: 40px;"/>
    ${currentSemiTool}
    `;

  const option = document.createElement('option');
  option.value = previousTool;
  option.textContent = previousTool;
  selectElement.appendChild(option);
  selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
  selectElement.selectedIndex = 0;
}

function updateScreenProcessingTool(selectElement) {
  const selectedTool = selectElement.value;
  const previousTool = document.getElementById('processing_tool_value_temp').value;
  currentSemiTool = selectedTool;
  const semiToolElement = document.getElementById('processing-tool');
  semiToolElement.innerHTML = `
    <img src="/static/images/${currentSemiTool}.svg" alt="${currentSemiTool} Icon" style="width: 40px; height: 40px;"/>
    ${currentSemiTool}
    `;

  const option = document.createElement('option');
  option.value = previousTool;
  option.textContent = previousTool;
  selectElement.appendChild(option);
  selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
  selectElement.selectedIndex = 0;
}


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



