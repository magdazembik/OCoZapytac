// Main JavaScript functionality

// Import Lucide icons library
const lucide = require("lucide")

// Initialize Lucide icons
document.addEventListener("DOMContentLoaded", () => {
  lucide.createIcons()
})

// Mobile menu toggle
document.addEventListener("DOMContentLoaded", () => {
  const mobileMenuToggle = document.getElementById("mobileMenuToggle")
  const navMenu = document.querySelector(".nav-menu")

  if (mobileMenuToggle && navMenu) {
    mobileMenuToggle.addEventListener("click", () => {
      navMenu.classList.toggle("active")
      mobileMenuToggle.classList.toggle("active")
    })
  }

  // Close mobile menu when clicking on a link
  const navLinks = document.querySelectorAll(".nav-link")
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      navMenu.classList.remove("active")
      mobileMenuToggle.classList.remove("active")
    })
  })

  // Close mobile menu when clicking outside
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".nav") && navMenu.classList.contains("active")) {
      navMenu.classList.remove("active")
      mobileMenuToggle.classList.remove("active")
    }
  })
})

// Smooth scroll to newsletter
function scrollToNewsletter() {
  const newsletter = document.getElementById("newsletter")
  if (newsletter) {
    newsletter.scrollIntoView({ behavior: "smooth" })
  }
}

// HTMX response handlers
document.addEventListener("htmx:responseError", (event) => {
  console.error("HTMX request failed:", event.detail)
  const target = event.detail.target
  if (target) {
    target.innerHTML = '<div class="error-message">Wystąpił błąd podczas ładowania danych.</div>'
  }
})

document.addEventListener("htmx:afterRequest", (event) => {
  // Re-initialize Lucide icons after HTMX content loads
  lucide.createIcons()
})

// Newsletter form success handler
document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.target.id === "newsletter-result") {
    const xhr = event.detail.xhr
    const target = event.detail.target

    if (xhr.status === 200) {
      target.innerHTML = '<div class="success-message">Dziękujemy za zapisanie się do newslettera!</div>'
      // Clear the form
      const form = target.closest("section").querySelector("form")
      if (form) {
        form.reset()
      }
    } else {
      target.innerHTML = '<div class="error-message">Wystąpił błąd. Spróbuj ponownie.</div>'
    }
  }
})

// Contact form success handler
document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.target.id === "contact-result") {
    const xhr = event.detail.xhr
    const target = event.detail.target

    if (xhr.status === 200) {
      target.innerHTML = '<div class="success-message">Dziękujemy za wiadomość! Odpowiemy w ciągu 24 godzin.</div>'
      // Clear the form
      const form = target.closest(".contact-form-container").querySelector("form")
      if (form) {
        form.reset()
      }
    } else {
      target.innerHTML =
        '<div class="error-message">Wystąpił błąd podczas wysyłania wiadomości. Spróbuj ponownie.</div>'
    }
  }
})

// Featured articles loading handler
document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.target.id === "featuredArticles") {
    const xhr = event.detail.xhr
    const target = event.detail.target

    if (xhr.status === 200) {
      try {
        const articles = JSON.parse(xhr.responseText)
        if (articles && articles.length > 0) {
          target.innerHTML = articles.map((article) => createArticleCard(article)).join("")
        } else {
          target.innerHTML = '<div class="loading">Brak artykułów do wyświetlenia.</div>'
        }
      } catch (error) {
        console.error("Error parsing articles:", error)
        target.innerHTML = '<div class="error-message">Błąd podczas ładowania artykułów.</div>'
      }
    }
  }
})

// Smooth scrolling for anchor links
document.addEventListener("click", (event) => {
  if (event.target.matches('a[href^="#"]')) {
    event.preventDefault()
    const targetId = event.target.getAttribute("href").substring(1)
    const targetElement = document.getElementById(targetId)

    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: "smooth",
        block: "start",
      })
    }
  }
})

// Add loading states to buttons
document.addEventListener("htmx:beforeRequest", (event) => {
  const trigger = event.detail.elt
  if (trigger.tagName === "BUTTON" || trigger.tagName === "INPUT") {
    trigger.disabled = true
    const originalText = trigger.textContent || trigger.value
    trigger.dataset.originalText = originalText
    trigger.textContent = "Ładowanie..."
  }
})

document.addEventListener("htmx:afterRequest", (event) => {
  const trigger = event.detail.elt
  if (trigger.tagName === "BUTTON" || trigger.tagName === "INPUT") {
    trigger.disabled = false
    if (trigger.dataset.originalText) {
      trigger.textContent = trigger.dataset.originalText
      delete trigger.dataset.originalText
    }
  }
})

// API helper functions
const API_BASE_URL = "http://localhost:8000/api/v1"

async function fetchAPI(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("API request failed:", error)
    throw error
  }
}

// Format date helper
function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString("pl-PL", {
    year: "numeric",
    month: "long",
    day: "numeric",
  })
}

// Create article card HTML
function createArticleCard(article) {
  return `
        <article class="article-card">
            <div class="article-card-content">
                <span class="article-card-category">${article.category}</span>
                <h3 class="article-card-title">
                    <a href="article.html?slug=${article.slug}">${article.title}</a>
                </h3>
                <p class="article-card-excerpt">${article.excerpt}</p>
                <div class="article-card-meta">
                    <span class="article-card-author">Autor: ${article.author}</span>
                    <span class="article-card-date">${formatDate(article.created_at)}</span>
                </div>
            </div>
        </article>
    `
}

// Intersection Observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("animate-in")
    }
  })
}, observerOptions)

// Observe elements for animation
document.addEventListener("DOMContentLoaded", () => {
  const animateElements = document.querySelectorAll(".feature-card, .about-card, .article-card")
  animateElements.forEach((el) => observer.observe(el))
})

// Floating shapes animation
function initFloatingShapes() {
  const shapes = document.querySelectorAll(".floating-shape")
  shapes.forEach((shape, index) => {
    const randomDelay = Math.random() * 10
    const randomDuration = 15 + Math.random() * 10
    shape.style.animationDelay = `${randomDelay}s`
    shape.style.animationDuration = `${randomDuration}s`
  })
}

document.addEventListener("DOMContentLoaded", initFloatingShapes)

// Scroll indicator
function updateScrollIndicator() {
  const scrollIndicator = document.querySelector(".scroll-indicator")
  if (scrollIndicator) {
    const scrolled = window.pageYOffset
    const rate = scrolled * -0.5
    scrollIndicator.style.transform = `translateX(-50%) translateY(${rate}px)`

    if (scrolled > 100) {
      scrollIndicator.style.opacity = "0"
    } else {
      scrollIndicator.style.opacity = "1"
    }
  }
}

window.addEventListener("scroll", updateScrollIndicator)
