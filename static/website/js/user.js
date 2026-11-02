/* AG-Enterprise user profile — small frontend interactions only */

(function () {
  var passwordInput = document.getElementById("password");
  var toggleBtn = document.getElementById("togglePassword");
  var logoutBtn = document.getElementById("logoutBtn");
  var logoutModal = document.getElementById("logoutModal");
  var confirmLogout = document.getElementById("confirmLogout");

  // 1. Password show / hide
  if (toggleBtn && passwordInput) {
    toggleBtn.addEventListener("click", function () {
      var showing = passwordInput.type === "text";
      var nextType = showing ? "password" : "text";

      passwordInput.type = nextType;
      toggleBtn.classList.toggle("is-visible", !showing);
      toggleBtn.setAttribute("aria-pressed", showing ? "false" : "true");
      toggleBtn.setAttribute(
        "aria-label",
        showing ? "Show password" : "Hide password",
      );
    });
  }

  function openModal() {
    if (!logoutModal) return;
    logoutModal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    if (!logoutModal) return;
    logoutModal.hidden = true;
    document.body.style.overflow = "";
  }

  // 2. Logout confirmation
  if (logoutBtn) {
    logoutBtn.addEventListener("click", openModal);
  }

  if (logoutModal) {
    logoutModal.querySelectorAll("[data-close-modal]").forEach(function (el) {
      el.addEventListener("click", closeModal);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && logoutModal && !logoutModal.hidden) {
      closeModal();
    }
  });

  // 3. Optional order card expand / collapse
  document.querySelectorAll(".order-card").forEach(function (card) {
    var toggle = card.querySelector(".order-toggle");
    if (!toggle) return;

    toggle.addEventListener("click", function () {
      var open = card.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute(
        "aria-label",
        open ? "Collapse order details" : "Expand order details",
      );
    });
  });
})();

const profileImageInput = document.getElementById("profileImageInput");
const profileImageForm = document.getElementById("profileImageForm");

if (profileImageInput && profileImageForm) {
  profileImageInput.addEventListener("change", function () {
    if (this.files.length > 0) {
      profileImageForm.submit();
    }
  });
}

window.addEventListener("load", function () {
  document.body.classList.add("loaded");
});
