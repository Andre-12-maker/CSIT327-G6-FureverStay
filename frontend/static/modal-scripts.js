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

  // Open modals
  window.openPetSitter = () => toggleModal("registerModal", "petSitterModal");
  window.openPetOwner = () => toggleModal("registerModal", "petOwnerModal");

  // Back to selection modal
  window.backToSelection = () => {
    toggleModal("petSitterModal", "registerModal");
    toggleModal("petOwnerModal", "registerModal");
  };

  // Success modals
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

  // Login/Register buttons
  const loginBtn = document.getElementById("loginBtn");
  if (loginBtn) loginBtn.addEventListener("click", () => toggleModal(null, "loginModal"));

  const registerBtn = document.getElementById("registerBtn");
  if (registerBtn) registerBtn.addEventListener("click", () => toggleModal(null, "registerModal"));

  const switchToRegister = document.getElementById("switchToRegister");
  if (switchToRegister) {
    switchToRegister.addEventListener("click", (e) => {
      e.preventDefault();
      toggleModal("loginModal", "registerModal");
    });
  }

  // Close modal when clicking outside
  window.addEventListener("click", (e) => {
    const modals = [
      "loginModal",
      "registerModal",
      "petSitterModal",
      "petOwnerModal",
      "successPetSitterModal",
      "successPetOwnerModal"
    ];
    modals.forEach(id => {
      const modal = document.getElementById(id);
      if (modal && e.target === modal) modal.classList.remove("show");
    });
  });

  // -----------------------------
  // Step navigation for spans
  // -----------------------------

  // Pet Sitter
  window.goToSitterStep2 = () => {
    const step1 = document.querySelector("#sitter-step1");
    const step2 = document.querySelector("#sitter-step2");

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


  // Pet Owner
  window.goToOwnerStep2 = () => {
    const step1 = document.querySelector("#owner-step1");
    const step2 = document.querySelector("#owner-step2");

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



  // Back buttons for step 2
  window.backToStep1 = (modalId) => {
    const modal = document.getElementById(modalId);

    if (modalId === "petSitterModal") {
      modal.querySelector("#sitter-step2").style.display = "none";
      modal.querySelector("#sitter-step1").style.display = "block";
    } else if (modalId === "petOwnerModal") {
      modal.querySelector("#owner-step2").style.display = "none";
      modal.querySelector("#owner-step1").style.display = "block";
    }
  };

  // Optional: Close Pet Owner modal
  window.closePetOwnerModal = () => {
    document.getElementById("petOwnerModal").style.display = "none";
  };
});
