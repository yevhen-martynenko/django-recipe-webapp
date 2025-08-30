document.addEventListener("DOMContentLoaded", () => {
  const tabButtons = document.querySelectorAll<HTMLButtonElement>(".auth__tab");
  const panels = document.querySelectorAll<HTMLElement>(".auth__form-panel");

  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetPanelId = button.getAttribute("aria-controls");
      if (!targetPanelId) return;

      const currentActivePanel = document.querySelector<HTMLElement>(
        ".auth__form-panel:not(.auth__form-panel--hidden)"
      );
      const targetPanel = document.getElementById(targetPanelId);

      if (!targetPanel) return;

      // Deactivate all tabs
      tabButtons.forEach((btn) => {
        btn.classList.remove("auth__tab--active");
        btn.setAttribute("aria-selected", "false");
      });

      // Activate clicked tab
      button.classList.add("auth__tab--active");
      button.setAttribute("aria-selected", "true");

      const completeTransition = () => {
        targetPanel.style.display = "block";
        setTimeout(() => {
          targetPanel.classList.remove("auth__form-panel--hidden");
        }, 20);
      };

      if (currentActivePanel && currentActivePanel !== targetPanel) {
        currentActivePanel.classList.add("auth__form-panel--hidden");
        currentActivePanel.addEventListener(
          "transitionend",
          () => {
            currentActivePanel.style.display = "none";
            completeTransition();
          },
          { once: true }
        );
      } else {
        completeTransition();
      }
    });
  });
});
