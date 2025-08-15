document.addEventListener("DOMContentLoaded", function () {
  const tabs = document.querySelectorAll(".tab");

  tabs.forEach((tab) => {
    tab.addEventListener("click", function (e) {
      e.preventDefault();
      
      const tabId = this.getAttribute("data-tab");
      
      // Update URL without page reload
      const newUrl = `/brands/${tabId}/`;
      window.history.pushState({ tab: tabId }, '', newUrl);
      
      // Update active tab
      activateTab(tabId);
    });
  });

  // Learn more buttons functionality
  const learnMoreButtons = document.querySelectorAll(".brand-components .button-style");
  
  learnMoreButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      
      const tabId = this.getAttribute("data-id");
      
      // Update URL without page reload
      const newUrl = `/brands/${tabId}/`;
      window.history.pushState({ tab: tabId }, '', newUrl);
      
      // Update active tab
      activateTab(tabId);
    });
  });

  // Handle browser back/forward buttons
  window.addEventListener("popstate", function (event) {
    const currentPath = window.location.pathname;
    const tabMatch = currentPath.match(/\/brands\/([^\/]+)\//);
    
    if (tabMatch) {
      const tabId = tabMatch[1];
      activateTab(tabId);
    } else {
      // Show overview/default content
      activateTab(null);
    }
  });

  function activateTab(tabId) {
    // Remove active class from all tabs and tab contents
    tabs.forEach((t) => t.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach((content) => {
      content.classList.remove("active");
    });
    
    if (tabId) {
      // Activate the corresponding tab
      const targetTab = document.querySelector(`[data-tab="${tabId}"]`);
      if (targetTab) {
        targetTab.classList.add("active");
      }
      
      // Activate the corresponding tab content
      const targetContent = document.getElementById(tabId);
      if (targetContent) {
        targetContent.classList.add("active");
      }
    } else {
      // Show the first tab-content (overview) when no specific tab is selected
      const firstTabContent = document.querySelector(".tab-content");
      if (firstTabContent) {
        firstTabContent.classList.add("active");
      }
    }
  }

  // Video modal functionality
  const modal = document.getElementById("videoModal");
  const videoFrame = document.getElementById("videoFrame");
  const closeBtn = document.querySelector(".close-modal");
  const videoThumbnails = document.querySelectorAll(".video-thumbnail");

  videoThumbnails.forEach((thumbnail) => {
    thumbnail.addEventListener("click", function () {
      const videoUrl = this.getAttribute("data-video-url");
      const embedUrl = convertToEmbedUrl(videoUrl);

      videoFrame.src = embedUrl + "?autoplay=1";
      modal.style.display = "flex";
      document.body.style.overflow = "hidden";
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", closeModal);
  }
  
  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      closeModal();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeModal();
    }
  });

  function closeModal() {
    modal.style.display = "none";
    videoFrame.src = "";
    document.body.style.overflow = "auto";
  }

  function convertToEmbedUrl(url) {
    const regex = /(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/))([^?&]+)/;
    const match = url.match(regex);
    const videoId = match ? match[1] : null;
    return videoId ? `https://www.youtube.com/embed/${videoId}` : "";
  }

  // PDF open functionality (only open in new tab)
  const pdfButtons = document.querySelectorAll(".tab-brand-guideline .button-style, .tab-promo-materials .button-style");
  
  pdfButtons.forEach((button) => {
    button.addEventListener("click", function(e) {
      e.preventDefault();
      
      let pdfUrl = null;
      
      // Check if it's brand guideline button
      if (this.closest('.tab-brand-guideline')) {
        const guidelineData = this.closest('.tab-brand-guideline').querySelector('img');
        if (guidelineData && guidelineData.dataset.pdfUrl) {
          pdfUrl = guidelineData.dataset.pdfUrl;
        }
      }
      
      // Check if it's promo material button
      if (this.closest('.tab-promo-materials div')) {
        const promoItem = this.closest('div');
        if (promoItem.dataset.pdfUrl) {
          pdfUrl = promoItem.dataset.pdfUrl;
        }
      }
      
      if (pdfUrl) {
        // Only open PDF in new tab
        window.open(pdfUrl, '_blank');
      }
    });
  });

  // Image library open and download functionality
  const imageItems = document.querySelectorAll(".tab-image-library .item");
  
  imageItems.forEach((item) => {
    item.addEventListener("click", function(e) {
      e.preventDefault();
      
      const img = this.querySelector('img');
      if (img && img.src) {
        // Open image in new tab first
        window.open(img.src, '_blank');
        
        // Then trigger download after a short delay
        setTimeout(() => {
          const downloadLink = document.createElement('a');
          downloadLink.href = img.src;
          downloadLink.download = '';
          downloadLink.style.display = 'none';
          document.body.appendChild(downloadLink);
          downloadLink.click();
          document.body.removeChild(downloadLink);
        }, 500);
      }
    });
  });
});