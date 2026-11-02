var toastContainer = document.getElementById("toastContainer");

function showToast(message, type) {
  if (!toastContainer) return;

  var toast = document.createElement("div");

  toast.className = "admin-toast";

  if (type === "error") {
    toast.classList.add("admin-toast--error");
  } else if (type === "warning") {
    toast.classList.add("admin-toast--warning");
  } else if (type === "info") {
    toast.classList.add("admin-toast--info");
  } else {
    toast.classList.add("admin-toast--success");
  }

  toast.setAttribute("role", "alert");

  var icon = "fa-circle-check";

  if (type === "error") {
    icon = "fa-circle-xmark";
  } else if (type === "warning") {
    icon = "fa-triangle-exclamation";
  } else if (type === "info") {
    icon = "fa-circle-info";
  }

  var iconBox = document.createElement("span");
  iconBox.className = "admin-toast-icon";

  var iconElement = document.createElement("i");
  iconElement.className = "fa-solid " + icon;
  iconElement.setAttribute("aria-hidden", "true");

  iconBox.appendChild(iconElement);

  var messageBox = document.createElement("span");
  messageBox.className = "admin-toast-message";
  messageBox.textContent = message;

  toast.appendChild(iconBox);
  toast.appendChild(messageBox);

  toastContainer.appendChild(toast);

  setTimeout(function () {
    toast.classList.add("admin-toast--hide");

    setTimeout(function () {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3500);
}

document.querySelectorAll(".django-message").forEach(function (item) {
  var message = item.getAttribute("data-message");
  var type = item.getAttribute("data-tag");

  showToast(message, type);

  item.remove();
});
