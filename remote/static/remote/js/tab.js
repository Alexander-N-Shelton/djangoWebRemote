document.addEventListener("DOMContentLoaded", function () {
  const navTab = document.getElementById("navTab");
  const favTab = document.getElementById("favTab");
  const navRemoteContainer = document.getElementById("navRemoteContainer");
  const favRemoteContainer = document.getElementById("favRemoteContainer");

  navTab.addEventListener("click", function (e) {
    e.preventDefault();
    navTab.classList.add("active");
    favTab.classList.remove("active");

    navRemoteContainer.classList.add('show', 'active');
    favRemoteContainer.classList.remove('show', 'active');
  });

  favTab.addEventListener("click", function (e) {
    e.preventDefault();
    favTab.classList.add("active");
    navTab.classList.remove("active");

    favRemoteContainer.classList.add('show', 'active');
    navRemoteContainer.classList.remove('show', 'active');
  });
});
