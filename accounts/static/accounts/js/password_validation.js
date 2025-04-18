// accounts/js/password_validation.js

function checkPasswordStrength () {
  const password = document.getElementById("password").value;
  const strengthRequirements = document.getElementById("strength-requirements");
  strengthRequirements.classList.remove('d-none');
  const lengthRequirement = document.getElementById("length-requirement");
  const uppercaseRequirement = document.getElementById("uppercase-requirement");
  const lowercaseRequirement = document.getElementById("lowercase-requirement");
  const numberRequirement = document.getElementById("number-requirement");
  const specialCharRequirement = document.getElementById("special-char-requirement");

  if (password.length < 8) {
    lengthRequirement.classList.add("text-danger");
  } else {
    lengthRequirement.classList.remove("text-danger");
    lengthRequirement.classList.add("text-success");
  }
  if (!/[A-Z]/.test(password)) {
    uppercaseRequirement.classList.add("text-danger");
  }
  else {
    uppercaseRequirement.classList.remove("text-danger");
    uppercaseRequirement.classList.add("text-success");
  }
  if (!/[a-z]/.test(password)) {
    lowercaseRequirement.classList.add("text-danger");
  }
  else {
    lowercaseRequirement.classList.remove("text-danger");
    lowercaseRequirement.classList.add("text-success");
  }
  if (!/[0-9]/.test(password)) {
    numberRequirement.classList.add("text-danger");
  }
  else {
    numberRequirement.classList.remove("text-danger");
    numberRequirement.classList.add("text-success");
  }
  if (!/[-_!@#$%^&*(),.?":{}|<>]/.test(password)) {
    specialCharRequirement.classList.add("text-danger");
  }
  else {
    specialCharRequirement.classList.remove("text-danger");
    specialCharRequirement.classList.add("text-success");
  }
  if (password.length >= 8 && /[A-Z]/.test(password) && /[a-z]/.test(password) && /[0-9]/.test(password) && /[-_!@#$%^&*(),.?":{}|<>]/.test(password)) {
    strengthRequirements.classList.remove("text-danger");
    strengthRequirements.classList.add("text-success");
    document.getElementById("strength-text").innerText = "Password meets all requirements.";
  } else {
    strengthRequirements.classList.remove("text-success");
    strengthRequirements.classList.add("text-danger");
    document.getElementById("strength-text").innerText = "Password does not meet all requirements.";
  }
}

document.getElementById("password").addEventListener("input", checkPasswordStrength);
