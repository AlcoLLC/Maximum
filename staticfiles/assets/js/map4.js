$(function () {
  $("body").scrollspy({ target: ".nav-left", offset: 10 });
  $(".nav a").on("click", function (event) {
    if (this.hash !== "") {
      event.preventDefault();
      var hash = this.hash;
      $("html, body").animate(
        {
          scrollTop: $(hash).offset().top,
        },
        800,
        function () {
          window.location.hash = hash;
        }
      );
    }
  });
  /* begin Back to Top button  */
  (function () {
    "use strict";

    function trackScroll() {
      var scrolled = window.pageYOffset;
      var coords = document.documentElement.clientHeight;
      if (scrolled > coords) {
        goTopBtn.classList.add("back_to_top-show");
      }
      if (scrolled < coords) {
        goTopBtn.classList.remove("back_to_top-show");
      }
    }

    function backToTop() {
      if (window.pageYOffset > 0) {
        window.scrollBy(0, -80);
        setTimeout(backToTop, 0);
      }
    }
    var goTopBtn = document.querySelector(".back_to_top");
    window.addEventListener("scroll", trackScroll);
    goTopBtn.addEventListener("click", backToTop);
  })();
  /* end Back to Top button  */
  /* ###############################################  */
});
