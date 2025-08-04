window.addEventListener('scroll', function () {
  const fixedWhatsapp = document.querySelector('.fixed-whatsapp');
  const scrollPosition = window.scrollY;

  if (scrollPosition > 100) {
    fixedWhatsapp.style.opacity = '1';
    fixedWhatsapp.style.visibility = 'visible';

    if (headerWhatsapp) {
      headerWhatsapp.style.opacity = '0';
      headerWhatsapp.style.visibility = 'hidden';
    }
  } else {
    fixedWhatsapp.style.opacity = '0';
    fixedWhatsapp.style.visibility = 'hidden';

    if (headerWhatsapp) {
      headerWhatsapp.style.opacity = '1';
      headerWhatsapp.style.visibility = 'visible';
    }
  }
});

document.getElementById('scrollToTop').addEventListener('click', function () {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});

document.addEventListener('DOMContentLoaded', function () {
  checkScroll();
  window.addEventListener('scroll', checkScroll);

  function checkScroll() {
    const sections = document.querySelectorAll('.section');
    sections.forEach((section) => {
      const sectionTop = section.getBoundingClientRect().top;
      const windowHeight = window.innerHeight;
      if (sectionTop < windowHeight * 0.85) {
        section.classList.add('active');
      } else {
        section.classList.remove('active');
      }
    });
  }

  const swiperGallery = new Swiper('.gallery-section .labSwiper', {
    slidesPerView: 2.5,
    centeredSlides: true,
    spaceBetween: 20,
    loop: true,
    speed: 800,
    navigation: {
      nextEl: '.gallery-section .swiper-button-next',
      prevEl: '.gallery-section .swiper-button-prev'
    },
    breakpoints: {
      320: {
        slidesPerView: 1.3,
        spaceBetween: 15
      },
      640: {
        slidesPerView: 1.8,
        spaceBetween: 15
      },
      1024: {
        slidesPerView: 2.2,
        spaceBetween: 20
      }
    },
    on: {
      init: function () {
        updateSlideScaling();
      },
      slideChange: function () {
        updateSlideScaling();
      }
    }
  });

  function updateSlideScaling() {
    const slides = document.querySelectorAll('.gallery-section .swiper-slide');

    slides.forEach((slide) => {
      slide.classList.remove('active-slide');
    });

    setTimeout(() => {
      const activeSlide = document.querySelector('.gallery-section .swiper-slide-active');
      if (activeSlide) {
        activeSlide.classList.add('active-slide');
      }
    }, 50);
  }
});
