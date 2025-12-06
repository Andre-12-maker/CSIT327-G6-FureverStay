// pet_sitter_dashboard.js
document.addEventListener('DOMContentLoaded', function () {
  // Dropdown Menu (safe guards)
  const dropdownBtn = document.getElementById("userDropdown");
  const dropdownContent = document.getElementById("dropdownContent");

  if (dropdownBtn && dropdownContent) {
    dropdownBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      dropdownContent.classList.toggle("show");
      const arrow = dropdownBtn.querySelector(".arrow");
      if (arrow) arrow.textContent = dropdownContent.classList.contains("show") ? "▲" : "▼";
      dropdownContent.setAttribute('aria-hidden', !dropdownContent.classList.contains('show'));
    });

    // Close dropdown when clicking outside
    window.addEventListener("click", function (event) {
      if (!dropdownBtn.contains(event.target) && !dropdownContent.contains(event.target)) {
        dropdownContent.classList.remove("show");
        const arrow = dropdownBtn.querySelector(".arrow");
        if (arrow) arrow.textContent = "▼";
        dropdownContent.setAttribute('aria-hidden', 'true');
      }
    });
  }

  // Tabs toggle (Manage / Pending) - safe
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  if (tabButtons.length && tabContents.length) {
    tabButtons.forEach((btn) => {
      btn.addEventListener("click", function () {
        // deactivate all
        tabButtons.forEach((b) => b.classList.remove("active"));
        tabContents.forEach((c) => c.classList.add("hidden"));

        // activate target
        btn.classList.add("active");
        const target = btn.getAttribute("data-tab");
        const targetEl = document.getElementById(target);
        if (targetEl) targetEl.classList.remove("hidden");
      });
    });
  }
});

// 📅 Availability Calendar
document.addEventListener("DOMContentLoaded", function () {
  const calendarBody = document.querySelector("#calendarBody");
  const monthYearLabel = document.querySelector("#monthYear");
  const prevBtn = document.querySelector("#prevMonth");
  const nextBtn = document.querySelector("#nextMonth");

  if (!calendarBody || !monthYearLabel) return; // Safety check

  let currentDate = new Date();
  let availability = {}; // { '2025-10-31': 'available' }

  // ✅ Fetch availability from backend (added credentials)
  async function fetchAvailability() {
    try {
      const response = await fetch("/dashboard/sitter/availability/get/", {
        credentials: "same-origin", // ✅ ensures session cookies are sent
      });
      if (!response.ok) throw new Error("Failed to load availability.");
      const data = await response.json();
      availability = {};
      data.forEach((item) => {
        availability[item.date] = item.is_available ? "available" : "booked";
      });
      renderCalendar(currentDate);
    } catch (err) {
      console.error("Error fetching availability:", err);
    }
  }

  // ✅ Update availability in backend (added credentials + csrf fix)
  async function updateAvailability(dateKey, isAvailable) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    try {
      await fetch("/dashboard/sitter/availability/update/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken || "",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        credentials: "same-origin", // ✅ required for authenticated user
        body: new URLSearchParams({
          date: dateKey,
          is_available: isAvailable,
        }),
      });
    } catch (err) {
      console.error("Error updating availability:", err);
    }
  }

  function renderCalendar(date) {
    const year = date.getFullYear();
    const month = date.getMonth();

    // Set label
    const monthNames = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];
    monthYearLabel.textContent = `${monthNames[month]} ${year}`;

    // Clear calendar
    calendarBody.innerHTML = "";

    // Get days
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    let row = document.createElement("tr");

    // Empty cells before first day
    for (let i = 0; i < firstDay; i++) {
      row.appendChild(document.createElement("td"));
    }

    for (let day = 1; day <= lastDate; day++) {
      const cell = document.createElement("td");
      cell.textContent = day;

      const dateKey = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;

      // Apply class if available/booked
      if (availability[dateKey] === "available") cell.classList.add("available");
      if (availability[dateKey] === "booked") cell.classList.add("booked");

      // Toggle availability (and send to backend)
      cell.addEventListener("click", () => {
        if (availability[dateKey] === "available") {
          availability[dateKey] = "booked";
          cell.classList.remove("available");
          cell.classList.add("booked");
          updateAvailability(dateKey, false);
        } else if (availability[dateKey] === "booked") {
          delete availability[dateKey];
          cell.classList.remove("booked");
          updateAvailability(dateKey, false);
        } else {
          availability[dateKey] = "available";
          cell.classList.add("available");
          updateAvailability(dateKey, true);
        }
      });

      row.appendChild(cell);

      // Break after Saturday
      if ((firstDay + day) % 7 === 0 || day === lastDate) {
        calendarBody.appendChild(row);
        row = document.createElement("tr");
      }
    }
  }

  // Navigation
  if (prevBtn) prevBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar(currentDate);
  });

  if (nextBtn) nextBtn.addEventListener("click", () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar(currentDate);
  });

  // ✅ Initial load: fetch data before rendering
  fetchAvailability();
});

document.addEventListener("DOMContentLoaded", () => {
  const csrfToken = document.querySelector("#csrf-form input[name='csrfmiddlewaretoken']")?.value;

  document.querySelectorAll(".accept-btn, .decline-btn").forEach(button => {
    button.addEventListener("click", () => {
      const bookingId = button.dataset.id;
      const action = button.classList.contains("accept-btn") ? "accept" : "decline";
      console.log("Clicked:", bookingId, action); // ✅ Debug

      fetch("/dashboard/sitter/update-booking-status/", {
        method: "POST",
        credentials: "same-origin", // ✅ send session cookies for login + CSRF check
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          booking_id: bookingId,
          action: action
        }),
      })
      .then(response => response.json())
      .then(data => {
        console.log("Server response:", data); // ✅ Debug
        if (data.success) {
          const card = button.closest(".reservation-card");
          const statusEl = card.querySelector(".status");
          statusEl.textContent = data.status.charAt(0).toUpperCase() + data.status.slice(1);
          statusEl.className = `status ${data.status}`;
          card.querySelector(".reservation-actions").innerHTML = `<p class="status-label">${data.status.toUpperCase()}</p>`;
        } else {
          alert(data.error || "Something went wrong");
        }
      })
      .catch(err => console.error("Error:", err));
    });
  });
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

document.addEventListener("DOMContentLoaded", () => {
    const csrfToken = document.querySelector("#csrf-form input[name='csrfmiddlewaretoken']").value;

    document.querySelectorAll(".complete-btn").forEach(button => {
        button.addEventListener("click", () => {
            const bookingId = button.dataset.id;

            fetch("/dashboard/sitter/complete-booking/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    booking_id: bookingId
                }),
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    button.textContent = "✔ Completed";
                    button.disabled = true;
                    button.classList.add("completed");

                    // Optional: visually remove card
                    // button.closest(".schedule-card").remove();
                } else {
                    alert(data.error || "Could not complete booking.");
                }
            });
        });
    });
});
