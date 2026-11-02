(function () {
  "use strict";

  var MOBILE_BREAKPOINT = 992;
  var body = document.body;
  var sidebar = document.getElementById("adminSidebar");
  var sidebarToggle = document.getElementById("sidebarToggle");
  var sidebarBackdrop = document.getElementById("sidebarBackdrop");
  var sidebarMobileClose = document.getElementById("sidebarMobileClose");
  var sidebarFlyout = document.getElementById("sidebarFlyout");
  var sidebarFlyoutTitle = document.getElementById("sidebarFlyoutTitle");
  var sidebarFlyoutList = document.getElementById("sidebarFlyoutList");
  var sidebarTooltip = document.getElementById("sidebarTooltip");
  var currentPageTitle = document.getElementById("currentPageTitle");
  var demoToastBtn = document.getElementById("demoToastBtn");

  var adminApp = document.getElementById("adminApp");
  var profileDropdown = document.getElementById("profileDropdown");
  var profileDropdownMenu = document.getElementById("profileDropdownMenu");

  var activeFlyoutItem = null;
  var tooltipTarget = null;

  /* ----------------------------------------------------------
     Utilities
  ---------------------------------------------------------- */
  function isMobile() {
    return window.innerWidth < MOBILE_BREAKPOINT;
  }

  function isCollapsed() {
    return body.classList.contains("sidebar-collapsed") && !isMobile();
  }

  /* ----------------------------------------------------------
     Preloader
  ---------------------------------------------------------- */
  function initPreloader() {
    function hidePreloader() {
      body.classList.add("loaded");

      if (adminApp) {
        adminApp.setAttribute("aria-hidden", "false");
      }
    }

    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () {
        setTimeout(hidePreloader, 100);
      });
    } else {
      setTimeout(hidePreloader, 100);
    }
  }
  /* ----------------------------------------------------------
     Desktop sidebar toggle
  ---------------------------------------------------------- */
  function updateToggleAria() {
    if (!sidebarToggle) return;

    if (isMobile()) {
      sidebarToggle.setAttribute(
        "aria-expanded",
        body.classList.contains("sidebar-mobile-open"),
      );
      sidebarToggle.setAttribute("aria-label", "Open navigation menu");
    } else {
      var expanded = !body.classList.contains("sidebar-collapsed");
      sidebarToggle.setAttribute("aria-expanded", expanded);
      sidebarToggle.setAttribute(
        "aria-label",
        expanded ? "Collapse sidebar navigation" : "Expand sidebar navigation",
      );
    }
  }

  function openMobileSidebar() {
    body.classList.add("sidebar-mobile-open");
    if (sidebarBackdrop) {
      sidebarBackdrop.setAttribute("aria-hidden", "false");
    }
    updateToggleAria();
  }

  function closeMobileSidebar() {
    body.classList.remove("sidebar-mobile-open");
    if (sidebarBackdrop) {
      sidebarBackdrop.setAttribute("aria-hidden", "true");
    }
    updateToggleAria();
  }

  function toggleDesktopSidebar() {
    body.classList.toggle("sidebar-collapsed");
    body.classList.toggle("sidebar-expanded");

    closeFlyout();
    hideTooltip();
    updateToggleAria();
  }

  function handleSidebarToggle() {
    if (isMobile()) {
      if (body.classList.contains("sidebar-mobile-open")) {
        closeMobileSidebar();
      } else {
        openMobileSidebar();
      }
    } else {
      toggleDesktopSidebar();
    }
  }

  /* ----------------------------------------------------------
     Expanded submenus
  ---------------------------------------------------------- */
  function closeAllSubmenus(except) {
    document
      .querySelectorAll(".nav-item.has-submenu.open")
      .forEach(function (item) {
        if (item !== except) {
          item.classList.remove("open");
          var btn = item.querySelector(".nav-toggle");
          if (btn) btn.setAttribute("aria-expanded", "false");
        }
      });
  }

  function toggleSubmenu(navItem) {
    var isOpen = navItem.classList.contains("open");
    closeAllSubmenus(navItem);

    if (!isOpen) {
      navItem.classList.add("open");
      var btn = navItem.querySelector(".nav-toggle");
      if (btn) btn.setAttribute("aria-expanded", "true");
    } else {
      navItem.classList.remove("open");
      var toggleBtn = navItem.querySelector(".nav-toggle");
      if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "false");
    }
  }

  function initSubmenus() {
    document
      .querySelectorAll(".nav-item.has-submenu")
      .forEach(function (navItem) {
        var toggle = navItem.querySelector(".nav-toggle");
        if (!toggle) return;

        toggle.addEventListener("click", function (e) {
          e.preventDefault();

          if (isCollapsed()) {
            openFlyout(navItem, toggle);
            return;
          }

          if (isMobile()) {
            toggleSubmenu(navItem);
            return;
          }

          toggleSubmenu(navItem);
        });
      });
  }

  /* ----------------------------------------------------------
     Collapsed flyout submenus
  ---------------------------------------------------------- */
  function closeFlyout() {
    if (!sidebarFlyout) return;
    sidebarFlyout.classList.remove("visible");
    sidebarFlyout.setAttribute("aria-hidden", "true");

    if (activeFlyoutItem) {
      activeFlyoutItem.classList.remove("flyout-active");
      activeFlyoutItem = null;
    }
  }

  function openFlyout(navItem, toggleEl) {
    if (!sidebarFlyout || !sidebarFlyoutList || !sidebarFlyoutTitle) return;

    if (
      activeFlyoutItem === navItem &&
      sidebarFlyout.classList.contains("visible")
    ) {
      closeFlyout();
      return;
    }

    closeFlyout();

    var title = navItem.getAttribute("data-flyout-title") || "Menu";
    var submenu = navItem.querySelector(".submenu");
    if (!submenu) return;

    sidebarFlyoutTitle.textContent = title;
    sidebarFlyoutList.innerHTML = "";

    submenu.querySelectorAll("a").forEach(function (link) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = link.getAttribute("href") || "#";
      a.textContent = link.textContent.trim();
      li.appendChild(a);
      sidebarFlyoutList.appendChild(li);
    });

    var rect = toggleEl.getBoundingClientRect();
    var flyoutTop = rect.top;
    var flyoutLeft = rect.right + 8;

    sidebarFlyout.style.top = flyoutTop + "px";
    sidebarFlyout.style.left = flyoutLeft + "px";

    var flyoutRect = sidebarFlyout.getBoundingClientRect();
    if (flyoutTop + flyoutRect.height > window.innerHeight - 12) {
      sidebarFlyout.style.top =
        Math.max(12, window.innerHeight - flyoutRect.height - 12) + "px";
    }

    if (flyoutLeft + 200 > window.innerWidth - 12) {
      sidebarFlyout.style.left = rect.left - 208 + "px";
    }

    sidebarFlyout.classList.add("visible");
    sidebarFlyout.setAttribute("aria-hidden", "false");
    navItem.classList.add("flyout-active");
    activeFlyoutItem = navItem;
  }

  /* ----------------------------------------------------------
     Tooltips (collapsed sidebar)
  ---------------------------------------------------------- */
  function hideTooltip() {
    if (!sidebarTooltip) return;
    sidebarTooltip.classList.remove("visible");
    sidebarTooltip.setAttribute("aria-hidden", "true");
    tooltipTarget = null;
  }

  function showTooltip(target, label) {
    if (!sidebarTooltip || !label || isMobile()) return;

    tooltipTarget = target;
    sidebarTooltip.textContent = label;

    var rect = target.getBoundingClientRect();
    sidebarTooltip.style.top =
      rect.top + rect.height / 2 - sidebarTooltip.offsetHeight / 2 + "px";
    sidebarTooltip.style.left = rect.right + 10 + "px";

    sidebarTooltip.classList.add("visible");
    sidebarTooltip.setAttribute("aria-hidden", "false");
  }

  function initTooltips() {
    sidebar.querySelectorAll(".nav-link, .nav-toggle").forEach(function (link) {
      link.addEventListener("mouseenter", function () {
        if (!isCollapsed()) return;

        var labelEl = link.querySelector(".nav-label");
        var label = labelEl ? labelEl.textContent.trim() : "";
        if (label === "Contact Messages") label = "Messages";
        if (label) showTooltip(link, label);
      });

      link.addEventListener("mouseleave", hideTooltip);
      link.addEventListener("focus", function () {
        if (!isCollapsed()) return;
        var labelEl = link.querySelector(".nav-label");
        var label = labelEl ? labelEl.textContent.trim() : "";
        if (label === "Contact Messages") label = "Messages";
        if (label) showTooltip(link, label);
      });
      link.addEventListener("blur", hideTooltip);
    });
  }

  /* ----------------------------------------------------------
     Page title from nav clicks
  ---------------------------------------------------------- */
  function isPlaceholderHref(href) {
    return !href || href === "#";
  }

  function initNavPageTitles() {
    sidebar.querySelectorAll(".nav-link[data-page]").forEach(function (link) {
      link.addEventListener("click", function (e) {
        if (isPlaceholderHref(link.getAttribute("href"))) {
          e.preventDefault();
        }

        var page = link.getAttribute("data-page");
        if (page && currentPageTitle) {
          currentPageTitle.textContent = page;
        }

        sidebar.querySelectorAll(".nav-item").forEach(function (item) {
          item.classList.remove("active");
        });
        link.closest(".nav-item").classList.add("active");

        if (isMobile()) closeMobileSidebar();
        closeFlyout();
      });
    });

    sidebar.querySelectorAll(".submenu a").forEach(function (link) {
      link.addEventListener("click", function (e) {
        if (isPlaceholderHref(link.getAttribute("href"))) {
          e.preventDefault();
        }
        closeFlyout();
        if (isMobile()) closeMobileSidebar();
      });
    });

    if (sidebarFlyout) {
      sidebarFlyout.addEventListener("click", function (e) {
        var anchor = e.target.closest("a");
        if (!anchor) return;
        if (isPlaceholderHref(anchor.getAttribute("href"))) {
          e.preventDefault();
        }
        closeFlyout();
      });
    }
  }

  /* ----------------------------------------------------------
     Toast demo
  ---------------------------------------------------------- */
  var toastMessages = [
    "Car added successfully.",
    "Brand updated successfully.",
    "Spare part created successfully.",
    "Blog post published successfully.",
  ];
  var toastIndex = 0;

  document.querySelectorAll(".django-message").forEach(function (item) {
    var message = item.getAttribute("data-message");
    var type = item.getAttribute("data-tag");

    showToast(message, type);

    item.remove();
  });

  /* ----------------------------------------------------------
     Outside click & Escape
  ---------------------------------------------------------- */
  function initGlobalListeners() {
    document.addEventListener("click", function (e) {
      if (
        isCollapsed() &&
        sidebarFlyout &&
        sidebarFlyout.classList.contains("visible")
      ) {
        var clickedInsideFlyout = sidebarFlyout.contains(e.target);
        var clickedNavToggle = e.target.closest(".nav-toggle");
        if (!clickedInsideFlyout && !clickedNavToggle) {
          closeFlyout();
        }
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        closeFlyout();
        hideTooltip();
        if (isMobile()) closeMobileSidebar();
      }
    });

    window.addEventListener("resize", function () {
      hideTooltip();
      closeFlyout();

      if (!isMobile()) {
        closeMobileSidebar();
        body.classList.add("sidebar-expanded");
      } else {
        body.classList.remove("sidebar-collapsed");
      }

      updateToggleAria();
    });
  }

  /* ----------------------------------------------------------
     Profile dropdown (vanilla — no Popper required)
  ---------------------------------------------------------- */
  function closeProfileDropdown() {
    if (!profileDropdown || !profileDropdownMenu) return;
    profileDropdown.setAttribute("aria-expanded", "false");
    profileDropdownMenu.classList.remove("show");
  }

  function initProfileDropdown() {
    if (!profileDropdown || !profileDropdownMenu) return;

    profileDropdown.addEventListener("click", function (e) {
      e.stopPropagation();
      var isOpen = profileDropdownMenu.classList.contains("show");
      closeProfileDropdown();
      if (!isOpen) {
        profileDropdown.setAttribute("aria-expanded", "true");
        profileDropdownMenu.classList.add("show");
      }
    });

    document.addEventListener("click", function (e) {
      if (
        !profileDropdown.contains(e.target) &&
        !profileDropdownMenu.contains(e.target)
      ) {
        closeProfileDropdown();
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeProfileDropdown();
    });
  }

  /* ----------------------------------------------------------
     Event bindings
  ---------------------------------------------------------- */
  function initEvents() {
    if (sidebarToggle) {
      sidebarToggle.addEventListener("click", handleSidebarToggle);
    }

    if (sidebarBackdrop) {
      sidebarBackdrop.addEventListener("click", closeMobileSidebar);
    }

    if (sidebarMobileClose) {
      sidebarMobileClose.addEventListener("click", closeMobileSidebar);
    }

    if (demoToastBtn) {
      demoToastBtn.addEventListener("click", function () {
        showToast(toastMessages[toastIndex % toastMessages.length]);
        toastIndex++;
      });
    }
  }

  /* ----------------------------------------------------------
     Init
  ---------------------------------------------------------- */
  function init() {
    initPreloader();
    initSubmenus();
    initTooltips();
    initNavPageTitles();
    initGlobalListeners();
    initProfileDropdown();
    initEvents();
    updateToggleAria();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

/* ----------------------------------------------------------
   Create / Edit modal forms
---------------------------------------------------------- */
(function () {
  "use strict";

  var moduleLabels = {
    car: "Car",
    category: "Category",
    brand: "Brand",
    sparepart: "Sparepart",
    partcategory: "Part Category",
    blog: "Blog",
    contact: "Contact Message",
  };
  var activeModal = null;
  var activeForm = null;
  var activeModule = null;
  var returnFocus = null;
  var galleryState = [];

  function cleanText(cell) {
    return cell ? cell.textContent.trim() : "";
  }

  function cleanNumber(value) {
    var match = String(value || "")
      .replace(/,/g, "")
      .match(/-?\d+(?:\.\d+)?/);
    return match ? Number(match[0]) : "";
  }

  function getRowItem(module, row) {
    var cells = row ? row.cells : [];
    var first = cleanText(cells[0]);
    if (module === "car") {
      var gallery = [];

      if (row) {
        try {
          gallery = JSON.parse(row.getAttribute("data-gallery") || "[]");
        } catch (error) {
          console.error("Invalid car gallery data:", error);
        }
      }

      return {
        id: row ? row.getAttribute("data-car-id") : "",
        name: row ? row.getAttribute("data-name") : "",
        brand: row ? row.getAttribute("data-brand") : "",
        category: row ? row.getAttribute("data-category") : "",
        price: row ? row.getAttribute("data-price") : "",
        stock: row ? row.getAttribute("data-stock") : "",
        year: row ? row.getAttribute("data-year") : "",
        mileage: row ? row.getAttribute("data-mileage") : "",
        color: row ? row.getAttribute("data-color") : "",
        fuel_type: row ? row.getAttribute("data-fuel-type") : "",
        transmission: row ? row.getAttribute("data-transmission") : "",
        engine: row ? row.getAttribute("data-engine") : "",
        horsepower: row ? row.getAttribute("data-horsepower") : "",
        description: row ? row.getAttribute("data-description") : "",
        condition: row ? row.getAttribute("data-condition") : "",
        is_featured: row && row.getAttribute("data-featured") === "true",

        thumbnail: row ? row.getAttribute("data-thumbnail") : "",
        gallery: gallery,
      };
    }
    if (module === "category") {
      return {
        id: row ? row.getAttribute("data-category-id") : "",
        name: first,
        image: row ? row.querySelector(".category_img")?.src || "" : "",
      };
    }
    if (module === "brand") {
      return {
        id: row ? row.getAttribute("data-brand-id") : "",
        title: first,
        logo: row ? row.querySelector(".brand_img")?.src || "" : "",
      };
    }
    if (module === "sparepart") {
      var gallery = [];

      if (row) {
        try {
          gallery = JSON.parse(row.getAttribute("data-gallery") || "[]");
        } catch (error) {
          console.error("Invalid sparepart gallery data:", error);
        }
      }

      return {
        id: row ? row.getAttribute("data-sparepart-id") : "",
        name: row ? row.getAttribute("data-name") : "",
        partcategory: row ? row.getAttribute("data-partcategory") : "",
        brand: row ? row.getAttribute("data-brand") : "",
        price: row ? row.getAttribute("data-price") : "",
        stock: row ? row.getAttribute("data-stock") : "",
        description: row ? row.getAttribute("data-description") : "",
        thumbnail: row ? row.getAttribute("data-thumbnail") : "",
        gallery: gallery,
      };
    }
    if (module === "partcategory") {
      return {
        id: row ? row.getAttribute("data-partcategory-id") : "",
        name: first,
      };
    }
    if (module === "blog") {
      return {
        id: row ? row.getAttribute("data-blog-id") : "",
        title: row ? row.getAttribute("data-title") : "",
        content: row ? row.getAttribute("data-content") : "",
        thumbnail: row ? row.getAttribute("data-thumbnail") : "",
      };
    }
    if (module === "contact") {
      return {
        name: row ? row.getAttribute("data-name") : "",
        email: row ? row.getAttribute("data-email") : "",
        phone: row ? row.getAttribute("data-phone") : "",
        message: row ? row.getAttribute("data-message") : "",
        created_at: row ? row.getAttribute("data-created-at") : "",
        status: row ? row.getAttribute("data-status") : "",
      };
    }
    return {};
  }

  function getModal(module) {
    return document.querySelector(
      '[data-admin-modal][data-admin-module="' + module + '"]',
    );
  }

  function getForm(modal) {
    return modal ? modal.querySelector("[data-modal-form]") : null;
  }

  function setPreviewImage(image, source) {
    image.classList.remove("is-broken");
    image.onload = function () {
      image.classList.remove("is-broken");
    };
    image.onerror = function () {
      image.classList.add("is-broken");
    };
    image.src = source || "";
  }

  function setSinglePreview(input, source, filename, isExisting) {
    if (!input) return;
    var preview = document.getElementById(
      input.getAttribute("data-preview-target"),
    );
    if (!preview) return;
    var image = preview.querySelector("[data-single-preview-image]");
    var name = preview.querySelector("[data-preview-name]");
    var existing = preview.querySelector("[data-existing-image]");
    var label = input.parentElement.querySelector("[data-upload-label]");
    if (source) {
      setPreviewImage(image, source);
      name.textContent =
        filename || (isExisting ? "Existing image" : "Selected image");
      if (existing) existing.value = isExisting ? source : "";
      if (label)
        label.textContent =
          filename || (isExisting ? "Replace image" : "Image selected");
      preview.hidden = false;
    } else {
      image.removeAttribute("src");
      image.classList.remove("is-broken");
      name.textContent = "No image selected";
      if (existing) existing.value = "";
      if (label) label.textContent = "Choose image";
      preview.hidden = true;
    }
  }

  function resetForm(form) {
    if (!form) return;
    form.reset();
    form.querySelectorAll("[data-image-input]").forEach(function (input) {
      setSinglePreview(input, "", "", false);
    });
    var deletedContainer = form.querySelector("[data-deleted-images]");

    if (deletedContainer) {
      deletedContainer.innerHTML = "";
    }

    galleryState = [];

    renderGallery(form);
  }

  function createGalleryTile(entry, index, viewOnly) {
    var tile = document.createElement("div");
    tile.className = "admin-gallery-tile";
    var image = document.createElement("img");
    image.alt =
      entry.name ||
      (entry.isExisting ? "Existing gallery image" : "Selected gallery image");
    setPreviewImage(image, entry.src);
    var remove = document.createElement("button");
    remove.type = "button";
    remove.className = "admin-gallery-remove";
    remove.setAttribute("data-gallery-remove", String(index));
    remove.setAttribute("aria-label", "Remove " + image.alt);
    remove.innerHTML = '<i class="fa-solid fa-xmark" aria-hidden="true"></i>';
    if (entry.isExisting && entry.id) {
      remove.setAttribute("data-delete-image-id", entry.id);
    }

    if (viewOnly) {
      remove.disabled = true;
      remove.tabIndex = -1;
      remove.setAttribute("aria-hidden", "true");
    }
    tile.appendChild(image);
    tile.appendChild(remove);
    if (entry.isExisting) {
      var badge = document.createElement("span");
      badge.className = "admin-gallery-badge";
      badge.textContent = "Existing";
      tile.appendChild(badge);
    }
    return tile;
  }

  function renderGallery(form) {
    if (!form) return;
    var preview = form.querySelector("[data-gallery-preview]");
    if (!preview) return;
    preview.innerHTML = "";
    if (!galleryState.length) {
      var empty = document.createElement("div");
      empty.className = "admin-gallery-empty";
      empty.textContent = "No gallery images selected yet.";
      preview.appendChild(empty);
      return;
    }
    galleryState.forEach(function (entry, index) {
      preview.appendChild(
        createGalleryTile(
          entry,
          index,
          form.classList.contains("is-view-mode"),
        ),
      );
    });
  }

  function populateForm(form, item) {
    Object.keys(item).forEach(function (key) {
      var input = form.elements[key];
      if (!input) return;
      if (input.type === "checkbox") {
        input.checked = Boolean(item[key]);
      } else if (input.type !== "file" && key !== "gallery") {
        input.value = item[key] == null ? "" : item[key];
      }
    });
    var imageFields = ["image", "logo", "thumbnail"];
    imageFields.forEach(function (fieldName) {
      var input = form.elements[fieldName];
      if (input && item[fieldName])
        setSinglePreview(input, item[fieldName], "Existing image", true);
    });
    galleryState = (item.gallery || []).map(function (image, index) {
      return {
        id: image.id || "",
        src: image.src || "",
        name: "Existing gallery image " + (index + 1),
        isExisting: true,
      };
    });
    renderGallery(form);
  }

  function setFormViewMode(form, viewOnly) {
    if (!form) return;
    form.classList.toggle("is-view-mode", viewOnly);
    form.setAttribute("aria-readonly", String(viewOnly));

    form
      .querySelectorAll("input, select, textarea")
      .forEach(function (control) {
        if (control.type === "hidden") return;
        if (
          control.type === "checkbox" ||
          control.type === "file" ||
          control.tagName === "SELECT"
        ) {
          control.disabled = viewOnly;
        } else {
          control.readOnly = viewOnly;
        }
      });

    form
      .querySelectorAll("[data-clear-single], [data-gallery-remove]")
      .forEach(function (control) {
        control.disabled = viewOnly;
        control.tabIndex = viewOnly ? -1 : 0;
      });

    form.querySelectorAll(".admin-upload-control").forEach(function (control) {
      control.setAttribute("aria-disabled", String(viewOnly));
      control.tabIndex = viewOnly ? -1 : 0;
    });

    var modal = form.closest("[data-admin-modal]");
    var submit = modal && modal.querySelector("[data-submit-button]");
    if (submit) {
      submit.hidden = viewOnly;
      submit.disabled = viewOnly;
    }
    var cancel = modal && modal.querySelector("[data-modal-cancel]");
    if (cancel) {
      cancel.hidden = viewOnly;
      cancel.disabled = viewOnly;
    }
  }

  function openModal(module, mode, row, trigger) {
    var modal = getModal(module);
    var form = getForm(modal);

    if (!modal || !form) return;

    activeModal = modal;
    activeForm = form;
    activeModule = module;
    returnFocus = trigger || document.activeElement;

    setFormViewMode(form, false);
    resetForm(form);

    // Always reset form action to CREATE
    var createUrl = form.getAttribute("data-create-url");

    if (createUrl) {
      form.action = createUrl;
    }

    var label = moduleLabels[module];
    var title = modal.querySelector("[data-modal-title]");
    var subtitle = modal.querySelector("[data-modal-subtitle]");
    var submit = modal.querySelector("[data-submit-button]");

    if (mode === "view") {
      populateForm(form, getRowItem(module, row));

      title.textContent = "View " + label;

      subtitle.textContent =
        "Review the existing " + label.toLowerCase() + " in read-only mode.";

      setFormViewMode(form, true);
    } else if (mode === "edit") {
      var item = getRowItem(module, row);

      populateForm(form, item);

      title.textContent = "Edit " + label;

      subtitle.textContent =
        "Review the existing data and update this " +
        label.toLowerCase() +
        " with new data approved by the admin.";

      if (submit) {
        submit.textContent = "Update " + label;
      }

      if (
        (module === "brand" ||
          module === "category" ||
          module === "car" ||
          module === "partcategory" ||
          module === "sparepart" ||
          module === "blog") &&
        item.id
      ) {
        var updateBaseUrl = form.getAttribute("data-update-base-url");

        if (updateBaseUrl) {
          form.action = updateBaseUrl.replace(
            "00000000-0000-0000-0000-000000000000",
            item.id,
          );
        }
      }
    } else {
      var createUrl = form.getAttribute("data-create-url");

      if (createUrl) {
        form.action = createUrl;
      }

      title.textContent = "Add New " + label;

      subtitle.textContent =
        "Enter the details below to add a new " + label.toLowerCase() + ".";

      if (submit) {
        submit.textContent = "Create " + label;
      }
    }

    modal.setAttribute("data-admin-modal-mode", mode);

    modal.setAttribute("aria-hidden", "false");

    modal.classList.add("is-open");

    document.body.classList.add("modal-open");

    window.setTimeout(function () {
      var first =
        mode === "view"
          ? modal.querySelector(".admin-modal-close")
          : form.querySelector('input:not([type="file"]), select, textarea');

      if (first) {
        first.focus();
      }
    }, 50);
  }

  function closeModal() {
    if (!activeModal) return;
    setFormViewMode(activeForm, false);
    activeModal.classList.remove("is-open");
    activeModal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
    var focusTarget = returnFocus;
    activeModal = null;
    activeForm = null;
    activeModule = null;
    galleryState = [];
    if (focusTarget && typeof focusTarget.focus === "function")
      focusTarget.focus();
  }

  function handleSingleImageChange(input) {
    var file = input.files && input.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function (event) {
      setSinglePreview(input, event.target.result, file.name, false);
    };
    reader.readAsDataURL(file);
  }

  function handleGalleryChange(input, form) {
    var files = Array.prototype.slice.call(input.files || []);
    if (!files.length) return;
    files.forEach(function (file) {
      var reader = new FileReader();
      reader.onload = function (event) {
        galleryState.push({
          src: event.target.result,
          name: file.name,
          isExisting: false,
        });
        renderGallery(form);
      };
      reader.readAsDataURL(file);
    });
  }

  function initModalForms() {
    document
      .querySelectorAll('[data-admin-action="create"]')
      .forEach(function (trigger) {
        trigger.addEventListener("click", function (event) {
          event.preventDefault();
          openModal(
            trigger.getAttribute("data-admin-module"),
            "create",
            null,
            trigger,
          );
        });
      });

    document
      .querySelectorAll('[data-admin-action="edit"]')
      .forEach(function (trigger) {
        trigger.addEventListener("click", function (event) {
          event.preventDefault();
          openModal(
            trigger.getAttribute("data-admin-module"),
            "edit",
            trigger.closest("tr"),
            trigger,
          );
        });
      });

    document
      .querySelectorAll('[data-admin-action="view"]')
      .forEach(function (trigger) {
        trigger.addEventListener("click", function (event) {
          event.preventDefault();
          openModal(
            trigger.getAttribute("data-admin-module"),
            "view",
            trigger.closest("tr"),
            trigger,
          );
        });
      });

    document.querySelectorAll("[data-admin-modal]").forEach(function (modal) {
      var form = getForm(modal);
      modal
        .querySelectorAll("[data-modal-close]")
        .forEach(function (closeButton) {
          closeButton.addEventListener("click", closeModal);
        });
      modal.querySelectorAll("[data-image-input]").forEach(function (input) {
        input.addEventListener("change", function () {
          handleSingleImageChange(input);
        });
      });
      modal.querySelectorAll("[data-gallery-input]").forEach(function (input) {
        input.addEventListener("change", function () {
          handleGalleryChange(input, form);
        });
      });
      modal.addEventListener("click", function (event) {
        var removeButton = event.target.closest("[data-gallery-remove]");
        if (!removeButton) return;
        event.preventDefault();
        var index = Number(removeButton.getAttribute("data-gallery-remove"));
        if (Number.isNaN(index)) return;

        var entry = galleryState[index];

        if (!entry) return;

        if (entry.isExisting && entry.id) {
          addDeletedImageInput(form, entry.id);
        }

        galleryState.splice(index, 1);

        renderGallery(form);
      });
      modal.querySelectorAll("[data-clear-single]").forEach(function (button) {
        button.addEventListener("click", function () {
          var input = document.getElementById(
            button.getAttribute("data-input-id"),
          );
          if (input) {
            input.value = "";
            setSinglePreview(input, "", "", false);
          }
        });
      });
      if (form) {
        form.addEventListener("submit", function (event) {
          if (form.classList.contains("is-view-mode")) {
            event.preventDefault();
            return;
          }

          if (!form.checkValidity()) {
            event.preventDefault();
            form.reportValidity();
            return;
          }
        });
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && activeModal) closeModal();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initModalForms);
  } else {
    initModalForms();
  }
})();

/* ----------------------------------------------------------
   Contact message read / unread toggle
---------------------------------------------------------- */

(function () {
  "use strict";

  var modal;
  var dialog;
  var itemNameElement;
  var feedbackElement;
  var cancelButton;
  var acceptButton;
  var closeButtons;
  var selectedItem = { name: "", id: "", url: "" };
  var previouslyFocusedElement = null;

  function getComponentElements() {
    modal = document.querySelector("[data-delete-confirmation]");
    if (!modal) return false;

    dialog = modal.querySelector(".delete-confirmation__dialog");
    itemNameElement = modal.querySelector("[data-delete-item-name]");
    feedbackElement = modal.querySelector("[data-delete-feedback]");
    cancelButton = modal.querySelector("[data-delete-cancel]");
    acceptButton = modal.querySelector("[data-delete-accept]");
    closeButtons = modal.querySelectorAll("[data-delete-close]");
    return Boolean(dialog && itemNameElement && cancelButton && acceptButton);
  }

  function normaliseItem(item) {
    if (typeof item === "string") {
      return { name: item, id: "" };
    }

    item = item || {};
    return {
      name: String(item.name || item.title || "this item").trim(),
      id: item.id === undefined || item.id === null ? "" : String(item.id),
      url: item.url ? String(item.url) : "",
    };
  }

  function setModalState(isOpen) {
    if (!modal) return;

    modal.classList.toggle("is-open", isOpen);
    modal.setAttribute("aria-hidden", String(!isOpen));
    modal.hidden = !isOpen;
    document.body.classList.toggle("delete-confirmation-open", isOpen);
  }

  function resetSelectedItem() {
    selectedItem = { name: "", id: "", url: "" };
    if (itemNameElement) itemNameElement.textContent = "";
    if (feedbackElement) {
      feedbackElement.textContent = "";
      feedbackElement.hidden = true;
    }
  }

  function closeDeleteConfirmation() {
    if (!modal || !modal.classList.contains("is-open")) return;

    setModalState(false);
    resetSelectedItem();

    if (
      previouslyFocusedElement &&
      typeof previouslyFocusedElement.focus === "function"
    ) {
      previouslyFocusedElement.focus();
    }
    previouslyFocusedElement = null;
  }

  function openDeleteConfirmation(item) {
    if (!modal) return;

    selectedItem = normaliseItem(item);
    itemNameElement.textContent = selectedItem.name;
    if (feedbackElement) {
      feedbackElement.textContent = "";
      feedbackElement.hidden = true;
    }

    previouslyFocusedElement = document.activeElement;
    setModalState(true);
    dialog.focus();
  }

  function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");

      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();

        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }

    return cookieValue;
  }

  function acceptDeleteConfirmation() {
    if (!modal || !selectedItem || !selectedItem.url) {
        console.error("Delete URL is missing.");
        return;
    }

    var deleteForm = document.getElementById("deleteForm");

    if (!deleteForm) {
        console.error("Delete form is missing.");
        return;
    }

    deleteForm.action = selectedItem.url;

}

  function handleTriggerClick(event) {
    var trigger = event.target.closest("[data-delete-trigger]");
    if (!trigger) return;

    event.preventDefault();
    openDeleteConfirmation({
      name:
        trigger.getAttribute("data-delete-name") ||
        trigger.getAttribute("data-delete-title") ||
        "this item",
      id: trigger.getAttribute("data-delete-id") || "",
      url: trigger.getAttribute("href") || "",
    });
  }

  function handleKeydown(event) {
    if (!modal || !modal.classList.contains("is-open")) return;

    if (event.key === "Escape") {
      event.preventDefault();
      closeDeleteConfirmation();
      return;
    }

    if (event.key !== "Tab") return;

    var focusableElements = modal.querySelectorAll(
      'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
    );
    if (!focusableElements.length) return;

    var firstElement = focusableElements[0];
    var lastElement = focusableElements[focusableElements.length - 1];
    if (event.shiftKey && document.activeElement === firstElement) {
      event.preventDefault();
      lastElement.focus();
    } else if (!event.shiftKey && document.activeElement === lastElement) {
      event.preventDefault();
      firstElement.focus();
    }
  }

  function initDeleteConfirmation() {
    if (!getComponentElements()) return;

    document.addEventListener("click", handleTriggerClick);
    document.addEventListener("keydown", handleKeydown);

    closeButtons.forEach(function (button) {
      button.addEventListener("click", closeDeleteConfirmation);
    });
    cancelButton.addEventListener("click", closeDeleteConfirmation);
    acceptButton.addEventListener("click", acceptDeleteConfirmation);

    window.openDeleteConfirmation = openDeleteConfirmation;
    window.closeDeleteConfirmation = closeDeleteConfirmation;
    window.getSelectedDeleteItem = function () {
      return { name: selectedItem.name, id: selectedItem.id };
    };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initDeleteConfirmation);
  } else {
    initDeleteConfirmation();
  }
})();

function addDeletedImageInput(form, imageId) {
  if (!form || !imageId) return;

  var container = form.querySelector("[data-deleted-images]");

  if (!container) return;

  var exists = container.querySelector(
    'input[name="delete_images"][value="' + imageId + '"]',
  );

  if (exists) return;

  var input = document.createElement("input");

  input.type = "hidden";
  input.name = "delete_images";
  input.value = imageId;

  container.appendChild(input);
}




(function () {
  "use strict";

  var activeModal = null;
  var pendingAction = null;
  var pendingUpdateUrl = null;

  var $ = function (selector) {
    return document.querySelector(selector);
  };

  //================ Open Order Modal ================//
  function openOrder(orderId) {
    var modal = document.getElementById("orderModal-" + orderId);

    if (!modal) return;

    activeModal = modal;

    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");

    document.body.classList.add("modal-open");
  }

  //================ Close Order Modal ================//
  function closeOrder() {
    if (!activeModal) return;

    activeModal.classList.remove("is-open");
    activeModal.setAttribute("aria-hidden", "true");

    document.body.classList.remove("modal-open");

    activeModal = null;
  }

  //================ Open Confirmation ================//
  function openConfirmation(action, updateUrl) {
    pendingAction = action;
    pendingUpdateUrl = updateUrl;

    var confirmationModal = $("#orderconfirmationModal");
    var reasonField = $("#cancelReasonField");
    var reasonSelect = $("#cancelReason");
    var confirmButton = $("#orderconfirmActionButton");

    if (action === "cancel") {
      $("#orderconfirmationTitle").textContent = "Cancel Order";

      $("#orderconfirmationMessage").textContent =
        "Are you sure you want to cancel this order?";

      reasonField.hidden = false;

      reasonSelect.value = "";

      confirmButton.className =
        "order-confirmation__button order-confirmation__button--danger";
    } else {
      $("#orderconfirmationTitle").textContent = "Confirm Order";

      $("#orderconfirmationMessage").textContent =
        "Are you sure you want to confirm this order?";

      reasonField.hidden = true;

      reasonSelect.value = "";

      confirmButton.className =
        "order-confirmation__button order-confirmation__button--success";
    }

    confirmationModal.hidden = false;

    requestAnimationFrame(function () {
      confirmationModal.classList.add("is-open");
    });
  }

  //================ Close Confirmation ================//
  function closeConfirmation() {
    var confirmationModal = $("#orderconfirmationModal");

    confirmationModal.classList.remove("is-open");

    setTimeout(function () {
      confirmationModal.hidden = true;
    }, 200);

    pendingAction = null;
    pendingUpdateUrl = null;

    $("#cancelReasonField").hidden = true;
    $("#cancelReason").value = "";
  }

  //================ DOM Ready ================//
  document.addEventListener("DOMContentLoaded", function () {
    //================ Click Events ================//
    document.addEventListener("click", function (event) {
      // View Order
      var view = event.target.closest("[data-view-order]");

      if (view) {
        openOrder(view.dataset.viewOrder);

        return;
      }

      // Close Order
      if (event.target.closest("[data-close-order]")) {
        closeOrder();

        return;
      }

      // Order Action
      var action = event.target.closest("[data-order-action]");

      if (action) {
        openConfirmation(action.dataset.orderAction, action.dataset.updateUrl);

        return;
      }

      // Close Confirmation
      if (event.target.closest("[data-close-confirmation]")) {
        closeConfirmation();

        return;
      }
    });

    //================ Submit Order Action ================//
    $("#orderActionForm").addEventListener("submit", function (event) {
      if (!pendingAction || !pendingUpdateUrl) {
        event.preventDefault();

        return;
      }

      var reason = $("#cancelReason").value;

      if (pendingAction === "cancel" && !reason) {
        event.preventDefault();

        $("#orderconfirmationMessage").textContent =
          "Please select a cancellation reason.";

        return;
      }

      $("#orderAction").value = pendingAction;

      $("#orderCancelReason").value = pendingAction === "cancel" ? reason : "";

      this.action = pendingUpdateUrl;
    });

    //================ Escape Key ================//
    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape") return;

      if ($("#orderconfirmationModal").classList.contains("is-open")) {
        closeConfirmation();
      } else if (activeModal) {
        closeOrder();
      }
    });
  });
})();
