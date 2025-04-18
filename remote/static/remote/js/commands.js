document.querySelectorAll('.remote-button').forEach(button => {
  button.addEventListener('click', () => {
    const buttonType = button.dataset.buttonType;
    const command = button.dataset.command;
    const targetType = button.dataset.targetType;
    const appEntry = button.dataset.appEntry;

    fetch('/remote/trigger/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ button_type: buttonType, target_type: targetType, app_entry: appEntry, command: command })

    });
  });
});

function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === 'csrftoken') return decodeURIComponent(value);
  }
  return null;
}