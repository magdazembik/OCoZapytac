// Articles page functionality

let allArticles = []
let filteredArticles = []
let currentCategory = "all"
let currentPage = 1
let currentSearch = ""
let isLoading = false

document.addEventListener("DOMContentLoaded", () => {
  const articlesGrid = document.getElementById("articlesGrid")
  const searchInput = document.getElementById("searchInput")
  const searchButton = document.getElementById("searchButton")
  const filterButtons = document.querySelectorAll(".filter-btn")
  const loadMoreBtn = document.getElementById("loadMoreBtn")
  const loadMoreContainer = document.getElementById("loadMoreContainer")

  // Load initial articles
  loadArticles()

  // Search functionality
  if (searchButton && searchInput) {
    searchButton.addEventListener("click", handleSearch)
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        handleSearch()
      }
    })
  }

  // Filter functionality
  filterButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Update active filter
      filterButtons.forEach((btn) => btn.classList.remove("active"))
      this.classList.add("active")

      currentCategory = this.dataset.category
      currentPage = 1
      loadArticles(true)
    })
  })

  // Load more functionality
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener("click", () => {
      currentPage++
      loadArticles(false)
    })
  }

  // Check URL parameters for initial filters
  const urlParams = new URLSearchParams(window.location.search)
  const categoryParam = urlParams.get("category")
  if (categoryParam) {
    currentCategory = categoryParam
    // Update active filter button
    filterButtons.forEach((btn) => {
      btn.classList.remove("active")
      if (btn.dataset.category === categoryParam) {
        btn.classList.add("active")
      }
    })
  }

  function handleSearch() {
    currentSearch = searchInput.value.trim()
    currentPage = 1
    loadArticles(true)
  }

  async function loadArticles(replace = false) {
    if (isLoading) return

    isLoading = true

    try {
      // Build query parameters
      const params = new URLSearchParams({
        page: currentPage,
        limit: 12,
      })

      if (currentCategory !== "all") {
        params.append("category", currentCategory)
      }

      if (currentSearch) {
        params.append("search", currentSearch)
      }

      // Show loading state
      if (replace) {
        articlesGrid.innerHTML = '<div class="loading">Ładowanie artykułów...</div>'
      } else {
        loadMoreBtn.textContent = "Ładowanie..."
        loadMoreBtn.disabled = true
      }

      const response = await fetchAPI(`/articles/?${params.toString()}`)

      if (response && Array.isArray(response)) {
        if (replace) {
          articlesGrid.innerHTML = ""
        }

        if (response.length === 0 && currentPage === 1) {
          articlesGrid.innerHTML = '<div class="loading">Nie znaleziono artykułów.</div>'
          loadMoreContainer.style.display = "none"
        } else {
          // Add articles to grid
          response.forEach((article) => {
            const articleElement = document.createElement("div")
            articleElement.innerHTML = createArticleCard(article)
            articlesGrid.appendChild(articleElement.firstElementChild)
          })

          // Show/hide load more button
          if (response.length < 12) {
            loadMoreContainer.style.display = "none"
          } else {
            loadMoreContainer.style.display = "block"
          }
        }
      } else {
        throw new Error("Invalid response format")
      }
    } catch (error) {
      console.error("Error loading articles:", error)
      if (replace) {
        articlesGrid.innerHTML = '<div class="error-message">Błąd podczas ładowania artykułów.</div>'
      } else {
        // Show error but keep existing articles
        const errorDiv = document.createElement("div")
        errorDiv.className = "error-message"
        errorDiv.textContent = "Błąd podczas ładowania kolejnych artykułów."
        articlesGrid.appendChild(errorDiv)
      }
      loadMoreContainer.style.display = "none"
    } finally {
      isLoading = false
      loadMoreBtn.textContent = "Załaduj więcej artykułów"
      loadMoreBtn.disabled = false
    }
  }
})

// Handle articles grid HTMX response
document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.target.id === "articlesGrid") {
    const xhr = event.detail.xhr
    const target = event.detail.target

    if (xhr.status === 200) {
      try {
        const articles = JSON.parse(xhr.responseText)
        if (articles && articles.length > 0) {
          target.innerHTML = articles.map((article) => createArticleCard(article)).join("")

          // Show load more button if there might be more articles
          const loadMoreContainer = document.getElementById("loadMoreContainer")
          if (loadMoreContainer && articles.length >= 12) {
            loadMoreContainer.style.display = "block"
          }
        } else {
          target.innerHTML = '<div class="loading">Nie znaleziono artykułów.</div>'
        }
      } catch (error) {
        console.error("Error parsing articles:", error)
        target.innerHTML = '<div class="error-message">Błąd podczas ładowania artykułów.</div>'
      }
    }
  }
})

// Search functionality
function searchArticles() {
  const searchTerm = document.getElementById("search-input").value.toLowerCase()

  filteredArticles = allArticles.filter((article) => {
    const matchesSearch =
      article.title.toLowerCase().includes(searchTerm) || article.excerpt.toLowerCase().includes(searchTerm)
    const matchesCategory = currentCategory === "all" || article.category === currentCategory
    return matchesSearch && matchesCategory
  })

  renderArticles(filteredArticles)
}

// Category filtering
function filterByCategory(category) {
  currentCategory = category

  // Update active button
  document.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.classList.remove("active")
  })
  document.querySelector(`[data-category="${category}"]`).classList.add("active")

  // Filter articles
  const searchTerm = document.getElementById("search-input").value.toLowerCase()

  filteredArticles = allArticles.filter((article) => {
    const matchesSearch =
      searchTerm === "" ||
      article.title.toLowerCase().includes(searchTerm) ||
      article.excerpt.toLowerCase().includes(searchTerm)
    const matchesCategory = category === "all" || article.category === category
    return matchesSearch && matchesCategory
  })

  renderArticles(filteredArticles)
}

// Render articles
function renderArticles(articles) {
  const container = document.getElementById("articles-container")
  const noResults = document.getElementById("no-results")

  if (!articles || articles.length === 0) {
    container.innerHTML = ""
    noResults.classList.remove("hidden")
    return
  }

  noResults.classList.add("hidden")
  container.innerHTML = `
        <div class="articles-grid-container">
            ${articles
              .map(
                (article) => `
                <article class="article-card">
                    <div class="article-image">
                        <img src="${article.image_url || "/placeholder.svg?height=300&width=500"}" 
                             alt="${article.title}">
                        <div class="article-category">
                            <span class="category-badge">${article.category || "Artykuł"}</span>
                        </div>
                    </div>
                    <div class="article-content">
                        <h3 class="article-title">
                            <a href="artykul.html?slug=${article.slug}">${article.title}</a>
                        </h3>
                        <p class="article-excerpt">${article.excerpt || ""}</p>
                        <div class="article-meta">
                            <div class="meta-item">
                                <i data-lucide="calendar"></i>
                                <span>${new Date(article.published_at).toLocaleDateString()}</span>
                            </div>
                            <div class="meta-item">
                                <i data-lucide="clock"></i>
                                <span>${article.read_time || "5 min"}</span>
                            </div>
                        </div>
                    </div>
                    <div class="article-footer">
                        <a href="artykul.html?slug=${article.slug}" class="btn btn-primary">
                            Czytaj więcej
                            <i data-lucide="arrow-right"></i>
                        </a>
                    </div>
                </article>
            `,
              )
              .join("")}
        </div>
    `

  window.lucide.createIcons()
}

// HTMX response handler for articles
document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.target.id === "articles-container") {
    try {
      const response = JSON.parse(event.detail.xhr.responseText)
      allArticles = response
      filteredArticles = response
      renderArticles(response)
    } catch (error) {
      console.error("Error parsing articles response:", error)
      document.getElementById("articles-container").innerHTML = `
                <div class="error-message">
                    <i data-lucide="alert-circle"></i>
                    <h3>Błąd ładowania artykułów</h3>
                    <p>Spróbuj odświeżyć stronę lub skontaktuj się z nami.</p>
                </div>
            `
      window.lucide.createIcons()
    }
  }
})

function createArticleCard(article) {
  return `
        <article class="article-card">
            <div class="article-image">
                <img src="${article.image_url || "/placeholder.svg?height=300&width=500"}" 
                     alt="${article.title}">
                <div class="article-category">
                    <span class="category-badge">${article.category || "Artykuł"}</span>
                </div>
            </div>
            <div class="article-content">
                <h3 class="article-title">
                    <a href="artykul.html?slug=${article.slug}">${article.title}</a>
                </h3>
                <p class="article-excerpt">${article.excerpt || ""}</p>
                <div class="article-meta">
                    <div class="meta-item">
                        <i data-lucide="calendar"></i>
                        <span>${new Date(article.published_at).toLocaleDateString()}</span>
                    </div>
                    <div class="meta-item">
                        <i data-lucide="clock"></i>
                        <span>${article.read_time || "5 min"}</span>
                    </div>
                </div>
            </div>
            <div class="article-footer">
                <a href="artykul.html?slug=${article.slug}" class="btn btn-primary">
                    Czytaj więcej
                    <i data-lucide="arrow-right"></i>
                </a>
            </div>
        </article>
    `
}

async function fetchAPI(url) {
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error("Network response was not ok")
  }
  return response.json()
}
