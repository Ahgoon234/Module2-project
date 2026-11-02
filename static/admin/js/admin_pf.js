(function adminPfBootstrap() {
  "use strict";

  var adminPfRoot = document.getElementById("admin-pf-root");
  if (
    !adminPfRoot ||
    adminPfRoot.getAttribute("data-admin-pf-ready") === "true"
  ) {
    return;
  }
  adminPfRoot.setAttribute("data-admin-pf-ready", "true");

  var adminPfPhoto = document.getElementById("admin-pf-photo");
  var adminPfEditPhoto = document.getElementById("admin-pf-edit-photo");
  var adminPfPhotoInput = document.getElementById("admin-pf-photo-input");
  var adminPfPhotoFeedback = document.getElementById("admin-pf-photo-feedback");
  var adminPfLogout = document.getElementById("admin-pf-logout");
  var adminPfModal = document.getElementById("admin-pf-logout-modal");

  function adminPfSetFeedback(message, isError) {
    if (!adminPfPhotoFeedback) {
      return;
    }
    adminPfPhotoFeedback.textContent = message || "";
    if (isError) {
      adminPfPhotoFeedback.classList.add("is-error");
    } else {
      adminPfPhotoFeedback.classList.remove("is-error");
    }
  }

  function adminPfOpenPicker() {
    if (adminPfPhotoInput) {
      adminPfPhotoInput.click();
    }
  }

  function adminPfHandlePhotoChange() {
    if (
      !adminPfPhotoInput ||
      !adminPfPhotoInput.files ||
      !adminPfPhotoInput.files[0]
    ) {
      return;
    }

    var adminPfFile = adminPfPhotoInput.files[0];

    if (!adminPfFile.type || adminPfFile.type.indexOf("image/") !== 0) {
      adminPfPhotoInput.value = "";
      adminPfSetFeedback("Please choose an image file.", true);
      return;
    }

    // Disable button while uploading
    if (adminPfEditPhoto) {
      adminPfEditPhoto.disabled = true;
      adminPfEditPhoto.textContent = "Saving...";
    }

    adminPfSetFeedback("Uploading profile photo...", false);

    // Submit image to Django
    var adminPfPhotoForm = document.getElementById("admin-pf-photo-form");

    if (adminPfPhotoForm) {
      adminPfPhotoForm.submit();
    }
  }

  function adminPfHandlePhotoError() {
    adminPfSetFeedback("The selected image could not be displayed.", true);
  }

  function adminPfOpenModal() {
    if (!adminPfModal) {
      return;
    }
    adminPfModal.hidden = false;
  }

  function adminPfCloseModal() {
    if (!adminPfModal) {
      return;
    }
    adminPfModal.hidden = true;
  }

  if (adminPfEditPhoto) {
    adminPfEditPhoto.addEventListener("click", adminPfOpenPicker);
  }
  if (adminPfPhotoInput) {
    adminPfPhotoInput.addEventListener("change", adminPfHandlePhotoChange);
  }
  if (adminPfPhoto) {
    adminPfPhoto.addEventListener("error", adminPfHandlePhotoError);
  }
  if (adminPfLogout) {
    adminPfLogout.addEventListener("click", adminPfOpenModal);
  }

  adminPfRoot
    .querySelectorAll("[data-admin-pf-close-modal]")
    .forEach(function (adminPfCloseBtn) {
      adminPfCloseBtn.addEventListener("click", adminPfCloseModal);
    });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && adminPfModal && !adminPfModal.hidden) {
      adminPfCloseModal();
    }
  });
})();

window.addEventListener("load", function () {
  document.body.classList.add("loaded");
});
