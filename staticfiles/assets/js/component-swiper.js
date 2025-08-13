document.addEventListener('DOMContentLoaded', function () {

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
