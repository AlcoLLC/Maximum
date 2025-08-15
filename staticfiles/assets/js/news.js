document.addEventListener('DOMContentLoaded', function() {
    const loadMoreBtn = document.getElementById('load-more-btn');
    const newsContainer = document.getElementById('news-container');
    const shownCountSpan = document.getElementById('shown-count');
    const totalCountSpan = document.getElementById('total-count');
    
    let currentlyShown = 9;
    const itemsPerLoad = 3;
    const allNewsItems = Array.from(newsContainer.querySelectorAll('.news-item'));
    const totalItems = allNewsItems.length;
    
    // Update total count
    totalCountSpan.textContent = totalItems;
    
    // Hide load more button if all items are already shown
    if (currentlyShown >= totalItems) {
        loadMoreBtn.style.display = 'none';
    }
    
    loadMoreBtn.addEventListener('click', function() {
        const itemsToShow = Math.min(itemsPerLoad, totalItems - currentlyShown);
        
        if (itemsToShow <= 0) {
            loadMoreBtn.style.display = 'none';
            return;
        }
        
        // Show next batch of items with animation
        for (let i = currentlyShown; i < currentlyShown + itemsToShow; i++) {
            const item = allNewsItems[i];
            if (item) {
                // Make item visible but transparent
                item.style.display = 'block';
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
                
                // Animate in with a slight delay for each item
                setTimeout(() => {
                    item.style.transition = 'all 0.6s ease';
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, (i - currentlyShown) * 100);
            }
        }
        
        currentlyShown += itemsToShow;
        shownCountSpan.textContent = currentlyShown;
        
        // Hide load more button if all items are now shown
        if (currentlyShown >= totalItems) {
            setTimeout(() => {
                loadMoreBtn.style.opacity = '0.5';
                loadMoreBtn.disabled = true;
                loadMoreBtn.textContent = loadMoreBtn.textContent.replace('Load more', 'All items loaded');
            }, 300);
        }
    });
});