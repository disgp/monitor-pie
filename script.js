document.addEventListener("DOMContentLoaded", () => {
  // Dashboard elements
  const cpuLoadElement = document.getElementById("cpu-load");
  const cpuFillElement = document.getElementById("cpu-fill");
  const ramLoadElement = document.getElementById("ram-load");
  const ramFillElement = document.getElementById("ram-fill");
  const dashboard = document.getElementById("dashboard");

  // Message elements
  const notConfiguredMessage = document.getElementById(
    "not-configured-message",
  );
  const disconnectedMessage = document.getElementById("disconnected-message");
  const offlineMessage = document.getElementById("offline-message");

  // Settings panel elements
  const settingsIcon = document.getElementById("settings-icon");
  const settingsPanel = document.getElementById("settings-panel");
  const ipInput = document.getElementById("ip-input");
  const saveIpButton = document.getElementById("save-ip-button");

  // --- State Management ---
  let macbookIp = localStorage.getItem("macbookIp") || null;

  // --- Functions ---
  function showMessage(messageElement) {
    dashboard.style.display = "none";
    [notConfiguredMessage, disconnectedMessage, offlineMessage].forEach(
      (msg) => {
        msg.style.display = msg === messageElement ? "block" : "none";
      },
    );
  }

  function showDashboard() {
    dashboard.style.display = "flex";
    [notConfiguredMessage, disconnectedMessage, offlineMessage].forEach(
      (msg) => {
        msg.style.display = "none";
      },
    );
  }

  async function updateSystemInfo() {
    if (!macbookIp) {
      showMessage(notConfiguredMessage);
      return;
    }

    const statsUrl = `http://${macbookIp}:8000/stats`;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2000);

    try {
      const response = await fetch(statsUrl, { signal: controller.signal });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const stats = await response.json();

      showDashboard();

      const cpuLoad = Math.round(stats.cpu_load);
      const ramLoad = Math.round(stats.ram_load);

      cpuLoadElement.textContent = `${cpuLoad}%`;
      ramLoadElement.textContent = `${ramLoad}%`;
      cpuFillElement.style.transform = `translateY(${100 - cpuLoad}%)`;
      ramFillElement.style.transform = `translateY(${100 - ramLoad}%)`;
    } catch (error) {
      if (error.name === "AbortError") {
        showMessage(offlineMessage); // Request timed out, host is likely offline
      } else {
        showMessage(disconnectedMessage); // Other network error, script likely not running
      }
    } finally {
      clearTimeout(timeoutId);
    }
  }

  // --- Event Listeners ---
  settingsIcon.addEventListener("click", () => {
    settingsPanel.style.display =
      settingsPanel.style.display === "none" ? "block" : "none";
  });

  saveIpButton.addEventListener("click", () => {
    const newIp = ipInput.value.trim();
    if (newIp) {
      macbookIp = newIp;
      localStorage.setItem("macbookIp", newIp);
      settingsPanel.style.display = "none";
      updateSystemInfo(); // Immediately try the new IP
    }
  });

  // --- Initial Load ---
  if (macbookIp) {
    ipInput.value = macbookIp; // Pre-fill the input field
  }

  setInterval(updateSystemInfo, 2000);
  updateSystemInfo(); // Initial update
});
