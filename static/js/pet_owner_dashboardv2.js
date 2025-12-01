  // ===============================
  // FureverStay Dashboard JS
  // ===============================

  // Dropdown toggle
  const dropdownBtn = document.getElementById("dropdown-btn");
  const dropdownMenu = document.querySelector(".dropdown-content");

  dropdownBtn?.addEventListener("click", () => {
    dropdownMenu.classList.toggle("hidden");
    dropdownMenu.style.display = dropdownMenu.classList.contains("hidden") ? "none" : "flex";
  });

  // Close dropdown when clicking outside
  window.addEventListener("click", (e) => {
    if (!dropdownBtn?.contains(e.target) && !dropdownMenu?.contains(e.target)) {
      dropdownMenu?.classList.add("hidden");
      if (dropdownMenu) dropdownMenu.style.display = "none";
    }
  });

  // ===============================
  // SEARCH & FILTER HANDLING (Dashboard Page Only)
  // ===============================
  const searchForm = document.getElementById("searchForm");
  const resultsGrid = document.getElementById("resultsGrid");

  if (searchForm && resultsGrid) {
    searchForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const location = document.getElementById("locationInput").value;
      const minPrice = document.getElementById("minPrice").value;
      const maxPrice = document.getElementById("maxPrice").value;
      const availability = document.getElementById("availabilityFilter").value;
      const sortOrder = document.getElementById("sortPrice").value;

      // Construct query parameters (only add if not empty)
      const params = new URLSearchParams();
      if (location) params.append("location", location);
      if (minPrice) params.append("min_price", minPrice);
      if (maxPrice) params.append("max_price", maxPrice);
      if (availability) params.append("availability", availability);

      try {
        const response = await fetch(`${fetchSittersURL}?${params.toString()}`);
        if (!response.ok) throw new Error("Failed to fetch sitters.");

        const data = await response.json();
        let sitters = data.sitters || [];

        // Sort by price
        if (sortOrder === "asc") sitters.sort((a, b) => a.hourly_rate - b.hourly_rate);
        if (sortOrder === "desc") sitters.sort((a, b) => b.hourly_rate - a.hourly_rate);
        resultsGrid.innerHTML = sitters.length
          ? sitters.map((s) => {
              const img = s.profile_image_url || "/static/assets/default_profile.png";
              const isSaved = window.savedSitters?.includes(s.sitter_id);
              const saveButtonHTML = isSaved
                  ? `<button class="save-btn saved" data-id="${s.sitter_id}">✓ Saved</button>`
                  : `<button class="save-btn" data-id="${s.sitter_id}">♡ Save</button>`;
              return `
                <div class="sitter-card">
                    <img src="${img}" alt="Sitter">
                    <div class="sitter-info">
                        <h4>${s.first_name} ${s.last_name}</h4>
                        <p>${s.bio || 'No bio provided.'}</p>
                        <p>📍 ${s.address || 'No address'}</p>
                        <p>🕒 Availability: ${s.availability || 'Not specified'}</p>
                        <p class="sitter-rate">₱${s.hourly_rate || '—'} / hr</p>
                    </div>
                    <div class="card-actions">
                        <button class="view-profile-btn" data-sitter-id="${s.sitter_id}">View Profile</button>
                        ${saveButtonHTML}
                    </div>
                </div>
              `;
          }).join("")
          : `<p>No sitters found.</p>`;
        // Click event to view profile
        document.querySelectorAll(".view-profile-btn").forEach((btn) => {
          btn.addEventListener("click", (e) => {
            const sitterId = e.target.dataset.sitterId;
            if (sitterId) {
              window.location.href = `/dashboard/owner/view_sitter_profile/${sitterId}/`;
            }
          });
        });
      } catch (err) {
        console.error(err);
        resultsGrid.innerHTML = `<p class="error">⚠️ Unable to fetch sitters right now.</p>`;
      }
    });
  }

  // ===============================
  // SITTER AVAILABILITY CALENDAR (View Profile Page Only)
  // ===============================
  document.addEventListener("DOMContentLoaded", function () {
    const calendarBody = document.querySelector("#calendarBody");
    if (!calendarBody) return; // prevent errors on other pages

    const sitterId = document.getElementById("calendarBody").dataset.sitterId;
    const monthYearLabel = document.querySelector("#monthYear");
    const prevBtn = document.querySelector("#prevMonth");
    const nextBtn = document.querySelector("#nextMonth");

    let currentDate = new Date();
    let availability = {};

    async function fetchAvailability() {
      try {
        const response = await fetch(`/dashboard/sitter/${sitterId}/availability/`);
        const data = await response.json();
        availability = {};
        data.forEach((item) => {
          availability[item.date] = item.is_available ? "available" : "unavailable";
        });
        renderCalendar(currentDate);
      } catch (err) {
        console.error("Error fetching availability:", err);
      }
    }

    function renderCalendar(date) {
      const year = date.getFullYear();
      const month = date.getMonth();
      const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
      ];

      if (monthYearLabel) monthYearLabel.textContent = `${monthNames[month]} ${year}`;
      calendarBody.innerHTML = "";

      const firstDay = new Date(year, month, 1).getDay();
      const lastDate = new Date(year, month + 1, 0).getDate();

      let row = document.createElement("tr");

      // Fill empty cells before the 1st day of the month
      for (let i = 0; i < firstDay; i++) {
        const emptyCell = document.createElement("td");
        row.appendChild(emptyCell);
      }

      for (let day = 1; day <= lastDate; day++) {
        const cell = document.createElement("td");
        cell.textContent = day;

        const dateKey = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
        if (availability[dateKey]) {
          cell.classList.add(availability[dateKey]); // add available/unavailable class
        }

        row.appendChild(cell);

        // If Saturday or last day, append the row and start a new one
        if ((firstDay + day) % 7 === 0 || day === lastDate) {
          calendarBody.appendChild(row);
          row = document.createElement("tr");
        }
      }
    }


    prevBtn?.addEventListener("click", () => {
      currentDate.setMonth(currentDate.getMonth() - 1);
      renderCalendar(currentDate);
    });

    nextBtn?.addEventListener("click", () => {
      currentDate.setMonth(currentDate.getMonth() + 1);
      renderCalendar(currentDate);
    });

    fetchAvailability();
  });

// ===============================
// BOOKING MODAL (View Profile Page Only)
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("bookingModal");
  const openBtn = document.querySelector(".book-btn");
  const closeBtn = document.querySelector(".cancel-btn");

  if (!modal || !openBtn || !closeBtn) return; // ✅ Safely skip on pages without modal

  const totalPriceText = document.getElementById("totalPrice");
  const startInput = document.getElementById("start_date");
  const endInput = document.getElementById("end_date");
  const hoursInput = document.getElementById("hours_per_day");

  // 🟢 Open modal
  openBtn.addEventListener("click", () => {
    modal.classList.remove("hidden");
    // store hourly rate in modal dataset for easy access
    modal.dataset.hourlyRate = parseFloat(openBtn.dataset.hourlyRate || 0);
    attachBookingListeners();
  });

  // 🔴 Close modal
  function closeModal() {
    modal.classList.add("hidden");
  }
  closeBtn.addEventListener("click", closeModal);

  // 🧩 Set up listeners once modal opens
  function attachBookingListeners() {
    const petCheckboxes = document.querySelectorAll('input[name="pets"]');
    const hourlyRate = parseFloat(modal.dataset.hourlyRate || 0);

    function calculateTotal() {
      const start = new Date(startInput.value);
      const end = new Date(endInput.value);
      const hoursPerDay = parseFloat(hoursInput.value) || 0;
      const selectedPets = Array.from(petCheckboxes).filter(p => p.checked).length;

      if (isNaN(start) || isNaN(end) || end < start || hoursPerDay <= 0 || selectedPets === 0) {
        totalPriceText.textContent = "0.00";
        return;
      }

      const days = (end - start) / (1000 * 60 * 60 * 24) + 1;
      const total = days * hoursPerDay * hourlyRate * selectedPets;
      totalPriceText.textContent = total.toFixed(2);
    }

    // ✅ Add listeners that trigger recalculation
    [startInput, endInput, hoursInput].forEach((input) => {
      input.removeEventListener("change", calculateTotal);
      input.addEventListener("change", calculateTotal);
      input.addEventListener("input", calculateTotal);
    });

    petCheckboxes.forEach((cb) => {
      cb.removeEventListener("change", calculateTotal);
      cb.addEventListener("change", calculateTotal);
    });

    // Trigger once initially
    calculateTotal();
  }
});

//saved sitters loading
function loadSavedSitters() {
    fetch("/dashboard/owner/saved_sitters/")
        .then(res => res.json())
        .then(data => {
            renderSavedSitters(data.saved);
            window.savedSitters = data.saved.map(s => s.id); // store IDs for toggles
        });
}
function renderSavedSitters(list) {
    const box = document.getElementById("savedSittersBox");
    if (list.length === 0) {
        box.innerHTML = "<p>No saved sitters yet.</p>";
        return;
    }
    box.innerHTML = list.map(s => {
        const imgSrc = s.image && s.image !== "" 
            ? s.image 
            : "/static/assets/default_profile.png";
        return `
            <div class="saved-card">
                <img src="${imgSrc}" class="saved-img" alt="Sitter Image">
                <h4>${s.first_name} ${s.last_name}</h4>
                <p>${s.address}</p>
                <p>₱${s.hourly_rate}/hr</p>
                <button class="remove-btn" data-id="${s.id}">Remove</button>
            </div>
        `;
    }).join("");
}
document.addEventListener("click", e => {
    const id = e.target.dataset.id;

    // UNSAVE
    if (e.target.classList.contains("remove-btn")) {
        fetch(`/dashboard/owner/remove_sitter/${id}/`)
            .then(() => loadSavedSitters());
    }

    // SAVE from search results
    if (e.target.classList.contains("save-btn")) {
        fetch(`/dashboard/owner/save_sitter/${id}/`)
            .then(() => loadSavedSitters());
    }
});
document.addEventListener("DOMContentLoaded", () => {
    loadSavedSitters();
});

//notifications
document.addEventListener("DOMContentLoaded", function () {
  const bell = document.getElementById("notifBell");
  const dropdown = document.getElementById("notifDropdown");
  const notifList = document.getElementById("notifList");
  const notifCount = document.getElementById("notifCount");
  const markAllBtn = document.getElementById("markAllBtn");
  window.loadNotifications = async function () {
    const res = await fetch("/dashboard/notifications/");
    const data = await res.json();
    notifList.innerHTML = "";
    let unreadCount = 0;
    data.notifications.forEach(notif => {
      if (!notif.is_read) unreadCount++;
      notifList.innerHTML += `
        <li class="notif-item ${notif.is_read ? '' : 'unread'}">
          ${notif.message}
          <br>
          <small>${notif.created_at}</small>
        </li>
      `;
    });
    if (unreadCount > 0) {
      notifCount.textContent = unreadCount;
      notifCount.classList.remove("hidden");
    } else {
      notifCount.classList.add("hidden");
    }
  };
  // Toggle dropdown
  bell.addEventListener("click", () => {
    dropdown.classList.toggle("hidden");
    loadNotifications();
  });
  // Mark all as read
  markAllBtn?.addEventListener("click", async () => {
    await fetch("/dashboard/notifications/mark-all/");
    loadNotifications();
    notifCount.classList.add("hidden");
  });
  loadNotifications();
});
