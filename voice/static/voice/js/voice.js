let isRecording = false;
let usageCount = parseInt(localStorage.getItem("voiceUsageCount") || "0");

// Initialize usage count display
document.getElementById("usageCount").textContent = usageCount;

async function startVoiceCommand() {
  if (isRecording) return;

  const button = document.getElementById("voiceButton");
  const status = document.getElementById("voiceStatus");
  const responseArea = document.getElementById("responseArea");

  // Clear previous responses
  responseArea.innerHTML = "";

  // Update UI for recording state
  isRecording = true;
  button.classList.add("recording");
  button.innerHTML = '<i class="fas fa-stop"></i>';

  status.innerHTML = `
        <div>
            <i class="fas fa-microphone text-success fa-2x mb-2"></i>
            <p class="text-success mb-0"><strong>Listening...</strong></p>
            <small class="text-muted">Speak your command now</small>
        </div>
    `;

  try {
    const response = await fetch("/voice/command/", {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();

    // Update usage count
    if (data.status === "success") {
      usageCount++;
      localStorage.setItem("voiceUsageCount", usageCount.toString());
      document.getElementById("usageCount").textContent = usageCount;
    }

    // Display result
    displayResult(data);
  } catch (error) {
    displayResult({
      status: "error",
      message: `Connection error: ${error.message}`,
    });
  } finally {
    // Reset UI
    isRecording = false;
    button.classList.remove("recording");
    button.innerHTML = '<i class="fas fa-microphone"></i>';

    status.innerHTML = `
            <div>
                <i class="fas fa-microphone-slash text-muted fa-2x mb-2"></i>
                <p class="text-muted mb-0">Click the microphone to start</p>
            </div>
        `;
  }
}

function displayResult(data) {
  const responseArea = document.getElementById("responseArea");
  let messageClass = "response-info";
  let icon = "fas fa-info-circle";

  if (data.status === "success") {
    messageClass = "response-success";
    icon = "fas fa-check-circle";
  } else if (data.status === "error") {
    messageClass = "response-error";
    icon = "fas fa-exclamation-circle";
  }

  let content = `
        <div class="response-message ${messageClass}">
            <i class="${icon} me-2"></i>
            <strong>${data.message || "Command processed"}</strong>
    `;

  if (data.voice_command) {
    content += `
            <div class="mt-2">
                <small>
                    <strong>Recognized:</strong> "${data.voice_command.recognized_text}"<br>
                    <strong>Matched:</strong> "${data.voice_command.matched_phrase}"<br>
                    <strong>Action:</strong> ${data.voice_command.target_button}
                </small>
            </div>
        `;
  }

  content += "</div>";
  responseArea.innerHTML = content;

  // Auto-clear success messages after 5 seconds
  if (data.status === "success") {
    setTimeout(() => {
      responseArea.innerHTML = "";
    }, 5000);
  }
}

// Add CSRF token to all AJAX requests
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Add keyboard support
document.addEventListener("keydown", function (event) {
  // Space bar to trigger voice command
  if (event.code === "Space" && !isRecording) {
    event.preventDefault();
    startVoiceCommand();
  }
});

// Reset daily usage count at midnight
const now = new Date();
const lastReset = localStorage.getItem("voiceUsageLastReset");
const today = now.toDateString();

if (lastReset !== today) {
  localStorage.setItem("voiceUsageCount", "0");
  localStorage.setItem("voiceUsageLastReset", today);
  document.getElementById("usageCount").textContent = "0";
}
