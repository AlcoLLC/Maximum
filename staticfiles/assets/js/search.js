document.addEventListener("DOMContentLoaded", function () {
  const cancelBtn = document.querySelector(".page-header .cancel-button");
  const searchInput = document.querySelector(".search-input");
  const searchForm = document.querySelector(".search-form");
  if (cancelBtn) {
    cancelBtn.addEventListener("click", function () {
      searchInput.value = "";
      searchInput.focus();
      const url = new URL(window.location);
      url.searchParams.delete("search");
      url.searchParams.delete("page");
      window.location.href = url.toString();
    });
  }
  if (searchInput) {
    let searchTimeout;
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(function () {
        if (
          searchInput.value.trim().length > 2 ||
          searchInput.value.trim().length === 0
        ) {
          searchForm.submit();
        }
      }, 500);
    });
  }
  const paginationNumbers = document.querySelectorAll(".page-number");
  const prevBtn = document.getElementById("prevPage");
  const nextBtn = document.getElementById("nextPage");
  paginationNumbers.forEach(function (pageLink) {
    pageLink.addEventListener("click", function (e) {
      e.preventDefault();
      const pageNum = this.getAttribute("data-page");
      goToPage(pageNum);
    });
  });
  if (prevBtn && !prevBtn.disabled) {
    prevBtn.addEventListener("click", function () {
      const pageNum = this.getAttribute("data-page");
      if (pageNum) {
        goToPage(pageNum);
      }
    });
  }
  if (nextBtn && !nextBtn.disabled) {
    nextBtn.addEventListener("click", function () {
      const pageNum = this.getAttribute("data-page");
      if (pageNum) {
        goToPage(pageNum);
      }
    });
  }
  function goToPage(pageNum) {
    const url = new URL(window.location);
    url.searchParams.set("page", pageNum);
    window.location.href = url.toString();
  }
  if (searchInput) {
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        if (searchInput.value.trim().length > 0) {
          searchForm.submit();
        }
      }
      if (e.key === "Escape") {
        searchInput.value = "";
        searchInput.blur();
      }
    });
  }
  if (searchInput && !searchInput.value) {
    searchInput.focus();
  }
  const queryElement = document.querySelector("[data-search-query]");
  const query = queryElement
    ? queryElement.getAttribute("data-search-query")
    : "";
  if (query && query.trim()) {
    highlightSearchTerms(query.trim());
  }
  function highlightSearchTerms(searchQuery) {
    const resultContents = document.querySelectorAll(
      ".result-text h2, .result-text .result-description"
    );
    const regex = new RegExp(
      `(${searchQuery.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`,
      "gi"
    );
    resultContents.forEach(function (element) {
      if (element.innerHTML && !element.querySelector(".highlight")) {
        element.innerHTML = element.innerHTML.replace(
          regex,
          '<mark class="highlight">$1</mark>'
        );
      }
    });
  }
});
