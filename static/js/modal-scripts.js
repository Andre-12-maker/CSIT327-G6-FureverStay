document.addEventListener("DOMContentLoaded", () => {
  // Helper: toggle modals by adding/removing 'show' class
  function toggleModal(hideId, showId) {
    if (hideId) {
      const hideModal = document.getElementById(hideId);
      if (hideModal) hideModal.classList.remove("show");
    }
    if (showId) {
      const showModal = document.getElementById(showId);
      if (showModal) showModal.classList.add("show");
    }
  }

  // Header buttons (global behavior)
  const loginBtn = document.getElementById("loginBtn");
  const registerBtn = document.getElementById("registerBtn");

  if (loginBtn) {
    loginBtn.addEventListener("click", (e) => {
      const modal = document.getElementById("loginModal");
      if (modal) {
        // If login modal exists on this page, open it
        toggleModal(null, "loginModal");
      } else {
        // Otherwise redirect to login page (data-url on button)
        const url = loginBtn.dataset.url;
        if (url) window.location.href = url;
      }
    });
  }

  if (registerBtn) {
    registerBtn.addEventListener("click", (e) => {
      const modal = document.getElementById("registerModal");
      if (modal) {
        // If register modal exists on this page, open it
        toggleModal(null, "registerModal");
      } else {
        // Otherwise redirect to register page (data-url on button)
        const url = registerBtn.dataset.url;
        if (url) window.location.href = url;
      }
    });
  }

  // If this page has a login modal, wire its "switch to register" link to go to register page
  const loginSwitch = document.querySelector(".register-link a");
  if (loginSwitch) {
    loginSwitch.addEventListener("click", (ev) => {
      ev.preventDefault();
      const registerUrl = registerBtn ? registerBtn.dataset.url : null;
      if (registerUrl) window.location.href = registerUrl;
    });
  }

  // ----- Register page specific behavior -----
  // Only define the register-page functions if the register modal exists
  if (document.getElementById("registerModal")) {
    // Pet sitter/owner modal toggles
    window.openPetSitter = () => toggleModal("registerModal", "petSitterModal");
    window.openPetOwner = () => toggleModal("registerModal", "petOwnerModal");

    window.backToSelection = () => {
      toggleModal("petSitterModal", "registerModal");
      toggleModal("petOwnerModal", "registerModal");
    };

    // Success modals
    window.showSuccessPetSitter = () =>
      toggleModal("petSitterModal", "successPetSitterModal");
    window.showSuccessPetOwner = () =>
      toggleModal("petOwnerModal", "successPetOwnerModal");

    window.closeSuccessPetSitter = () => {
      toggleModal("successPetSitterModal", null);
      const loginUrl = loginBtn ? loginBtn.dataset.url : "/login";
      window.location.href = loginUrl;
    };

    window.closeSuccessPetOwner = () => {
      toggleModal("successPetOwnerModal", null);
      const loginUrl = loginBtn ? loginBtn.dataset.url : "/login";
      window.location.href = loginUrl;
    };

    // Step navigation
    window.goToSitterStep2 = () => {
      const step1 = document.querySelector("#sitter-step1");
      const step2 = document.querySelector("#sitter-step2");
      if (!step1 || !step2) return;
      const inputs = step1.querySelectorAll("input[required]");
      for (let input of inputs) {
        if (!input.value.trim()) {
          alert("Please fill in all fields before continuing.");
          return;
        }
      }
      step1.style.display = "none";
      step2.style.display = "block";
    };

    window.goToOwnerStep2 = () => {
      const step1 = document.querySelector("#owner-step1");
      const step2 = document.querySelector("#owner-step2");
      if (!step1 || !step2) return;
      const inputs = step1.querySelectorAll("input[required]");
      for (let input of inputs) {
        if (!input.value.trim()) {
          alert("Please fill in all fields before continuing.");
          return;
        }
      }
      step1.style.display = "none";
      step2.style.display = "block";
    };

    window.backToStep1 = (modalId) => {
      const modal = document.getElementById(modalId);
      if (!modal) return;
      if (modalId === "petSitterModal") {
        modal.querySelector("#sitter-step2").style.display = "none";
        modal.querySelector("#sitter-step1").style.display = "block";
      } else if (modalId === "petOwnerModal") {
        modal.querySelector("#owner-step2").style.display = "none";
        modal.querySelector("#owner-step1").style.display = "block";
      }
    };

    // Click-outside closes register-related modals
    window.addEventListener("click", (e) => {
      const modals = [
        "registerModal",
        "petSitterModal",
        "petOwnerModal",
        "successPetSitterModal",
        "successPetOwnerModal",
      ];
      modals.forEach((id) => {
        const modal = document.getElementById(id);
        if (modal && e.target === modal) modal.classList.remove("show");
      });
    });
  }

  // If this page has a login modal, add outside-click close
  if (document.getElementById("loginModal")) {
    const loginModal = document.getElementById("loginModal");
    window.addEventListener("click", (e) => {
      if (e.target === loginModal) loginModal.classList.remove("show");
    });
  }
});
