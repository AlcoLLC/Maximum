document.addEventListener("DOMContentLoaded", function () {
  const columns = document.querySelectorAll(".faq-section .section-grid");

  const questions = document.querySelectorAll(
    ".faq-section .grid-item .question"
  );

  questions.forEach((question) => {
    question.addEventListener("click", function () {
      const gridItem = this.parentElement;
      const answer = gridItem.querySelector(".answer");
      const plusIcon = this.querySelector(".plus-icon");
      const minusIcon = this.querySelector(".minus-icon");

      if (answer.style.display === "block") {
        answer.style.display = "none";
        plusIcon.style.display = "block";
        minusIcon.style.display = "none";
        gridItem.style.height = "auto";
        gridItem.classList.remove("open");
      } else {
        answer.style.display = "block";
        plusIcon.style.display = "none";
        minusIcon.style.display = "block";
        const questionHeight = question.offsetHeight;
        const answerHeight = answer.offsetHeight;
        const totalPadding = 40;
        const newHeight = questionHeight + answerHeight + totalPadding;
        gridItem.style.height = newHeight + "px";
        gridItem.classList.add("open");
      }
    });
  });
});
