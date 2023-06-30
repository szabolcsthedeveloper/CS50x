// Get all the answer buttons
var answerButtons = document.querySelectorAll('.answer');

// Add click event listener to each button
answerButtons.forEach(function(button) {
  button.addEventListener('click', function() {
    var isCorrect = button.getAttribute('data-correct') === 'true';

    // Remove existing color classes from all buttons
    answerButtons.forEach(function(button) {
      button.classList.remove('correct', 'incorrect');
    });

    // Change button color based on the answer
    if (isCorrect) {
      button.classList.add('correct');
    } else {
      button.classList.add('incorrect');
    }

    // Show text beneath the question based on the answer
    var feedbackText = isCorrect ? 'Correct!' : 'Incorrect';
    var feedbackElement = document.createElement('p');
    feedbackElement.textContent = feedbackText;
    button.parentNode.appendChild(feedbackElement);
  });
});
``



document.addEventListener("DOMContentLoaded", function() {
    var confirmBtn = document.getElementById("confirm-btn");
    confirmBtn.addEventListener("click", function() {
      var answerInput = document.getElementById("answer-input");
      var answerFeedback = document.getElementById("answer-feedback");
      var userAnswer = answerInput.value.trim();

      if (userAnswer === "correct") {
        answerInput.classList.add("correct");
        answerInput.classList.remove("incorrect");
        answerFeedback.textContent = "Correct!";
        answerFeedback.classList.remove("incorrect");
        answerFeedback.classList.add("correct");
      } else {
        answerInput.classList.add("incorrect");
        answerInput.classList.remove("correct");
        answerFeedback.textContent = "Incorrect";
        answerFeedback.classList.remove("correct");
        answerFeedback.classList.add("incorrect");
      }
    });
  });
