document.addEventListener("DOMContentLoaded", () => {

  function toggleModal(hideId, showId) {
    if (hideId) document.getElementById(hideId)?.classList.remove("show");
    if (showId) document.getElementById(showId)?.classList.add("show");
    document.body.style.overflow = document.querySelector(".modal.show") ? "hidden" : "";
  }

  const loginBtn = document.getElementById("loginBtn");
  const registerBtn = document.getElementById("registerBtn");

  // Header buttons
  loginBtn?.addEventListener("click", () => {
    const modal = document.getElementById("loginModal");
    if (modal) toggleModal(null, "loginModal");
    else window.location.href = loginBtn.dataset.url;
  });

  registerBtn?.addEventListener("click", () => {
    const modal = document.getElementById("registerModal");
    if (modal) toggleModal(null, "registerModal");
    else window.location.href = registerBtn.dataset.url;
  });

  // Login modal's "switch to register" link
  document.querySelectorAll(".login-modal .register-link span, .login-modal .register-link a").forEach(link => {
    link.addEventListener("click", (ev) => {
      ev.preventDefault(); // prevent default anchor behavior
      // Close login modal
      toggleModal("loginModal", null);

      // Open register modal if exists
      const regModal = document.getElementById("registerModal");
      if (regModal) {
        toggleModal(null, "registerModal");
      } else {
        // fallback to URL redirect
        const url = link.dataset.url || link.getAttribute("href") || "/register";
        window.location.href = url;
      }
    });
  });

  // Optional: ESC key closes modals
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const openModal = document.querySelector(".modal.show");
      if (openModal) {
        openModal.classList.remove("show");
        document.body.classList.remove("modal-open");
      }
    }
  });

});
