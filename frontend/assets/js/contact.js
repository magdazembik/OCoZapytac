// Contact page functionality

// Declare showNotification function
function showNotification(message, type) {
  console.log(`Notification: ${message} (Type: ${type})`)
}

// FAQ toggle functionality
function toggleFAQ(button) {
  const faqItem = button.parentElement
  const answer = faqItem.querySelector(".faq-answer")
  const icon = button.querySelector("i")

  // Close all other FAQ items
  document.querySelectorAll(".faq-item").forEach((item) => {
    if (item !== faqItem) {
      const otherAnswer = item.querySelector(".faq-answer")
      const otherButton = item.querySelector(".faq-question")
      const otherIcon = otherButton.querySelector("i")

      otherAnswer.classList.remove("active")
      otherButton.classList.remove("active")
    }
  })

  // Toggle current FAQ item
  answer.classList.toggle("active")
  button.classList.toggle("active")
}

// Form validation
function validateForm() {
  const form = document.getElementById("contact-form")
  const name = form.querySelector("#name").value.trim()
  const email = form.querySelector("#email").value.trim()
  const message = form.querySelector("#message").value.trim()

  if (!name || !email || !message) {
    showNotification("Proszę wypełnić wszystkie wymagane pola", "error")
    return false
  }

  if (!emailRegex.test(email)) {
    showNotification("Proszę podać prawidłowy adres email", "error")
    return false
  }

  return true
}

// Email validation
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// HTMX event handlers
document.addEventListener("htmx:beforeRequest", (event) => {
  if (event.detail.target.id === "contact-form") {
    // Show loading state
    const loadingIndicator = document.getElementById("form-loading")
    const submitButton = document.querySelector(".btn-submit")

    if (loadingIndicator) {
      loadingIndicator.classList.remove("hidden")
    }

    if (submitButton) {
      submitButton.disabled = true
      submitButton.querySelector(".btn-text").textContent = "Wysyłanie..."
    }
  }
})

document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.target.id === "contact-form") {
    const loadingIndicator = document.getElementById("form-loading")

    if (loadingIndicator) {
      loadingIndicator.classList.add("hidden")
    }

    if (event.detail.xhr.status === 200) {
      showContactSuccess()
    } else {
      showContactError()
      resetSubmitButton()
    }

    // Re-initialize Lucide icons
    if (window.lucide) {
      window.lucide.createIcons()
    }
  }
})

// Success handler
function showContactSuccess() {
  const form = document.getElementById("contact-form")
  if (form) {
    form.innerHTML = `
            <div class="contact-success">
                <div class="success-icon">
                    <i data-lucide="check-circle"></i>
                </div>
                <h3>Dziękujemy za wiadomość!</h3>
                <p>Otrzymaliśmy Twoją wiadomość i odpowiemy najszybciej jak to możliwe, zazwyczaj w ciągu 24 godzin.</p>
                <button class="btn btn-outline" onclick="resetContactForm()">
                    Wyślij kolejną wiadomość
                </button>
            </div>
        `

    if (window.lucide) {
      window.lucide.createIcons()
    }

    showNotification("Wiadomość została wysłana pomyślnie!", "success")
  }
}

// Error handler
function showContactError() {
  showNotification("Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.", "error")
}

// Reset submit button
function resetSubmitButton() {
  const submitButton = document.querySelector(".btn-submit")
  if (submitButton) {
    submitButton.disabled = false
    submitButton.querySelector(".btn-text").textContent = "Wyślij wiadomość"
  }
}

// Reset form to initial state
function resetContactForm() {
  const formContainer = document.getElementById("contact-form").parentElement

  formContainer.innerHTML = `
        <div class="contact-form-header">
            <h2>Napisz do nas</h2>
            <p>Wypełnij formularz poniżej, a odpowiemy najszybciej jak to możliwe.</p>
        </div>

        <form id="contact-form" 
              class="contact-form"
              hx-post="http://localhost:8000/api/v1/contact/"
              hx-target="#contact-form"
              hx-swap="outerHTML"
              hx-indicator="#form-loading">
            
            <div class="form-group">
                <label for="name" class="form-label">
                    <i data-lucide="user"></i>
                    Imię i nazwisko *
                </label>
                <input type="text" 
                       id="name" 
                       name="name" 
                       required 
                       class="form-input"
                       placeholder="np. Jan Kowalski">
            </div>

            <div class="form-group">
                <label for="email" class="form-label">
                    <i data-lucide="mail"></i>
                    Adres email *
                </label>
                <input type="email" 
                       id="email" 
                       name="email" 
                       required 
                       class="form-input"
                       placeholder="np. jan@example.com">
            </div>

            <div class="form-group">
                <label for="subject" class="form-label">
                    <i data-lucide="tag"></i>
                    Temat
                </label>
                <select id="subject" name="subject" class="form-select">
                    <option value="">Wybierz temat...</option>
                    <option value="Pytanie o optymalizację podatkową">Pytanie o optymalizację podatkową</option>
                    <option value="Pomoc w przygotowaniu pytań do księgowego">Pomoc w przygotowaniu pytań do księgowego</option>
                    <option value="Współpraca">Współpraca</option>
                    <option value="Problem techniczny">Problem techniczny</option>
                    <option value="Sugestia artykułu">Sugestia artykułu</option>
                    <option value="Inne">Inne</option>
                </select>
            </div>

            <div class="form-group">
                <label for="message" class="form-label">
                    <i data-lucide="message-square"></i>
                    Wiadomość *
                </label>
                <textarea id="message" 
                          name="message" 
                          required 
                          rows="6" 
                          class="form-textarea"
                          placeholder="Opisz swoje pytanie lub problem..."></textarea>
            </div>

            <div class="form-footer">
                <div class="form-disclaimer">
                    <i data-lucide="shield-check"></i>
                    <span>Twoje dane są bezpieczne i nie będą udostępniane osobom trzecim.</span>
                </div>
                
                <button type="submit" class="btn btn-primary btn-large btn-submit">
                    <span class="btn-text">Wyślij wiadomość</span>
                    <i data-lucide="send"></i>
                </button>
            </div>

            <div id="form-loading" class="form-loading hidden">
                <div class="spinner"></div>
                <span>Wysyłanie wiadomości...</span>
            </div>
        </form>
    `

  if (window.lucide) {
    window.lucide.createIcons()
  }
}

// Character counter for textarea (optional enhancement)
function addCharacterCounter() {
  const textarea = document.getElementById("message")
  if (textarea) {
    const maxLength = 1000
    const counter = document.createElement("div")
    counter.className = "character-counter"
    counter.style.cssText = `
            text-align: right;
            font-size: 0.875rem;
            color: var(--gray-500);
            margin-top: var(--space-2);
        `

    textarea.parentElement.appendChild(counter)

    function updateCounter() {
      const remaining = maxLength - textarea.value.length
      counter.textContent = `${remaining} znaków pozostało`

      if (remaining < 100) {
        counter.style.color = "var(--red-500)"
      } else {
        counter.style.color = "var(--gray-500)"
      }
    }

    textarea.addEventListener("input", updateCounter)
    textarea.setAttribute("maxlength", maxLength)
    updateCounter()
  }
}

// Auto-resize textarea
function autoResizeTextarea() {
  const textarea = document.getElementById("message")
  if (textarea) {
    textarea.addEventListener("input", function () {
      this.style.height = "auto"
      this.style.height = this.scrollHeight + "px"
    })
  }
}

// Initialize contact page features
document.addEventListener("DOMContentLoaded", () => {
  // Add character counter and auto-resize to textarea
  setTimeout(() => {
    addCharacterCounter()
    autoResizeTextarea()
  }, 100)

  // Smooth scroll for FAQ items
  document.querySelectorAll(".faq-question").forEach((button) => {
    button.addEventListener("click", () => {
      setTimeout(() => {
        button.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
        })
      }, 300)
    })
  })

  // Handle contact form HTMX response with better error handling
  const contactForm = document.querySelector(".contact-form")

  if (contactForm) {
    // Add form validation
    contactForm.addEventListener("submit", (event) => {
      if (!validateContactForm()) {
        event.preventDefault()
      }
    })

    // Add real-time validation
    const inputs = contactForm.querySelectorAll("input, select, textarea")
    inputs.forEach((input) => {
      input.addEventListener("blur", function () {
        validateField(this)
      })
    })
  }
})

function validateContactForm() {
  const form = document.querySelector(".contact-form")
  const name = form.querySelector("#name")
  const email = form.querySelector("#email")
  const subject = form.querySelector("#subject")
  const message = form.querySelector("#message")

  let isValid = true

  // Clear previous errors
  clearFieldErrors()

  // Validate name
  if (!name.value.trim()) {
    showFieldError(name, "Imię i nazwisko jest wymagane.")
    isValid = false
  }

  // Validate email
  if (!email.value.trim()) {
    showFieldError(email, "Adres e-mail jest wymagany.")
    isValid = false
  } else if (!emailRegex.test(email.value)) {
    showFieldError(email, "Podaj prawidłowy adres e-mail.")
    isValid = false
  }

  // Validate subject
  if (!subject.value) {
    showFieldError(subject, "Wybierz temat wiadomości.")
    isValid = false
  }

  // Validate message
  if (!message.value.trim()) {
    showFieldError(message, "Wiadomość jest wymagana.")
    isValid = false
  } else if (message.value.trim().length < 10) {
    showFieldError(message, "Wiadomość musi mieć co najmniej 10 znaków.")
    isValid = false
  }

  return isValid
}

function validateField(field) {
  const fieldName = field.name
  const value = field.value.trim()

  clearFieldError(field)

  switch (fieldName) {
    case "name":
      if (!value) {
        showFieldError(field, "Imię i nazwisko jest wymagane.")
        return false
      }
      break

    case "email":
      if (!value) {
        showFieldError(field, "Adres e-mail jest wymagany.")
        return false
      } else if (!emailRegex.test(value)) {
        showFieldError(field, "Podaj prawidłowy adres e-mail.")
        return false
      }
      break

    case "subject":
      if (!value) {
        showFieldError(field, "Wybierz temat wiadomości.")
        return false
      }
      break

    case "message":
      if (!value) {
        showFieldError(field, "Wiadomość jest wymagana.")
        return false
      } else if (value.length < 10) {
        showFieldError(field, "Wiadomość musi mieć co najmniej 10 znaków.")
        return false
      }
      break
  }

  return true
}

function showFieldError(field, message) {
  const formGroup = field.closest(".form-group")
  const existingError = formGroup.querySelector(".field-error")

  if (existingError) {
    existingError.remove()
  }

  const errorElement = document.createElement("div")
  errorElement.className = "field-error"
  errorElement.textContent = message
  errorElement.style.color = "#dc2626"
  errorElement.style.fontSize = "0.875rem"
  errorElement.style.marginTop = "0.25rem"

  formGroup.appendChild(errorElement)
  field.style.borderColor = "#dc2626"
}

function clearFieldError(field) {
  const formGroup = field.closest(".form-group")
  const existingError = formGroup.querySelector(".field-error")

  if (existingError) {
    existingError.remove()
  }

  field.style.borderColor = "#d1d5db"
}

function clearFieldErrors() {
  const errors = document.querySelectorAll(".field-error")
  errors.forEach((error) => error.remove())

  const inputs = document.querySelectorAll(".contact-form input, .contact-form select, .contact-form textarea")
  inputs.forEach((input) => {
    input.style.borderColor = "#d1d5db"
  })
}

// Form analytics (optional - for tracking form interactions)
function trackFormInteraction(action, field = null) {
  // This is where you could add analytics tracking
  console.log(`Form interaction: ${action}`, field)
}

// Add form interaction tracking
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contact-form")
  if (form) {
    // Track form start
    form.addEventListener(
      "focusin",
      () => {
        trackFormInteraction("form_started")
      },
      { once: true },
    )

    // Track field interactions
    form.querySelectorAll("input, select, textarea").forEach((field) => {
      field.addEventListener("blur", () => {
        if (field.value.trim()) {
          trackFormInteraction("field_completed", field.name)
        }
      })
    })
  }
})
