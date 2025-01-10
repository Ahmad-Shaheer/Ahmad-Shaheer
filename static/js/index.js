import { GoogleGenerativeAI } from "@google/generative-ai";

const businessInfo = `

"You are a virtual assistant designed to guide users in planning and deploying their data pipelines. Your role is to help users make informed decisions based on their data type, processing needs, and end goals.

Your key functions include:

Providing practical recommendations for tools, frameworks, and strategies to process, transform, and store their data.
Explaining concepts in simple terms without unnecessary technical jargon unless explicitly requested.
Addressing common queries about data formats (e.g., CSV, JSON), data processing methods (batch or streaming), and pipeline tools (e.g., ETL, Apache Kafka).
Considerations:

Adapt recommendations based on user inputs, such as the nature of their data (structured, semi-structured, or mixed), their processing goals (storage, analytics, or graph-based databases), and whether transformations are needed.
Offer suggestions for both beginner-friendly and advanced tools depending on the user's expertise.
Maintain a concise, professional, and helpful tone throughout the conversation.
Tone Instructions:
Conciseness: Respond in short, informative sentences.
Formality: Use polite language with slight formality (e.g., "Please let us know," "We are happy to assist").
Clarity: Avoid technical jargon unless necessary.
Consistency: Ensure responses are aligned in tone and style across all queries.
Example: "Thank you for reaching out! Please let us know if you need further assistance."

`;

const API_KEY = "AIzaSyAPyT_TRvGDAE0otiFo4gbH-usDFMbdETc";
const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ 
    model: "gemini-1.5-flash",
    systemInstruction: businessInfo
});

let messages = {
    history: [],
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

document.querySelector(".chat-window .input-area button")
.addEventListener("click", ()=>sendMessage());

document.querySelector(".chat-button")
.addEventListener("click", ()=>{
    document.querySelector("body").classList.add("chat-open");
});

document.querySelector(".chat-window button.close")
.addEventListener("click", ()=>{
    document.querySelector("body").classList.remove("chat-open");
});




// Event listeners for buttons to trigger chat, set value, and open chat box
document.getElementById("dataFormatOption").addEventListener("click", function() {
    console.log("dataFormatOption clicked");  // Debugging line
    document.querySelector('.chat-window input').value = "What's my data format?";
    console.log("Value set to input:", document.querySelector('.chat-window input').value);  // Debugging line
    sendMessage();

    // Open the chat box simultaneously
    document.querySelector("body").classList.add("chat-open");
});

document.getElementById("dataSourceOption").addEventListener("click", function() {
    console.log("dataSourceOption clicked");  // Debugging line
    document.querySelector('.chat-window input').value = "How do I identify data sources?";
    console.log("Value set to input:", document.querySelector('.chat-window input').value);  // Debugging line
    sendMessage();

    // Open the chat box simultaneously
    document.querySelector("body").classList.add("chat-open");
});

document.getElementById("dataTransformOption").addEventListener("click", function() {
    console.log("dataTransformOption clicked");  // Debugging line
    document.querySelector('.chat-window input').value = "What are transformations?";
    console.log("Value set to input:", document.querySelector('.chat-window input').value);  // Debugging line
    sendMessage();

    // Open the chat box simultaneously
    document.querySelector("body").classList.add("chat-open");
});