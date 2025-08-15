document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("contactForm");
  const submitButton = form.querySelector(".submit-btn");
  const requiredFields = [
    "first_name",
    "last_name",
    "email",
    "privacy_consent",
  ];

  // Field validation rules
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

  // Error display utilities
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
            animation: slideDown 0.3s ease-out;
        `;

    // Add warning icon
    const icon = document.createElement("span");
    icon.innerHTML = "⚠";
    icon.style.marginRight = "6px";
    icon.style.fontSize = "16px";
    errorDiv.insertBefore(icon, errorDiv.firstChild);

    field.classList.add("error");
    field.parentElement.appendChild(errorDiv);

    // Add shake animation to field
    field.style.animation = "shake 0.5s ease-in-out";
    setTimeout(() => {
      field.style.animation = "";
    }, 500);
  }

  function clearFieldError(field) {
    const existingError = field.parentElement.querySelector(
      ".field-error-message"
    );
    if (existingError) {
      existingError.remove();
    }
    field.classList.remove("error", "success");
  }

  function showFieldSuccess(field) {
    clearFieldError(field);
    field.classList.add("success");

    // Add checkmark animation
    field.style.animation = "successPulse 0.3s ease-out";
    setTimeout(() => {
      field.style.animation = "";
    }, 300);
  }

  // Field validation function
  function validateField(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return true;

    const rule = validationRules[fieldId];
    if (!rule) return true;

    let value;
    if (field.type === "checkbox") {
      value = field.checked;
    } else {
      value = field.value.trim();
    }

    // Required field check
    if (rule.required) {
      if (field.type === "checkbox" && !value) {
        showFieldError(field, rule.message);
        return false;
      } else if (field.type !== "checkbox" && (!value || value === "")) {
        showFieldError(field, rule.message);
        return false;
      }
    }

    // If field is not required and empty, skip other validations
    if (!rule.required && (!value || value === "")) {
      clearFieldError(field);
      return true;
    }

    // Minimum length check
    if (
      rule.minLength &&
      field.type !== "checkbox" &&
      value.length < rule.minLength
    ) {
      showFieldError(field, rule.message);
      return false;
    }

    // Maximum length check
    if (
      rule.maxLength &&
      field.type !== "checkbox" &&
      value.length > rule.maxLength
    ) {
      showFieldError(field, rule.message);
      return false;
    }

    // Pattern check
    if (
      rule.pattern &&
      field.type !== "checkbox" &&
      !rule.pattern.test(value)
    ) {
      showFieldError(field, rule.message);
      return false;
    }

    // Special validation for select fields
    if (
      field.tagName === "SELECT" &&
      rule.required &&
      (!value || value === "")
    ) {
      showFieldError(field, rule.message);
      return false;
    }

    showFieldSuccess(field);
    return true;
  }

  // Email validation with AJAX
  let emailValidationTimeout;
  function validateEmailAjax(email) {
    if (!email || !validationRules.email.pattern.test(email)) {
      return;
    }

    // Clear previous timeout
    if (emailValidationTimeout) {
      clearTimeout(emailValidationTimeout);
    }

    // Debounce email validation
    emailValidationTimeout = setTimeout(() => {
      const emailField = document.getElementById("email");

      // Show loading state
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
          // Clear loading state
          emailField.style.backgroundImage = "";
          emailField.style.paddingRight = "";

          if (data.warning) {
            // Show warning but don't mark as error
            console.warn("Email validation warning:", data.message);

            // Show subtle warning indicator
            const warningDiv = document.createElement("div");
            warningDiv.className = "field-warning-message";
            warningDiv.textContent = data.message;
            warningDiv.style.cssText = `
                        color: #f39c12;
                        font-size: 12px;
                        margin-top: 4px;
                        opacity: 0.8;
                    `;

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
            // Email is valid
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

  // Form validation
  function validateForm() {
    let isValid = true;

    // Validate all fields with rules
    Object.keys(validationRules).forEach((fieldId) => {
      if (!validateField(fieldId)) {
        isValid = false;
      }
    });

    // Update submit button state
    updateSubmitButtonState(isValid);

    return isValid;
  }

  // Update submit button state
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

  // Get CSRF token
  function getCSRFToken() {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") {
        return value;
      }
    }

    // Fallback: try to get from meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      return csrfMeta.getAttribute("content");
    }

    // Fallback: try to get from hidden input
    const csrfInput = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    );
    if (csrfInput) {
      return csrfInput.value;
    }

    return "";
  }

  // Show loading state
  function showLoadingState() {
    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";
    submitButton.classList.add("loading");

    // Disable all form inputs
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
      input.disabled = true;
    });
  }

  // Hide loading state
  function hideLoadingState() {
    submitButton.classList.remove("loading");
    submitButton.textContent = "Submit";

    // Re-enable all form inputs
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
      input.disabled = false;
    });

    // Re-validate form to update button state
    validateForm();
  }

  // Show success message
  function showSuccessMessage(message) {
    // Remove any existing messages
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
            </div>
        `;
    successDiv.style.cssText = `
            background-color: #d4edda;
            color: #155724;
            padding: 16px 20px;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            margin-bottom: 24px;
            font-size: 15px;
            font-weight: 500;
            animation: slideIn 0.4s ease-out;
        `;

    form.insertBefore(successDiv, form.firstChild);

    // Remove success message after 10 seconds
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

  // Show error message
  function showErrorMessage(message) {
    // Remove any existing messages
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
            </div>
        `;
    errorDiv.style.cssText = `
            background-color: #f8d7da;
            color: #721c24;
            padding: 16px 20px;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            margin-bottom: 24px;
            font-size: 15px;
            font-weight: 500;
            animation: slideIn 0.4s ease-out;
        `;

    form.insertBefore(errorDiv, form.firstChild);
  }

  // Handle form field changes
  function setupFieldListeners() {
    Object.keys(validationRules).forEach((fieldId) => {
      const field = document.getElementById(fieldId);
      if (!field) return;

      // Validate on blur (when user leaves field)
      field.addEventListener("blur", (e) => {
        validateField(fieldId);
        validateForm();
      });

      // Validate on input for immediate feedback (with debouncing)
      field.addEventListener("input", (e) => {
        // Clear previous timeout
        if (field.validationTimeout) {
          clearTimeout(field.validationTimeout);
        }

        // Debounce validation
        field.validationTimeout = setTimeout(() => {
          validateField(fieldId);
          validateForm();

          // Special handling for email
          if (fieldId === "email" && field.value.trim()) {
            validateEmailAjax(field.value.trim());
          }
        }, 300);
      });

      // Special handling for select fields
      if (field.tagName === "SELECT") {
        field.addEventListener("change", (e) => {
          validateField(fieldId);
          validateForm();
        });
      }

      // Special handling for checkbox
      if (field.type === "checkbox") {
        field.addEventListener("change", (e) => {
          validateField(fieldId);
          validateForm();
        });
      }
    });
  }

  // Form submission handler
  // Form submission handler - Düzeltilmiş versiyon
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Final validation before submission
    if (!validateForm()) {
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
      // Collect form data - DÜZELTİLDİ
      const formData = {};

      // Manuel olarak form alanlarını topla
      formData.first_name =
        document.getElementById("firstName")?.value?.trim() || "";
      formData.last_name =
        document.getElementById("lastName")?.value?.trim() || "";
      formData.email = document.getElementById("email")?.value?.trim() || "";
      formData.phone = document.getElementById("phone")?.value?.trim() || "";
      formData.company =
        document.getElementById("company")?.value?.trim() || "";
      formData.region = document.getElementById("region")?.value?.trim() || "";
      formData.country =
        document.getElementById("country")?.value?.trim() || "";
      formData.role = document.getElementById("role")?.value?.trim() || "";
      formData.annual_volume =
        document.getElementById("volume")?.value?.trim() || "";
      formData.question_type =
        document.getElementById("questionType")?.value?.trim() || "";
      formData.message =
        document.getElementById("message")?.value?.trim() || "";
      formData.privacy_consent =
        document.getElementById("privacy")?.checked || false;

      // Boş değerleri kontrol et ve debug için log ekle
      console.log("Form data being sent:", formData);

      // Required alanları kontrol et
      const requiredFields = {
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        privacy_consent: formData.privacy_consent,
      };

      for (let [field, value] of Object.entries(requiredFields)) {
        if (field === "privacy_consent" && !value) {
          console.error(`Required field ${field} is missing or false`);
          showErrorMessage("Privacy policy must be accepted.");
          return;
        } else if (field !== "privacy_consent" && (!value || value === "")) {
          console.error(`Required field ${field} is missing or empty`);
          showErrorMessage(`${field.replace("_", " ")} is required.`);
          return;
        }
      }

      const response = await fetch("/contact-step-2/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify(formData),
      });

      let result;
      try {
        result = await response.json();
      } catch (parseError) {
        console.error("Failed to parse response as JSON:", parseError);
        // Response text'ini de kontrol et
        const responseText = await response.text();
        console.error("Response text:", responseText);
        throw new Error("Invalid response from server");
      }

      console.log("Server response:", result); // Debug için

      if (response.ok && result.success) {
        showSuccessMessage(
          result.message ||
            "Thank you for contacting us! We will get back to you soon."
        );

        // Reset form
        form.reset();

        // Clear all field states
        Object.keys(validationRules).forEach((fieldId) => {
          const field = document.getElementById(fieldId);
          if (field) {
            clearFieldError(field);
          }
        });

        // Scroll to success message
        window.scrollTo({ top: 0, behavior: "smooth" });

        setTimeout(() => {
          form.style.animation = "successBounce 0.6s ease-out";
          setTimeout(() => {
            form.style.animation = "";
          }, 600);
        }, 100);
      } else {
        console.error("Server returned error:", result); // Debug için

        // Handle field-specific errors
        if (result.errors && typeof result.errors === "object") {
          let hasFieldErrors = false;
          Object.keys(result.errors).forEach((fieldKey) => {
            // Backend field names to frontend field IDs
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
              hasFieldErrors = true;
            }
          });

          if (hasFieldErrors) {
            showErrorMessage("Please correct the errors above and try again.");
            const firstErrorField = form.querySelector(".error");
            if (firstErrorField) {
              setTimeout(() => {
                firstErrorField.scrollIntoView({
                  behavior: "smooth",
                  block: "center",
                });
                firstErrorField.focus();
              }, 100);
            }
          }
        }

        // Show general error message
        const errorMessage =
          result.message ||
          "An error occurred while submitting the form. Please try again.";
        if (!result.errors || Object.keys(result.errors).length === 0) {
          showErrorMessage(errorMessage);
        }
      }
    } catch (error) {
      console.error("Form submission error:", error);

      let errorMessage =
        "An error occurred while submitting the form. Please try again.";

      if (error.name === "TypeError" && error.message.includes("fetch")) {
        errorMessage =
          "Network error. Please check your connection and try again.";
      } else if (error.message) {
        errorMessage = error.message;
      }

      showErrorMessage(errorMessage);
    } finally {
      hideLoadingState();
    }
  });

  // Initialize form
  function initializeForm() {
    setupFieldListeners();
    validateForm(); // Initial validation to set button state

    // Add form reset handler
    const resetButtons = form.querySelectorAll(
      'button[type="reset"], input[type="reset"]'
    );
    resetButtons.forEach((button) => {
      button.addEventListener("click", (e) => {
        setTimeout(() => {
          // Clear all field states after reset
          Object.keys(validationRules).forEach((fieldId) => {
            const field = document.getElementById(fieldId);
            if (field) {
              clearFieldError(field);
            }
          });

          // Remove any messages
          const messages = form.querySelectorAll(
            ".success-message, .error-message-general"
          );
          messages.forEach((message) => message.remove());

          validateForm();
        }, 10);
      });
    });
  }

  // Add CSS animations and styles
  function addStyles() {
    const style = document.createElement("style");
    style.textContent = `
            @keyframes slideDown {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideOut {
                from {
                    opacity: 1;
                    transform: translateY(0);
                }
                to {
                    opacity: 0;
                    transform: translateY(-20px);
                }
            }
            
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-3px); }
                20%, 40%, 60%, 80% { transform: translateX(3px); }
            }
            
            @keyframes successPulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.02); }
                100% { transform: scale(1); }
            }
            
            @keyframes successBounce {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .form-group input.error,
            .form-group select.error,
            .form-group textarea.error {
                border-color: #e74c3c !important;
                background-color: #fef5f5 !important;
                box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1) !important;
            }
            
            .form-group input.success,
            .form-group select.success,
            .form-group textarea.success {
                border-color: #27ae60 !important;
                background-color: #f5fef7 !important;
                box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1) !important;
            }
            
            .submit-btn:disabled {
                opacity: 0.6 !important;
                cursor: not-allowed !important;
                transform: none !important;
                box-shadow: none !important;
            }
            
            .submit-btn.loading {
                position: relative;
                color: transparent !important;
            }
            
            .submit-btn.loading::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top: 2px solid white;
                animation: spin 1s linear infinite;
            }
            
            .checkbox-wrapper input[type="checkbox"].error + .checkbox-label {
                color: #e74c3c;
            }
            
            .checkbox-wrapper.error {
                border-color: #e74c3c;
                background-color: #fef5f5;
            }
            
            .field-error-message {
                animation: slideDown 0.3s ease-in;
            }
            
            .field-warning-message {
                animation: slideDown 0.3s ease-in;
            }
            
            /* Focus styles for accessibility */
            .form-group input:focus-visible,
            .form-group select:focus-visible,
            .form-group textarea:focus-visible {
                outline: 2px solid #1976d2;
                outline-offset: 2px;
            }
            
            .submit-btn:focus-visible {
                outline: 2px solid #1976d2;
                outline-offset: 2px;
            }
            
            /* High contrast mode support */
            @media (prefers-contrast: high) {
                .form-group input,
                .form-group select,
                .form-group textarea {
                    border-width: 2px;
                }
            }
            
            /* Reduced motion support */
            @media (prefers-reduced-motion: reduce) {
                * {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                }
            }
        `;
    document.head.appendChild(style);
  }

  // Initialize everything
  addStyles();
  initializeForm();

  // Add console log for debugging
  console.log("Contact Step 2 form initialized successfully");

  // Expose validation function globally for debugging
  window.contactFormDebug = {
    validateForm: validateForm,
    validateField: validateField,
    showFieldError: showFieldError,
    clearFieldError: clearFieldError,
    formData: () => {
      const formData = new FormData(form);
      const data = {};
      formData.forEach((value, key) => {
        data[key] = value;
      });
      return data;
    },
  };
});
