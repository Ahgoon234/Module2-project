document.addEventListener("DOMContentLoaded", function () {
  var toast = document.getElementById("errorPageToast");
  var backButton = document.getElementById("errorPageBackButton");
  var audio = document.getElementById("errorPageAudio");

  if (toast) {
    toast.classList.add("is-visible");
  }

  if (!backButton || !audio) {
    console.error("Back button or audio element was not found.");
    return;
  }

  var isRedirecting = false;

  function resetButton() {
    backButton.classList.remove("is-loading");
    backButton.removeAttribute("aria-disabled");
    backButton.removeAttribute("aria-busy");
  }

  function redirectToPage() {
    if (isRedirecting) {
      return;
    }

    isRedirecting = true;
    window.location.href = backButton.href;
  }

  backButton.addEventListener("click", function (event) {
    event.preventDefault();

    if (isRedirecting) {
      return;
    }

    backButton.classList.add("is-loading");
    backButton.setAttribute("aria-disabled", "true");
    backButton.setAttribute("aria-busy", "true");

    // Try to play the audio directly after the button click.
    var playPromise = audio.play();

    if (playPromise !== undefined) {
      playPromise.catch(function (error) {
        console.error("Audio playback failed:", error);
        resetButton();
      });
    }
  });

  // Redirect only when playback finishes.
  audio.addEventListener("ended", redirectToPage);

  // If the audio file cannot load, show the error instead
  // of redirecting immediately.
  audio.addEventListener("error", function () {
    console.error(
      "Audio file could not be loaded:",
      audio.currentSrc,
      audio.error,
    );

    resetButton();
  });
});
