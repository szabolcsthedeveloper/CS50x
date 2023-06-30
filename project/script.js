let score = 0;  // Current score/cookies
let clickPower = 1;  // Click power to increase score
let autoPower = 0;  // Automatic score generation power

function cookieClick() {
  score += clickPower;
  updateScore();
  animateCookieClick();
  createFallingCookies(clickPower);
}

function autoGenerateScore() {
  score += autoPower;
  updateScore();
  createFallingCookies(autoPower);
}

function purchaseClickUpgrade() {
  const clickUpgradeCost = 10;

  if (score >= clickUpgradeCost) {
    score -= clickUpgradeCost;
    clickPower += 1;
    updateScore();
    updateClickUpgradeCost(clickUpgradeCost * 2);
  }
}

function purchaseIdleUpgrade() {
  const idleUpgradeCost = 20;

  if (score >= idleUpgradeCost) {
    score -= idleUpgradeCost;
    autoPower += 1;
    updateScore();
    updateIdleUpgradeCost(idleUpgradeCost * 2);
  }
}

function updateScore() {
  document.getElementById('score').innerText = score;
}

function updateClickUpgradeCost(cost) {
  document.getElementById('click-upgrade-cost').innerText = 'Cost: ' + cost;
}

function updateIdleUpgradeCost(cost) {
  document.getElementById('idle-upgrade-cost').innerText = 'Cost: ' + cost;
}

function animateCookieClick() {
  const cookieElement = document.getElementById('cookie');
  cookieElement.classList.add('cookie-click-animation');
  setTimeout(() => {
    cookieElement.classList.remove('cookie-click-animation');
  }, 500);
}

function createFallingCookies(amount) {
  const container = document.getElementById('background');
  const maxWidth = container.offsetWidth;

  for (let i = 0; i < amount; i++) {
    const cookie = document.createElement('img');
    cookie.src = 'cookie.png';
    cookie.classList.add('falling-cookie');
    cookie.style.left = getRandomPosition(maxWidth) + 'px';
    container.appendChild(cookie);

    setTimeout(() => {
      cookie.remove();
    }, 3000);
  }
}

function getRandomPosition(maxWidth) {
  return Math.floor(Math.random() * maxWidth);
}

setInterval(autoGenerateScore, 1000);  // Call autoGenerateScore every second
updateScore();  // Display initial score
updateClickUpgradeCost(10);  // Display initial click upgrade cost
updateIdleUpgradeCost(20);



function animateCookieClick() {
    const cookieElement = document.getElementById('cookie');
    cookieElement.classList.add('cookie-click-animation');
    setTimeout(() => {
      cookieElement.classList.remove('cookie-click-animation');
    }, 500);
    cookieElement.classList.add('cookie-enlarge-animation');
    setTimeout(() => {
      cookieElement.classList.remove('cookie-enlarge-animation');
    }, 300);
  }

