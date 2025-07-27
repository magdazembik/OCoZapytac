// Article page functionality
document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search)
  const articleSlug = urlParams.get("slug")

  if (articleSlug) {
    loadArticle(articleSlug)
  } else {
    showError("Nie znaleziono artykułu.")
  }
})

async function loadArticle(slug) {
  try {
    const article = await fetchAPI(`/articles/slug/${slug}`)

    if (article) {
      displayArticle(article)
      loadRelatedArticles(article.category, article.id)
    } else {
      showError("Artykuł nie został znaleziony.")
    }
  } catch (error) {
    console.error("Error loading article:", error)
    showError("Błąd podczas ładowania artykułu.")
  }
}

function displayArticle(article) {
  // Update page title and meta
  document.title = `${article.title} - Co Zapytać`
  document.getElementById("articleTitle").textContent = `${article.title} - Co Zapytać`
  document.getElementById("articleDescription").content = article.excerpt
  document.getElementById("breadcrumbTitle").textContent = article.title

  // Create article HTML
  const articleHTML = `
        <div class="article-header">
            <span class="article-category">${article.category}</span>
            <h1 class="article-title">${article.title}</h1>
            <div class="article-meta">
                <span class="article-author">Autor: ${article.author}</span>
                <span class="article-date">${formatDate(article.created_at)}</span>
                <span class="article-read-time">Czas czytania: ${article.read_time}</span>
            </div>
        </div>
        <div class="article-content">
            ${article.content}
        </div>
    `

  document.getElementById("articleContent").innerHTML = articleHTML
}

async function loadRelatedArticles(category, currentArticleId) {
  try {
    const params = new URLSearchParams({
      category: category,
      limit: 3,
      exclude: currentArticleId,
    })

    const relatedArticles = await fetchAPI(`/articles/?${params.toString()}`)

    if (relatedArticles && relatedArticles.length > 0) {
      const relatedHTML = relatedArticles
        .map(
          (article) => `
                <div class="related-article-card">
                    <h4 class="related-article-title">
                        <a href="article.html?slug=${article.slug}">${article.title}</a>
                    </h4>
                    <p class="related-article-excerpt">${article.excerpt}</p>
                </div>
            `,
        )
        .join("")

      document.getElementById("relatedArticles").innerHTML = relatedHTML
    } else {
      document.getElementById("relatedArticles").innerHTML = '<div class="loading">Brak powiązanych artykułów.</div>'
    }
  } catch (error) {
    console.error("Error loading related articles:", error)
    document.getElementById("relatedArticles").innerHTML =
      '<div class="error-message">Błąd podczas ładowania powiązanych artykułów.</div>'
  }
}

function showError(message) {
  document.getElementById("articleContent").innerHTML = `
        <div class="error-message">
            <h2>Błąd</h2>
            <p>${message}</p>
            <a href="/articles" class="btn btn-primary">Powrót do artykułów</a>
        </div>
    `
}

// Handle article content HTMX response (if using HTMX instead of JS)
document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.target.id === "articleContent") {
    const xhr = event.detail.xhr
    const target = event.detail.target

    if (xhr.status === 200) {
      try {
        const article = JSON.parse(xhr.responseText)
        displayArticle(article)
      } catch (error) {
        console.error("Error parsing article:", error)
        showError("Błąd podczas ładowania artykułu.")
      }
    } else if (xhr.status === 404) {
      showError("Artykuł nie został znaleziony.")
    } else {
      showError("Błąd podczas ładowania artykułu.")
    }
  }
})

// Handle related articles HTMX response
document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.target.id === "relatedArticles") {
    const xhr = event.detail.xhr
    const target = event.detail.target

    if (xhr.status === 200) {
      try {
        const articles = JSON.parse(xhr.responseText)
        if (articles && articles.length > 0) {
          const relatedHTML = articles
            .map(
              (article) => `
                        <div class="related-article-card">
                            <h4 class="related-article-title">
                                <a href="article.html?slug=${article.slug}">${article.title}</a>
                            </h4>
                            <p class="related-article-excerpt">${article.excerpt}</p>
                        </div>
                    `,
            )
            .join("")
          target.innerHTML = relatedHTML
        } else {
          target.innerHTML = '<div class="loading">Brak powiązanych artykułów.</div>'
        }
      } catch (error) {
        console.error("Error parsing related articles:", error)
        target.innerHTML = '<div class="error-message">Błąd podczas ładowania powiązanych artykułów.</div>'
      }
    }
  }
})

// Declare fetchAPI and formatDate functions
function fetchAPI(url) {
  return fetch(url).then((response) => response.json())
}

function formatDate(dateString) {
  const date = new Date(dateString)
  const options = { year: "numeric", month: "long", day: "numeric" }
  return date.toLocaleDateString("pl-PL", options)
}
