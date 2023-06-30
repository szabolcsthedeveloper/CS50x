const cookieBtn = document.getElementById('cookie-btn');
const scoreElement = document.getElementById('score');

let score = 0;

cookieBtn.addEventListener('click', () => {
  score++;
  scoreElement.textContent = `Score: ${score}`;
  cookieBtn.classList.add('clicked');

  setTimeout(() => {
    cookieBtn.classList.remove('clicked');
  }, 100);
});
