// Navigation and favorite buttons data from Django
const navigationButtons = {{ navigation_buttons_json|safe }};
const favoriteButtons = {{ favorite_buttons_json|safe }};

// Update target button options based on command type
function updateTargetOptions() {
  const commandType = document.getElementById("command_type").value;
  const targetSelect = document.getElementById("target_button");

  // Clear existing options
  targetSelect.innerHTML = '<option value="">Select button</option>';

  if (commandType === "navigation") {
    navigationButtons.forEach((button) => {
      targetSelect.innerHTML += `<option value="${button.name}">${button.name}</option>`;
    });
  } else if (commandType === "favorite") {
    favoriteButtons.forEach((button) => {
      targetSelect.innerHTML += `<option value="${button.name}">${button.name}</option>`;
    });
  }
}

// Test voice command function
async function testVoiceCommand() {
  const btn = document.getElementById("testVoiceBtn");
  const result = document.getElementById("voiceResult");

  btn.innerHTML = "Listening...";
  btn.classList.add("recording");
  btn.disabled = true;

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

    if (data.status === "success") {
      result.innerHTML = `
                  <div class="alert alert-success">
                      <strong>Success!</strong><br>
                      Recognized: "${data.voice_command.recognized_text}"<br>
                      Matched: "${data.voice_command.matched_phrase}"<br>
                      Executed: ${data.voice_command.target_button}<br>
                      Result: ${data.message}
                  </div>
              `;
    } else {
      result.innerHTML = `
                  <div class="alert alert-warning">
                      <strong>Notice:</strong> ${data.message}
                  </div>
              `;
    }
  } catch (error) {
    result.innerHTML = `
              <div class="alert alert-danger">
                  <strong>Error:</strong> ${error.message}
              </div>
          `;
  }

  btn.innerHTML = "Test Voice Command";
  btn.classList.remove("recording");
  btn.disabled = false;
}
