// global/js/script.js

function userScroll() {
  const toTopBtn = document.querySelector('#to-top');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      toTopBtn.classList.add('show-btn');
    } else {
      toTopBtn.classList.remove('show-btn');
    }
  });
}

function scrollToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', userScroll);
document.querySelector('#to-top').addEventListener('click', scrollToTop);

function goToNextSection() {
  const nextSectionBtn = document.querySelector('#next-section');
  const sections = document.getElementsByTagName('section');
  
  nextSectionBtn.addEventListener('click', () => {
    for (let i = 0; i < sections.length; i++) {
      if (sections[i].getBoundingClientRect().top > 0) {
        sections[i].scrollIntoView({ behavior: 'smooth' });
        break;
      } 
    }
  });
}
document.addEventListener('DOMContentLoaded', goToNextSection);

function checkSection() {
  const nextSectionBtn = document.querySelector('#next-section');

  if (document.documentElement.scrollTop  === document.documentElement.scrollTopMax) {
    nextSectionBtn.classList.add('hide');
  }
  else {
    nextSectionBtn.classList.remove('hide');
  }
  window.addEventListener('scroll', checkSection);
}

document.addEventListener('DOMContentLoaded', checkSection);

function checkSectionTotal() {
  const nextSectionBtn = document.querySelector('#next-section');
  const sections = document.getElementsByTagName('section');

  if (sections.length > 1) {
    nextSectionBtn.classList.remove('hidden');
  } else {
    nextSectionBtn.classList.add('hidden');
  }
}
document.addEventListener('DOMContentLoaded', checkSectionTotal);
