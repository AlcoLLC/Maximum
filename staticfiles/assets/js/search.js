// Search functionality - Updated for multilingual support
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-form');
    const searchButton = document.querySelector('.search-button');
    const searchInput = document.querySelector('.search-form input[name="search"]');

    // Function to get current language from URL
    function getCurrentLanguage() {
        const path = window.location.pathname;
        const supportedLangs = ['en', 'de', 'es', 'fr', 'it', 'zh-hans'];
        
        for (let lang of supportedLangs) {
            if (path.startsWith(`/${lang}/`) || path === `/${lang}`) {
                return lang;
            }
        }
        return 'en'; // Default to English
    }

    // Function to build search URL with proper language prefix
    function buildSearchUrl(query) {
        const currentLang = getCurrentLanguage();
        const encodedQuery = encodeURIComponent(query);
        
        if (currentLang === 'en') {
            return `/search/?search=${encodedQuery}`;
        } else {
            return `/${currentLang}/search/?search=${encodedQuery}`;
        }
    }

    // Handle search form submission
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            performSearch();
        });
    }

    // Handle search button click
    if (searchButton) {
        searchButton.addEventListener('click', function(e) {
            e.preventDefault();
            performSearch();
        });
    }

    // Handle enter key press in search input
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });
    }

    function performSearch() {
        const query = searchInput.value.trim();
        if (query) {
            // Redirect to search page with query and proper language
            window.location.href = buildSearchUrl(query);
        }
    }
});