document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contactForm");
  const submitButton = form.querySelector(".submit-btn");
  let hasAttemptedSubmit = false;

  const validationRules = {
    firstName: {
      required: true,
      minLength: 2,
      maxLength: 100,
      pattern: /^[a-zA-Z\s\-'\.]+$/,
      message: "First name is required (minimum 2 characters, letters only)",
    },
    lastName: {
      required: true,
      minLength: 2,
      maxLength: 100,
      pattern: /^[a-zA-Z\s\-'\.]+$/,
      message: "Last name is required (minimum 2 characters, letters only)",
    },
    email: {
      required: true,
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
      message: "Please enter a valid email address",
    },
    phone: {
      required: false,
      pattern: /^[\d\s\-\+\(\)]+$/,
      minLength: 7,
      maxLength: 20,
      message: "Please enter a valid phone number (7-20 digits)",
    },
    company: {
      required: false,
      maxLength: 200,
      message: "Company name must be less than 200 characters",
    },
    region: {
      required: false,
      maxLength: 100,
      message: "Region must be less than 100 characters",
    },
    country: {
      required: false,
      maxLength: 100,
      message: "Country must be less than 100 characters",
    },
    role: {
      required: false,
      message: "Please select your role",
    },
    volume: {
      required: false,
      maxLength: 100,
      message: "Annual volume must be less than 100 characters",
    },
    questionType: {
      required: false,
      message: "Please select a question type",
    },
    message: {
      required: false,
      maxLength: 2000,
      message: "Message must be less than 2000 characters",
    },
    privacy: {
      required: true,
      message: "You must agree to the privacy policy",
    },
  };

  function showFieldError(field, message) {
    clearFieldError(field);
    const errorDiv = document.createElement("div");
    errorDiv.className = "field-error-message";
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
            color: #e74c3c; 
            font-size: 14px; 
            margin-top: 6px; 
            display: flex; 
            align-items: center; 
            animation: slideDown 0.3s ease-out;`;
    const icon = document.createElement("span");
    icon.innerHTML = "⚠";
    icon.style.marginRight = "6px";
    icon.style.fontSize = "16px";
    errorDiv.insertBefore(icon, errorDiv.firstChild);
    field.classList.add("error");
    if (field.type === "checkbox") {
      field.closest(".checkbox-wrapper").appendChild(errorDiv);
    } else {
      field.parentElement.appendChild(errorDiv);
    }
    field.style.animation = "shake 0.5s ease-in-out";
    setTimeout(() => {
      field.style.animation = "";
    }, 500);
  }

  function clearFieldError(field) {
    let parent =
      field.type === "checkbox"
        ? field.closest(".checkbox-wrapper")
        : field.parentElement;
    const existingError = parent.querySelector(".field-error-message");
    if (existingError) {
      existingError.remove();
    }
    field.classList.remove("error", "success");
  }

  function showFieldSuccess(field) {
    clearFieldError(field);
    field.classList.add("success");
    field.style.animation = "successPulse 0.3s ease-out";
    setTimeout(() => {
      field.style.animation = "";
    }, 300);
  }

  function validateField(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return true;
    const rule = validationRules[fieldId];
    if (!rule) return true;

    let value = field.type === "checkbox" ? field.checked : field.value.trim();
    let isValid = true;

    if (rule.required) {
      if (field.type === "checkbox" && !value) {
        isValid = false;
      } else if (field.type !== "checkbox" && !value) {
        isValid = false;
      }
    }

    if (isValid && value && field.type !== "checkbox") {
      if (rule.minLength && value.length < rule.minLength) isValid = false;
      if (rule.maxLength && value.length > rule.maxLength) isValid = false;
      if (rule.pattern && !rule.pattern.test(value)) isValid = false;
    }

    if (hasAttemptedSubmit) {
      if (!isValid) {
        showFieldError(field, rule.message);
      } else {
        showFieldSuccess(field);
      }
    } else {
      clearFieldError(field);
    }

    return isValid;
  }

  let emailValidationTimeout;
  function validateEmailAjax(email) {
    if (!email || !validationRules.email.pattern.test(email)) {
      return;
    }
    if (emailValidationTimeout) {
      clearTimeout(emailValidationTimeout);
    }
    emailValidationTimeout = setTimeout(() => {
      const emailField = document.getElementById("email");
      emailField.style.backgroundImage =
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2'%3E%3Cpath d='M21 12a9 9 0 11-6.219-8.56'/%3E%3C/svg%3E\")";
      emailField.style.backgroundRepeat = "no-repeat";
      emailField.style.backgroundPosition = "right 12px center";
      emailField.style.backgroundSize = "16px";
      emailField.style.paddingRight = "40px";
      fetch("/validate-email/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ email: email }),
      })
        .then((response) => response.json())
        .then((data) => {
          emailField.style.backgroundImage = "";
          emailField.style.paddingRight = "";
          if (data.warning) {
            console.warn("Email validation warning:", data.message);
            const warningDiv = document.createElement("div");
            warningDiv.className = "field-warning-message";
            warningDiv.textContent = data.message;
            warningDiv.style.cssText = `
                            color: #f39c12; font-size: 12px; margin-top: 4px; opacity: 0.8;`;
            const existingWarning = emailField.parentElement.querySelector(
              ".field-warning-message"
            );
            if (existingWarning) {
              existingWarning.remove();
            }
            emailField.parentElement.appendChild(warningDiv);
            setTimeout(() => {
              if (warningDiv.parentElement) {
                warningDiv.remove();
              }
            }, 3000);
          } else if (data.valid) {
            showFieldSuccess(emailField);
          }
        })
        .catch((error) => {
          console.error("Email validation error:", error);
          emailField.style.backgroundImage = "";
          emailField.style.paddingRight = "";
        });
    }, 500);
  }

  function validateForm(showErrorsOnFields = false) {
    if (showErrorsOnFields) {
      hasAttemptedSubmit = true;
    }
    let isFormValid = true;
    Object.keys(validationRules).forEach((fieldId) => {
      if (!validateField(fieldId)) {
        isFormValid = false;
      }
    });
    updateSubmitButtonState(isFormValid);
    return isFormValid;
  }

  function updateSubmitButtonState(isValid) {
    if (isValid) {
      submitButton.disabled = false;
      submitButton.classList.remove("disabled");
      submitButton.style.opacity = "1";
    } else {
      submitButton.disabled = true;
      submitButton.classList.add("disabled");
      submitButton.style.opacity = "0.6";
    }
  }

  function getCSRFToken() {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") {
        return value;
      }
    }
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      return csrfMeta.getAttribute("content");
    }
    const csrfInput = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    );
    if (csrfInput) {
      return csrfInput.value;
    }
    return "";
  }

  function showLoadingState() {
    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";
    submitButton.classList.add("loading");
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
      input.disabled = true;
    });
  }

  function hideLoadingState() {
    submitButton.classList.remove("loading");
    submitButton.textContent = "Submit";
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
      input.disabled = false;
    });
    validateForm(false);
  }

  function showSuccessMessage(message) {
    const existingMessage = form.querySelector(
      ".success-message, .error-message-general"
    );
    if (existingMessage) {
      existingMessage.remove();
    }
    const successDiv = document.createElement("div");
    successDiv.className = "success-message";
    successDiv.innerHTML = `
            <div style="display: flex; align-items: center;">
                <span style="font-size: 20px; margin-right: 10px;">✓</span>
                <span>${message}</span>
            </div>`;
    successDiv.style.cssText = `
            background-color: #d4edda; color: #155724; padding: 16px 20px;
            border: 1px solid #c3e6cb; border-radius: 8px; margin-bottom: 24px;
            font-size: 15px; font-weight: 500; animation: slideIn 0.4s ease-out;`;
    form.insertBefore(successDiv, form.firstChild);
    setTimeout(() => {
      if (successDiv.parentNode) {
        successDiv.style.animation = "slideOut 0.4s ease-out";
        setTimeout(() => {
          if (successDiv.parentNode) {
            successDiv.remove();
          }
        }, 400);
      }
    }, 10000);
  }

  function showErrorMessage(message) {
    const existingMessage = form.querySelector(
      ".success-message, .error-message-general"
    );
    if (existingMessage) {
      existingMessage.remove();
    }
    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message-general";
    errorDiv.innerHTML = `
            <div style="display: flex; align-items: center;">
                <span style="font-size: 20px; margin-right: 10px;">⚠</span>
                <span>${message}</span>
            </div>`;
    errorDiv.style.cssText = `
            background-color: #f8d7da; color: #721c24; padding: 16px 20px;
            border: 1px solid #f5c6cb; border-radius: 8px; margin-bottom: 24px;
            font-size: 15px; font-weight: 500; animation: slideIn 0.4s ease-out;`;
    form.insertBefore(errorDiv, form.firstChild);
  }

  function setupFieldListeners() {
    Object.keys(validationRules).forEach((fieldId) => {
      const field = document.getElementById(fieldId);
      if (!field) return;

      const eventHandler = () => {
        validateField(fieldId);

        // Update button state without showing errors everywhere
        let isFormCurrentlyValid = true;
        Object.keys(validationRules).forEach((id) => {
          const f = document.getElementById(id);
          if (!f) return;
          const rule = validationRules[id];
          if (!rule) return;
          const value = f.type === "checkbox" ? f.checked : f.value.trim();
          let isFieldValid = true;
          if (rule.required && (f.type === "checkbox" ? !value : !value)) {
            isFieldValid = false;
          } else if (value && f.type !== "checkbox") {
            if (rule.minLength && value.length < rule.minLength)
              isFieldValid = false;
            if (rule.maxLength && value.length > rule.maxLength)
              isFieldValid = false;
            if (rule.pattern && !rule.pattern.test(value)) isFieldValid = false;
          }
          if (!isFieldValid) isFormCurrentlyValid = false;
        });
        updateSubmitButtonState(isFormCurrentlyValid);

        if (fieldId === "email" && field.value.trim()) {
          validateEmailAjax(field.value.trim());
        }
      };

      field.addEventListener("input", eventHandler);
      field.addEventListener("change", eventHandler);
    });
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (!validateForm(true)) {
      showErrorMessage("Please correct the errors above before submitting.");
      const firstErrorField = form.querySelector(".error");
      if (firstErrorField) {
        firstErrorField.scrollIntoView({ behavior: "smooth", block: "center" });
        firstErrorField.focus();
      }
      return;
    }
    showLoadingState();
    try {
      const formData = {
        first_name: document.getElementById("firstName")?.value?.trim() || "",
        last_name: document.getElementById("lastName")?.value?.trim() || "",
        email: document.getElementById("email")?.value?.trim() || "",
        phone: document.getElementById("phone")?.value?.trim() || "",
        company: document.getElementById("company")?.value?.trim() || "",
        region: document.getElementById("region")?.value?.trim() || "",
        country: document.getElementById("country")?.value?.trim() || "",
        role: document.getElementById("role")?.value?.trim() || "",
        annual_volume: document.getElementById("volume")?.value?.trim() || "",
        question_type:
          document.getElementById("questionType")?.value?.trim() || "",
        message: document.getElementById("message")?.value?.trim() || "",
        privacy_consent: document.getElementById("privacy")?.checked || false,
      };

      const response = await fetch("/contact-step-2/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      if (response.ok && result.success) {
        showSuccessMessage(
          result.message ||
            "Thank you for contacting us! We will get back to you soon."
        );
        form.reset();
        hasAttemptedSubmit = false;
        Object.keys(validationRules).forEach((fieldId) => {
          const field = document.getElementById(fieldId);
          if (field) {
            clearFieldError(field);
          }
        });
        validateForm(false);
        window.scrollTo({ top: 0, behavior: "smooth" });
      } else {
        if (result.errors && typeof result.errors === "object") {
          Object.keys(result.errors).forEach((fieldKey) => {
            const fieldMapping = {
              first_name: "firstName",
              last_name: "lastName",
              email: "email",
              phone: "phone",
              company: "company",
              region: "region",
              country: "country",
              role: "role",
              annual_volume: "volume",
              question_type: "questionType",
              message: "message",
              privacy_consent: "privacy",
            };
            const frontendFieldId = fieldMapping[fieldKey] || fieldKey;
            const field = document.getElementById(frontendFieldId);
            if (
              field &&
              result.errors[fieldKey] &&
              result.errors[fieldKey].length > 0
            ) {
              showFieldError(field, result.errors[fieldKey][0]);
            }
          });
        }
        const errorMessage =
          result.message || "An error occurred. Please try again.";
        showErrorMessage(errorMessage);
      }
    } catch (error) {
      console.error("Form submission error:", error);
      showErrorMessage(
        "A network error occurred. Please check your connection and try again."
      );
    } finally {
      hideLoadingState();
    }
  });

  function initializeForm() {
    setupFieldListeners();
    validateForm(false);
  }

  function addStyles() {
    const style = document.createElement("style");
    style.textContent = `
          @keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
          @keyframes slideIn { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
          @keyframes slideOut { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(-20px); } }
          @keyframes shake { 0%, 100% { transform: translateX(0); } 10%, 30%, 50%, 70%, 90% { transform: translateX(-3px); } 20%, 40%, 60%, 80% { transform: translateX(3px); } }
          @keyframes successPulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
          @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
          .form-group input.error, .form-group select.error, .form-group textarea.error, .checkbox-wrapper input.error + .checkbox-label { border-color: #e74c3c !important; background-color: #fef5f5 !important; box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1) !important; }
          .checkbox-wrapper input.error + .checkbox-label { color: #e74c3c; }
          .form-group input.success, .form-group select.success, .form-group textarea.success { border-color: #27ae60 !important; background-color: #f5fef7 !important; box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1) !important; }
          .submit-btn:disabled { opacity: 0.6 !important; cursor: not-allowed !important; }
          .submit-btn.loading { position: relative; color: transparent !important; }
          .submit-btn.loading::after { content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 20px; height: 20px; border: 2px solid rgba(255, 255, 255, 0.3); border-radius: 50%; border-top: 2px solid white; animation: spin 1s linear infinite; }
          @media (prefers-reduced-motion: reduce) { * { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; } }
      `;
    document.head.appendChild(style);
  }

  addStyles();
  initializeForm();

  console.log("Contact Step 2 form initialized successfully");
});
