document.addEventListener('DOMContentLoaded', function () {
  // =================
  // MOBILE MENU FUNCTIONALITY
  // =================
  let isMobileMenuInitialized = false;

  function initializeMobileMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobile-menu');
    const hamburgerIcon = hamburger.querySelector('i');
    let isProcessingClick = false;

    hamburger.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      if (isProcessingClick) {
        return;
      }
      isProcessingClick = true;

      const isActive = mobileMenu.classList.toggle('active');
      hamburger.classList.toggle('active');
      document.body.style.overflow = isActive ? 'hidden' : '';

      // Icon change
      if (hamburgerIcon) {
        hamburgerIcon.className = isActive ? 'fas fa-xmark' : 'fas fa-bars';
      }

      setTimeout(() => {
        isProcessingClick = false;
      }, 200);
    });

    document.addEventListener('click', function (e) {
      if (
        mobileMenu.classList.contains('active') &&
        !mobileMenu.contains(e.target) &&
        !hamburger.contains(e.target)
      ) {
        mobileMenu.classList.remove('active');
        hamburger.classList.remove('active');
        document.body.style.overflow = '';

        if (hamburgerIcon) {
          hamburgerIcon.className = 'fas fa-bars';
        }
      }
    });
  }

  // Desktop language dropdown elements
  const langDropdownBtn = document.querySelector('.language-dropdown .lang-dropdown-btn');
  const languageDropdown = document.getElementById('languageDropdown');
  const desktopLangOptions = document.querySelectorAll('#languageDropdown .lang-option');

  // Mobile language dropdown elements (if exists)
  const mobileLangDropdownBtn = document.querySelector(
    '.mobile-language-dropdown .lang-dropdown-btn'
  );
  const mobileLanguageDropdown = document.getElementById('mobileLanguageDropdown');
  const mobileLangOptions = document.querySelectorAll('#mobileLanguageDropdown .lang-option');

  // Desktop dropdown functionality
  if (langDropdownBtn && languageDropdown) {
    langDropdownBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      languageDropdown.classList.toggle('show');
      // Close mobile dropdown if open
      if (mobileLanguageDropdown) {
        mobileLanguageDropdown.classList.remove('show');
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
      if (!langDropdownBtn.contains(e.target) && !languageDropdown.contains(e.target)) {
        languageDropdown.classList.remove('show');
      }
    });
  }

  // Mobile language dropdown functionality (if mobile dropdown exists)
  if (mobileLangDropdownBtn && mobileLanguageDropdown) {
    mobileLangDropdownBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      mobileLanguageDropdown.classList.toggle('show');
      // Close desktop dropdown if open
      if (languageDropdown) {
        languageDropdown.classList.remove('show');
      }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function (e) {
      if (!mobileLangDropdownBtn.contains(e.target) && !mobileLanguageDropdown.contains(e.target)) {
        mobileLanguageDropdown.classList.remove('show');
      }
    });
  }

  // Desktop language option click handlers
  desktopLangOptions.forEach((option) => {
    option.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      const selectedLang = this.getAttribute('data-lang');

      if (languageDropdown) {
        languageDropdown.classList.remove('show');
      }

      switchLanguage(selectedLang);
    });
  });

  // Mobile language option click handlers (if mobile options exist)
  if (mobileLangOptions.length > 0) {
    mobileLangOptions.forEach((option) => {
      option.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();

        const selectedLang = this.getAttribute('data-lang');

        if (mobileLanguageDropdown) {
          mobileLanguageDropdown.classList.remove('show');
        }

        switchLanguage(selectedLang);
      });
    });
  }

  // =================
  // LANGUAGE SWITCHING FUNCTIONS
  // =================
  function switchLanguage(langCode) {
    let csrfValue = getCsrfToken();
    const newPath = calculateNewPath(langCode);

    if (csrfValue) {
      submitLanguageForm(langCode, newPath, csrfValue);
    } else {
      window.location.href = newPath;
    }
  }

  function getCsrfToken() {
    // First try meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) {
      return csrfMeta.getAttribute('content');
    }

    // Try input field
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfInput) {
      return csrfInput.value;
    }

    // Try cookie
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
        return value;
      }
    }
    return null;
  }

  function calculateNewPath(langCode) {
    let currentPath = window.location.pathname;
    const supportedLangs = ['en', 'de', 'es', 'fr', 'it', 'zh-hans'];

    for (let lang of supportedLangs) {
      const regex = new RegExp(`^/${lang}(/|$)`);
      if (regex.test(currentPath)) {
        currentPath = currentPath.replace(regex, '/');
        break;
      }
    }

    if (!currentPath.startsWith('/')) {
      currentPath = '/' + currentPath;
    }

    if (langCode === 'en') {
      return currentPath;
    } else {
      if (currentPath === '/') {
        return `/${langCode}/`;
      } else {
        return `/${langCode}${currentPath}`;
      }
    }
  }

  function submitLanguageForm(langCode, nextUrl, csrfToken) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/i18n/setlang/';
    form.style.display = 'none';

    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    const langInput = document.createElement('input');
    langInput.type = 'hidden';
    langInput.name = 'language';
    langInput.value = langCode;
    form.appendChild(langInput);

    const nextInput = document.createElement('input');
    nextInput.type = 'hidden';
    nextInput.name = 'next';
    nextInput.value = nextUrl;
    form.appendChild(nextInput);

    document.body.appendChild(form);
    form.submit();
  }

  function setActiveLanguageButton() {
    const currentPath = window.location.pathname;
    let currentLang = 'en';

    // Determine current language from URL
    const supportedLangs = ['en', 'de', 'es', 'fr', 'it', 'zh-hans'];
    for (let lang of supportedLangs) {
      if (currentPath.startsWith(`/${lang}/`) || currentPath === `/${lang}`) {
        currentLang = lang;
        break;
      }
    }

    // Remove active class from all language options
    document.querySelectorAll('.lang-option').forEach((btn) => {
      btn.classList.remove('active');
    });

    // Add active class to current language
    document.querySelectorAll(`.lang-option[data-lang="${currentLang}"]`).forEach((btn) => {
      btn.classList.add('active');
    });

    // Update dropdown button text
    const langTexts = {
      en: 'EN',
      de: 'DE',
      es: 'ES',
      fr: 'FR',
      it: 'IT',
      'zh-hans': '汉语'
    };

    const currentLangText = langTexts[currentLang] || 'EN';
  }

  // =================
  // ACTIVE LINKS FUNCTIONALITY
  // =================
  function setActiveLinks() {
    const currentPath = window.location.pathname;
    const allNavLinks = document.querySelectorAll('.navbar a[href], .mobile-menu a[href]');

    allNavLinks.forEach((link) => {
      link.classList.remove('active');
    });

    const dropdownParents = document.querySelectorAll(
      '.dropdown > a, .mobile-dropdown > .mobile-dropdown-head'
    );
    dropdownParents.forEach((parent) => {
      parent.classList.remove('active');
    });

    // Check dropdown links
    const dropdownLinks = document.querySelectorAll(
      '.dropdown-content a[href], .mobile-dropdown-content a[href]'
    );
    let activeDropdownFound = false;

    dropdownLinks.forEach((dropdownLink) => {
      const linkPath = dropdownLink.getAttribute('href');

      if (
        linkPath === currentPath ||
        (linkPath && linkPath !== '/' && currentPath.startsWith(linkPath))
      ) {
        dropdownLink.classList.add('active');

        const parentDropdown = dropdownLink.closest('.dropdown');
        if (parentDropdown) {
          const parentLink = parentDropdown.querySelector('> a');
          if (parentLink) {
            parentLink.classList.add('active');
            activeDropdownFound = true;
          }
        }

        const parentMobileDropdown = dropdownLink.closest('.mobile-dropdown');
        if (parentMobileDropdown) {
          const parentMobileLink = parentMobileDropdown.querySelector('.mobile-dropdown-head');
          if (parentMobileLink) {
            parentMobileLink.classList.add('active');
            activeDropdownFound = true;
          }
        }
      }
    });

    // If no dropdown link is active, check regular navigation links
    if (!activeDropdownFound) {
      const regularNavLinks = document.querySelectorAll(
        '.navbar a[href]:not(.dropdown-content a), .mobile-menu a[href]:not(.mobile-dropdown-content a)'
      );

      regularNavLinks.forEach((link) => {
        const linkPath = link.getAttribute('href');

        if (linkPath === currentPath) {
          link.classList.add('active');
        } else if (
          linkPath &&
          linkPath !== '/' &&
          linkPath !== '' &&
          currentPath.startsWith(linkPath)
        ) {
          link.classList.add('active');
        }
      });
    }
  }

  // =================
  // INITIALIZATION
  // =================
  initializeMobileMenu();
  setActiveLanguageButton();
  setActiveLinks();

  // Event listeners for browser navigation
  window.addEventListener('popstate', setActiveLinks);
  window.updateActiveLinks = setActiveLinks;

  // Test function for debugging
  window.testLanguageSwitch = function (lang) {
    switchLanguage(lang);
  };
});
