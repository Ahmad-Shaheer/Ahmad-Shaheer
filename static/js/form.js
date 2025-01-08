
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

  



//  let currentStorageTool = "{{ pipeline['Storage'] }}";
//  let currentIntermediateTool = "{{ pipeline['Intermediate Storage'] }}";
//  let currentStructuredTool = "{{ pipeline['Structured'] }}";
//  let currentSemiTool = "{{ pipeline['Semi'] }}";
  



  function updateScreenStorageTool(selectElement) {
      const selectedTool = selectElement.value;
      const previousTool = document.getElementById('storage_tool_value_temp').value;
      // currentStorageTool = selectedTool;
      const storageToolElement = document.getElementById('storage-tool');
      storageToolElement.innerHTML = `
      <img src="/static/images/${selectedTool}.svg" alt="${selectedTool} Icon" style="width: 40px; height: 40px;"/>
      <strong>Storage:</strong> ${selectedTool}
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
    <strong>Intermediate Storage:</strong> ${currentIntermediateTool}
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
    <strong>Orchestration:</strong> ${currentOrchestrationTool}
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
    <strong>Structured Storage:</strong> ${currentStructuredTool}
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
    <strong>Semi Storage:</strong> ${currentSemiTool}
    `;

  const option = document.createElement('option');
  option.value = previousTool;
  option.textContent = previousTool;
  selectElement.appendChild(option);
  selectElement.querySelector(`option[value="${selectedTool}"]`).remove();
  selectElement.selectedIndex = 0;
}

async function sendMessage() {


  const userMessage = document.querySelector('.chat-window input').value;
  console.log("User message in sendMessage:", userMessage);  // Debugging line

  if (userMessage.length) {

      try {
          document.querySelector(".chat-window input").value = "";
          document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend",`
              <div class="user">
                  <p>${userMessage}</p>
              </div>
          `);

          document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend",`
              <div class="loader"></div>
          `);

          const chat = model.startChat(messages);

          let result = await chat.sendMessageStream(userMessage);
          
          document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend",`
              <div class="model">
                  <p></p>
              </div>
          `);
          
          let modelMessages = '';

          for await (const chunk of result.stream) {
            const chunkText = chunk.text();
            modelMessages = document.querySelectorAll(".chat-window .chat div.model");
            modelMessages[modelMessages.length - 1].querySelector("p").insertAdjacentHTML("beforeend",`
              ${chunkText}
          `);
          }

          messages.history.push({
              role: "user",
              parts: [{ text: userMessage }],
          });

          messages.history.push({
              role: "model",
              parts: [{ text: modelMessages[modelMessages.length - 1].querySelector("p").innerHTML }],
          });

      } catch (error) {
          document.querySelector(".chat-window .chat").insertAdjacentHTML("beforeend",`
              <div class="error">
                  <p>The message could not be sent. Please try again.</p>
              </div>
          `);
      }

      document.querySelector(".chat-window .chat .loader").remove();
      
  }
}


document.querySelector(".chat-button").addEventListener("click", () => {
  const body = document.querySelector("body");
  if (!body.classList.contains("chat-open")) {
      console.log("Opening chat...");
      body.classList.add("chat-open"); // Add the class to open the chat
      document.querySelector(".chat-window").style.display = "flex"; // Ensure visibility
  } else {
      console.log("Chat is already open.");
  }
});


document.querySelector(".chat-window .input-area button")
.addEventListener("click", ()=>sendMessage());


// close is working fine
document.querySelector(".chat-window button.close").addEventListener("click", () => {
  const body = document.querySelector("body");
  const chatWindow = document.querySelector(".chat-window");

  body.classList.remove("chat-open"); // Remove the chat-open class to close the chat
  chatWindow.style.display = "none"; // Hide the chat window
});


document.getElementById("ingestionToolOption").addEventListener("click", function() {
  console.log("ingestionToolOption clicked");  // Debugging line
  document.querySelector('.chat-window input').value = "What's my data format?";
  console.log("Value set to input:", document.querySelector('.chat-window input').value);  // Debugging line
  sendMessage();

  // Open the chat box simultaneously
  document.querySelector("body").classList.add("chat-open");
});

document.getElementById("processingToolOption").addEventListener("click", function() {
  console.log("processingToolOption clicked");  // Debugging line
  document.querySelector('.chat-window input').value = "What's my data format?";
  console.log("Value set to input:", document.querySelector('.chat-window input').value);  // Debugging line
  sendMessage();

  // Open the chat box simultaneously
  document.querySelector("body").classList.add("chat-open");
});

document.getElementById("storageToolOption").addEventListener("click", function() {
  console.log("storageToolOption clicked");  // Debugging line
  document.querySelector('.chat-window input').value = "What's my data format?";
  console.log("Value set to input:", document.querySelector('.chat-window input').value);  // Debugging line
  sendMessage();

  // Open the chat box simultaneously
  document.querySelector("body").classList.add("chat-open");
});

document.getElementById("orchestrationToolOption").addEventListener("click", function() {
  console.log("orchestrationToolOption clicked");  // Debugging line
  document.querySelector('.chat-window input').value = "What's my data format?";
  console.log("Value set to input:", document.querySelector('.chat-window input').value);  // Debugging line
  sendMessage();

  // Open the chat box simultaneously
  document.querySelector("body").classList.add("chat-open");
});




