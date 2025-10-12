document.addEventListener("DOMContentLoaded", () => {
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

  window.openPetSitter = () => toggleModal("registerModal", "petSitterModal");
  window.openPetOwner = () => toggleModal("registerModal", "petOwnerModal");

  window.backToSelection = () => {
    toggleModal("petSitterModal", "registerModal");
    toggleModal("petOwnerModal", "registerModal");
  };

  window.showSuccessPetSitter = () => toggleModal("petSitterModal", "successPetSitterModal");
  window.showSuccessPetOwner = () => toggleModal("petOwnerModal", "successPetOwnerModal");

  window.closeSuccessPetSitter = () => {
    toggleModal("successPetSitterModal", null);
    window.location.href = "/login";
  };

  window.closeSuccessPetOwner = () => {
    toggleModal("successPetOwnerModal", null);
    window.location.href = "/login";
  };

  // Login button
  const loginBtn = document.getElementById("loginBtn");
  if (loginBtn) {
    loginBtn.addEventListener("click", () => toggleModal(null, "loginModal"));
  }

  // Register button
  const registerBtn = document.getElementById("registerBtn");
  if (registerBtn) {
    registerBtn.addEventListener("click", () => toggleModal(null, "registerModal"));
  }

  // Switch to Register from Login modal
  const switchToRegister = document.getElementById("switchToRegister");
  if (switchToRegister) {
    switchToRegister.addEventListener("click", (e) => {
      e.preventDefault();
      toggleModal("loginModal", "registerModal");
    });
  }

  // Clicking outside modal closes it
  window.addEventListener("click", (e) => {
    const modals = [
      "loginModal",
      "registerModal",
      "petSitterModal",
      "petOwnerModal",
      "successPetSitterModal",
      "successPetOwnerModal"
    ];

    modals.forEach((id) => {
      const modal = document.getElementById(id);
      if (modal && e.target === modal) {
        modal.classList.remove("show");
      }
    });
  });
  function goToStep2() {
    const step1 = document.getElementById("step1");
    const step2 = document.getElementById("step2");

    // Simple validation
    const inputs = step1.querySelectorAll("input[required]");
    for (let input of inputs) {
      if (!input.value.trim()) {
        alert("Please fill in all fields before continuing.");
        return;
      }
    }

    step1.style.display = "none";
    step2.style.display = "block";
  }

  function goToStep1() {
    document.getElementById("step2").style.display = "none";
    document.getElementById("step1").style.display = "block";
  }

  function closePetOwnerModal() {
    document.getElementById("petOwnerModal").style.display = "none";
  }
});
