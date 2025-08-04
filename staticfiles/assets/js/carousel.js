class MinimalInfiniteSlider {
  constructor(options) {
    this.container = document.getElementById(options.containerId);
    this.content = document.getElementById(options.contentId);
    this.nextBtn = document.getElementById(options.nextId);
    this.prevBtn = document.getElementById(options.prevId);

    this.speed = options.speed || 1;
    this.gap = options.gap || 30;
    this.itemWidth = options.itemWidth || 100;
    this.pauseOnHover = options.pauseOnHover !== false;

    // Vəziyyət dəyişənləri
    this.isAnimating = true;
    this.isPaused = false;
    this.animationId = null;
    this.currentTranslate = 0;
    this.isDragging = false;
    this.startX = 0;
    this.currentX = 0;
    this.dragOffset = 0;

    this.init();
  }

  init() {
    this.setupInfiniteLoop();
    this.setupEventListeners();
    this.start();
  }

  setupInfiniteLoop() {
    const items = Array.from(this.content.children);
    if (items.length === 0) return;

    const clonedItems = items.map((item) => item.cloneNode(true));
    clonedItems.forEach((item) => this.content.appendChild(item));

    this.singleWidth = items.length * (this.itemWidth + this.gap);
    this.currentTranslate = 0;

    this.content.style.transform = `translateX(${this.currentTranslate}px)`;
    this.content.style.transition = 'none';
  }

  setupEventListeners() {
    if (this.pauseOnHover) {
      this.container.addEventListener('mouseenter', () => this.pause());
      this.container.addEventListener('mouseleave', () => this.resume());
    }

    this.container.addEventListener('mousedown', (e) => this.startDrag(e));
    this.container.addEventListener('touchstart', (e) => this.startDrag(e), { passive: false });

    document.addEventListener('mousemove', (e) => this.drag(e));
    document.addEventListener('touchmove', (e) => this.drag(e), { passive: false });

    document.addEventListener('mouseup', () => this.endDrag());
    document.addEventListener('touchend', () => this.endDrag());

    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', () => this.next());
    }

    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', () => this.prev());
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.pause();
      } else {
        this.resume();
      }
    });
  }

  startDrag(e) {
    this.isDragging = true;
    this.startX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
    this.currentX = this.startX;
    this.dragOffset = 0;
    this.pause();

    this.container.style.cursor = 'grabbing';
    e.preventDefault();
  }

  drag(e) {
    if (!this.isDragging) return;

    this.currentX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
    this.dragOffset = this.currentX - this.startX;

    const newTranslate = this.currentTranslate + this.dragOffset;
    this.content.style.transform = `translateX(${newTranslate}px)`;

    e.preventDefault();
  }

  endDrag() {
    if (!this.isDragging) return;

    this.isDragging = false;
    this.currentTranslate += this.dragOffset;
    this.dragOffset = 0;

    this.container.style.cursor = 'grab';

    setTimeout(() => this.resume(), 300);
  }

  next() {
    this.pause();
    const moveDistance = this.itemWidth + this.gap;
    this.smoothMove(-moveDistance);

    setTimeout(() => this.resume(), 600);
  }

  prev() {
    this.pause();
    const moveDistance = this.itemWidth + this.gap;
    this.smoothMove(moveDistance);

    setTimeout(() => this.resume(), 600);
  }

  smoothMove(distance) {
    const start = this.currentTranslate;
    const target = start + distance;
    const duration = 500;
    const startTime = performance.now();

    const animate = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = start + distance * easeOut;

      this.currentTranslate = current;
      this.content.style.transform = `translateX(${current}px)`;

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        this.checkReset();
      }
    };

    requestAnimationFrame(animate);
  }

  animate() {
    if (!this.isAnimating || this.isPaused || this.isDragging) {
      this.animationId = requestAnimationFrame(() => this.animate());
      return;
    }

    this.currentTranslate -= this.speed;
    this.content.style.transform = `translateX(${this.currentTranslate}px)`;

    this.checkReset();
    this.animationId = requestAnimationFrame(() => this.animate());
  }

  checkReset() {
    if (this.currentTranslate <= -this.singleWidth) {
      this.currentTranslate += this.singleWidth;
    }

    if (this.currentTranslate > 0) {
      this.currentTranslate -= this.singleWidth;
    }
  }

  start() {
    this.isAnimating = true;
    this.isPaused = false;
    this.container.style.cursor = 'grab';
    this.animate();
  }

  pause() {
    this.isPaused = true;
  }

  resume() {
    this.isPaused = false;
  }

  stop() {
    this.isAnimating = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
  }

  updateSpeed(newSpeed) {
    this.speed = Math.max(0.5, Math.min(5, newSpeed));
  }

  destroy() {
    this.stop();
    this.isDragging = false;
    this.content.style.transform = '';
    this.content.style.transition = '';
  }
}

let sliderInstances = {};

function createSlider(id, config) {
  if (sliderInstances[id]) {
    sliderInstances[id].destroy();
  }

  sliderInstances[id] = new MinimalInfiniteSlider(config);
  return sliderInstances[id];
}

// Responsiv konfiqurasiya
function getResponsiveConfig() {
  const width = window.innerWidth;

  if (width <= 500) {
    return {
      speed: 1,
      gap: 28,
      itemWidth: 85
    };
  } else if (width <= 620) {
    return {
      speed: 1.2,
      gap: 30,
      itemWidth: 100
    };
  } else if (width <= 800) {
    return {
      speed: 1.2,
      gap: 40,
      itemWidth: 100
    };
  } else if (width <= 1200) {
    return {
      speed: 1.4,
      gap: 80,
      itemWidth: 130
    };
  } else {
    return {
      speed: 1.2,
      gap: 115,
      itemWidth: 155
    };
  }
}

// Əsas başlatma funksiyası
function initializeSlider() {
  if (!document.getElementById('carousel')) return;

  const config = getResponsiveConfig();

  createSlider('logoSlider', {
    containerId: 'carousel',
    contentId: 'content',
    nextId: 'next',
    prevId: 'prev',
    ...config,
    pauseOnHover: true
  });

  if (!document.getElementById('carousel2')) return;
  const config2 = getResponsiveConfig();
  createSlider('carLogoSlider', {
    containerId: 'carousel2',
    contentId: 'content2',
    nextId: 'next2',
    prevId: 'prev2',
    ...config2,
    pauseOnHover: true
  });
}

// Ekran ölçüsü dəyişəndə yenidən konfiqurasiya et
let resizeTimeout;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    const slider = sliderInstances.logoSlider;
    if (slider) {
      const config = getResponsiveConfig();
      slider.updateSpeed(config.speed);
      // Digər parametrləri də yeniləmək lazım olsa, slider-i yenidən başlat
    }
  }, 250);
});

// DOM hazır olduqda başlat
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeSlider);
} else {
  initializeSlider();
}

window.pauseSlider = () => {
  Object.values(sliderInstances).forEach((slider) => slider.pause());
};

window.resumeSlider = () => {
  Object.values(sliderInstances).forEach((slider) => slider.resume());
};

window.updateSliderSpeed = (speed) => {
  Object.values(sliderInstances).forEach((slider) => slider.updateSpeed(speed));
};
