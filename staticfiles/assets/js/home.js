// Product Ranges Swiper
document.addEventListener('DOMContentLoaded', function () {
  // Header Swiper
  const headerSwiper = new Swiper('.mySwiper', {
    loop: false,
    effect: 'fade',
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    on: {
      init: function () {
        generateCustomPagination(this, '.swiper-navigation');
        updatePaginationActive(this, '.swiper-navigation');
      },
      slideChange: function () {
        updatePaginationActive(this, '.swiper-navigation');
      }
    }
  });

  // Product Ranges Industry Swiper
  const industrySwiper = new Swiper('.industrySwiper', {
    slidesPerView: 1.5,
    spaceBetween: 30,
    centeredSlides: true,
    loop: true,
    autoplay: {
      delay: 4000,
      disableOnInteraction: false
    },
    navigation: {
      nextEl: '.industry-navigation .swiper-button-next',
      prevEl: '.industry-navigation .swiper-button-prev'
    },
    breakpoints: {
      480: {
        slidesPerView: 1.8
      },
      768: {
        slidesPerView: 2.5
      },
      1024: {
        slidesPerView: 3.2
      },
      1200: {
        slidesPerView: 4.2
      }
    }
  });

  function generateCustomPagination(swiperInstance, containerSelector) {
    const container = document.querySelector(containerSelector);
    if (!container) return;

    container.innerHTML = '';

    swiperInstance.slides.forEach((_, index) => {
      const dot = document.createElement('div');
      dot.addEventListener('click', () => {
        swiperInstance.slideTo(index);
      });
      container.appendChild(dot);
    });
  }

  function updatePaginationActive(swiperInstance, containerSelector) {
    const paginationItems = document.querySelectorAll(`${containerSelector} div`);
    paginationItems.forEach((el, index) => {
      el.classList.toggle('active', index === swiperInstance.realIndex);
    });
  }

  // News Swiper
  const newsSwiper = new Swiper('.newsSwiper', {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,
    autoplay: {
      delay: 4000,
      disableOnInteraction: false
    },
    navigation: {
      nextEl: '.news-swiper-button-next',
      prevEl: '.news-swiper-button-prev'
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 10
      },
      768: {
        slidesPerView: 1.5,
        spaceBetween: 15
      },
      1024: {
        slidesPerView: 2,
        spaceBetween: 10
      }
    }
  });

  const productsSwiper = new Swiper('.productsSwiper', {
    slidesPerView: 1,
    grid: {
      rows: 2,
      fill: 'row'
    },
    loop: false,
    autoplay: {
      delay: 4000,
      disableOnInteraction: false
    },
    spaceBetween: 10,
    navigation: {
      nextEl: '.product-swiper-button-next',
      prevEl: '.product-swiper-button-prev'
    },
    breakpoints: {
      900: {
        slidesPerView: 2,
        grid: {
          rows: 2
        },
        spaceBetween: 10
      },
      700: {
        slidesPerView: 1,
        grid: {
          rows: 2
        },
        spaceBetween: 10
      },
      500: {
        slidesPerView: 1,
        grid: {
          rows: 1
        },
        spaceBetween: 5
      }
    }
  });

  const partnersSwiper = new Swiper('.partnersSwiper', {
    slidesPerView: 4,
    spaceBetween: 30,
    loop: true,
    navigation: {
      nextEl: '.partners-swiper-button-next',
      prevEl: '.partners-swiper-button-prev'
    },
    autoplay: {
      delay: 2500,
      disableOnInteraction: false
    },
    breakpoints: {
      320: {
        slidesPerView: 2,
        spaceBetween: 10
      },
      480: {
        slidesPerView: 2,
        spaceBetween: 15
      },
      768: {
        slidesPerView: 3,
        spaceBetween: 20
      },
      1024: {
        slidesPerView: 4,
        spaceBetween: 20
      }
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const playButton = document.getElementById('playButton');
  const videoContainer = document.getElementById('videoContainer');
  const youtubeVideo = document.getElementById('youtubeVideo');

  if (playButton) {
    playButton.addEventListener('click', function () {
      playButton.style.display = 'none';
      videoContainer.style.display = 'block';
      const videoSrc = youtubeVideo.src;
      youtubeVideo.src = videoSrc + '&autoplay=1';
    });
  }
});
