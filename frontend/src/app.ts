import "@styles/main.scss";
import { API_BASE_URL, API_ENDPOINTS } from "@/api.ts";

// LOGOUT :
document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("authToken");
  if (!token) return;

  try {
    const response = await fetch(API_ENDPOINTS.users.me, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) return;

    const data = await response.json();
    const username = data.username;

    const userInfo = document.getElementById("user-info");
    const usernameEl = document.getElementById("username");
    const logoutBtn = document.getElementById("logout-btn");

    if (userInfo && usernameEl && logoutBtn) {
      usernameEl.textContent = username;
      userInfo.style.display = "inline-block";

      logoutBtn.addEventListener("click", async () => {
        try {
          const logoutResp = await fetch(API_ENDPOINTS.auth.logout, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          if (logoutResp.ok) {
            localStorage.removeItem("authToken");
            window.location.href = "/auth/"; // redirect to login
          } else {
            alert("Failed to log out.");
          }
        } catch (err) {
          console.error("Logout error:", err);
          alert("Network error during logout.");
        }
      });
    }
  } catch (err) {
    console.error("Failed to load user info", err);
  }
});
