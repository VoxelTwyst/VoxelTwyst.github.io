window.addEventListener('scroll', () => {
    document.body.style.setProperty('--scroll', window.pageYOffset / 800);
  }, false);