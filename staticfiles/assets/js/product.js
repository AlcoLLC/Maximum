document.addEventListener("DOMContentLoaded", function () {
  // Filter header toggle functionality
  const filterHeaders = document.querySelectorAll(".filter-header");

  filterHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      this.classList.toggle("active");
      const content = this.nextElementSibling;
      content.classList.toggle("open");
      const icon = this.querySelector(".filter-icon i");
      if (content.classList.contains("open")) {
        icon.classList.remove("fa-chevron-down");
        icon.classList.add("fa-chevron-up");
      } else {
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
      }
    });
  });

  // Desktop filter - checkbox functionality without auto-submit
  const desktopCheckboxes = document.querySelectorAll(
    '.filter-container .checkbox-group input[type="checkbox"]'
  );
  const searchInput = document.querySelector(
    '.filter-container input[name="search"]'
  );

  desktopCheckboxes.forEach((checkbox) => {
    const label = checkbox.nextElementSibling;

    checkbox.addEventListener("change", function () {
      if (this.checked) {
        label.classList.add("selected-item");
      } else {
        label.classList.remove("selected-item");
      }
      // Do NOT auto-submit form anymore
    });
  });

  // Search input - only submit on Enter key press
  if (searchInput) {
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault(); // Prevent default form submission
        submitFilterForm();
      }
    });
  }

  // Search button click handler
  const searchButton = document.querySelector(
    ".filter-container .search-button"
  );
  if (searchButton) {
    searchButton.addEventListener("click", function (e) {
      e.preventDefault();
      submitFilterForm();
    });
  }

  // Desktop Filter Results Button
  const filterResultsBtn = document.getElementById("filterResultsBtn");
  if (filterResultsBtn) {
    filterResultsBtn.addEventListener("click", function () {
      submitFilterForm();
    });
  }

  // Function to submit the filter form
  function submitFilterForm() {
    const form = document.getElementById("filterForm");
    const pageInput = document.querySelector('input[name="page"]');
    if (pageInput) {
      pageInput.value = 1;
    }
    if (form) {
      form.submit();
    }
  }

  // Pagination functionality
  const prevButton = document.getElementById("prevPage");
  const nextButton = document.getElementById("nextPage");
  const pageNumbers = document.querySelectorAll(".page-number");

  if (prevButton) {
    prevButton.addEventListener("click", function () {
      if (!this.disabled) {
        const currentPageSpan = document.querySelector(".page-number.active");
        if (currentPageSpan) {
          const currentPage = parseInt(
            currentPageSpan.getAttribute("data-page")
          );
          if (currentPage > 1) {
            navigateToPage(currentPage - 1);
          }
        }
      }
    });
  }

  if (nextButton) {
    nextButton.addEventListener("click", function () {
      if (!this.disabled) {
        const currentPageSpan = document.querySelector(".page-number.active");
        if (currentPageSpan) {
          const currentPage = parseInt(
            currentPageSpan.getAttribute("data-page")
          );
          navigateToPage(currentPage + 1);
        }
      }
    });
  }

  pageNumbers.forEach((number) => {
    number.addEventListener("click", function (e) {
      e.preventDefault();
      const pageNum = parseInt(this.getAttribute("data-page"));
      if (pageNum) {
        navigateToPage(pageNum);
      }
    });
  });

  function navigateToPage(pageNum) {
    const form = document.getElementById("filterForm");
    const pageInput = document.querySelector('input[name="page"]');
    if (pageInput && form) {
      pageInput.value = pageNum;
      form.submit();
    }
  }

  // Animation on scroll for sections
  checkScroll();
  window.addEventListener("scroll", checkScroll);

  function checkScroll() {
    const sections = document.querySelectorAll(".section");
    sections.forEach((section) => {
      const sectionTop = section.getBoundingClientRect().top;
      const windowHeight = window.innerHeight;
      if (sectionTop < windowHeight * 0.85) {
        section.classList.add("active");
      } else {
        section.classList.remove("active");
      }
    });
  }
});

// Modal overlay functionality
document.addEventListener("DOMContentLoaded", function () {
  const mobileFilterBtn = document.getElementById("filterMobileBtn");
  const productFilterModal = document.getElementById("productFilterModal");
  const productModalClose = document.getElementById("productModalClose");
  const productSearchResultsBtn = document.getElementById(
    "productSearchResultsBtn"
  );

  // Open modal
  if (mobileFilterBtn) {
    mobileFilterBtn.addEventListener("click", function () {
      productFilterModal.classList.add("show-modal");
      document.body.style.overflow = "hidden";
    });
  }

  // Close modal function
  function closeProductModal() {
    productFilterModal.classList.remove("show-modal");
    document.body.style.overflow = "auto";
  }

  // Close modal button
  if (productModalClose) {
    productModalClose.addEventListener("click", closeProductModal);
  }

  // Close modal when clicking overlay
  if (productFilterModal) {
    productFilterModal.addEventListener("click", function (e) {
      if (e.target === productFilterModal) {
        closeProductModal();
      }
    });
  }

  // Close modal on escape key
  document.addEventListener("keydown", function (e) {
    if (
      e.key === "Escape" &&
      productFilterModal.classList.contains("show-modal")
    ) {
      closeProductModal();
    }
  });

  // Modal filter header toggle functionality - accordion style (only one open at a time)
  const modalFilterHeaders = document.querySelectorAll(".modal-filter-header");
  modalFilterHeaders.forEach((header) => {
    header.addEventListener("click", function () {
      const currentContent = this.nextElementSibling;
      const currentIcon = this.querySelector(".modal-filter-icon i");
      const isCurrentlyOpen =
        currentContent.classList.contains("modal-content-open");

      // Close all other sections first
      modalFilterHeaders.forEach((otherHeader) => {
        if (otherHeader !== this) {
          const otherContent = otherHeader.nextElementSibling;
          const otherIcon = otherHeader.querySelector(".modal-filter-icon i");

          // Close other sections
          otherHeader.classList.remove("modal-header-active");
          otherContent.classList.remove("modal-content-open");
          otherIcon.classList.remove("fa-chevron-up");
          otherIcon.classList.add("fa-chevron-down");
        }
      });

      // Toggle current section
      if (!isCurrentlyOpen) {
        // Open current section
        this.classList.add("modal-header-active");
        currentContent.classList.add("modal-content-open");
        currentIcon.classList.remove("fa-chevron-down");
        currentIcon.classList.add("fa-chevron-up");
      } else {
        // Close current section if it was already open
        this.classList.remove("modal-header-active");
        currentContent.classList.remove("modal-content-open");
        currentIcon.classList.remove("fa-chevron-up");
        currentIcon.classList.add("fa-chevron-down");
      }
    });
  });

  // Modal checkbox functionality
  const modalCheckboxes = document.querySelectorAll(
    '.modal-checkbox-group input[type="checkbox"]'
  );
  modalCheckboxes.forEach((checkbox) => {
    const label = checkbox.nextElementSibling;

    checkbox.addEventListener("change", function () {
      if (this.checked) {
        label.classList.add("modal-selected-item");
      } else {
        label.classList.remove("modal-selected-item");
      }
    });
  });

  // Search results button - collect form data and submit
  if (productSearchResultsBtn) {
    productSearchResultsBtn.addEventListener("click", function () {
      // Get the main form
      const mainForm = document.getElementById("filterForm");
      if (mainForm) {
        // Sync modal form data with main form
        const modalForm = document.getElementById("modalFilterForm");
        if (modalForm) {
          // Clear existing selections in main form
          const mainCheckboxes = mainForm.querySelectorAll(
            'input[type="checkbox"]'
          );
          mainCheckboxes.forEach((cb) => (cb.checked = false));

          // Copy modal selections to main form
          const modalCheckboxes = modalForm.querySelectorAll(
            'input[type="checkbox"]:checked'
          );
          modalCheckboxes.forEach((modalCb) => {
            const mainCb = mainForm.querySelector(
              `input[name="${modalCb.name}"][value="${modalCb.value}"]`
            );
            if (mainCb) {
              mainCb.checked = true;
              // Update visual state
              const label = mainCb.nextElementSibling;
              if (label) {
                label.classList.add("selected-item");
              }
            }
          });

          // Copy search input
          const modalSearchInput = modalForm.querySelector(
            'input[name="search"]'
          );
          const mainSearchInput = mainForm.querySelector(
            'input[name="search"]'
          );
          if (modalSearchInput && mainSearchInput) {
            mainSearchInput.value = modalSearchInput.value;
          }

          // Reset to page 1
          const pageInput = mainForm.querySelector('input[name="page"]');
          if (pageInput) {
            pageInput.value = 1;
          }

          // Submit main form
          mainForm.submit();
        }
      }

      // Close modal
      closeProductModal();
    });
  }

  // Modal search button
  const modalSearchButton = document.querySelector(".modal-search-button");
  const modalSearchInput = document.querySelector(".modal-search-input");

  if (modalSearchButton) {
    modalSearchButton.addEventListener("click", function () {
      // Trigger search results
      if (productSearchResultsBtn) {
        productSearchResultsBtn.click();
      }
    });
  }

  if (modalSearchInput) {
    modalSearchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        // Trigger search results
        if (productSearchResultsBtn) {
          productSearchResultsBtn.click();
        }
      }
    });
  }
});
