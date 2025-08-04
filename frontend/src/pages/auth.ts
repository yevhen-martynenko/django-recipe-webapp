import "@styles/main.scss";
import "@styles/pages/auth.scss";
import "@utils/auth_tabs.ts";
import { show_message, store_message } from "@utils/messages.ts";
import { API_BASE_URL, API_ENDPOINTS } from "@/api.ts";

// ----------------------------------------------
// SIGNUP
// ----------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
  const signup_form = document.getElementById("signup-form") as HTMLFormElement | null;
  const signup_button = document.getElementById("signup-button") as HTMLButtonElement | null;

  if (!signup_form || !signup_button) return;

  signup_form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const user_email = (document.getElementById("signup-email") as HTMLInputElement).value;
    const user_name = (document.getElementById("signup-username") as HTMLInputElement).value;
    const user_password = (document.getElementById("signup-password") as HTMLInputElement).value;
    const remember_me = (document.querySelector('input[name="remember"]') as HTMLInputElement)?.checked || false;
    const csrf_token = (document.querySelector("[name=csrfmiddlewaretoken]") as HTMLInputElement)?.value || "";

    signup_button.disabled = true;
    signup_button.textContent = "Creating Account...";

    try {
      const response = await fetch(API_ENDPOINTS.auth.register, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify({
          email: user_email,
          username: user_name,
          password: user_password,
          remember: remember_me,
        }),
      });

      const response_data = await response.json();

      if (response.ok) {
        if (response_data.token) {
          localStorage.setItem("authToken", response_data.token);
        }

        store_message("Account created successfully!", "success");
        signup_form.reset();

        setTimeout(() => {
          window.location.href = API_BASE_URL;
        }, 100);
      } else {
        handle_registration_error(response_data);
      }
    } catch (error) {
      show_message("Unable to create account. Please check your connection and try again.", "error");
    } finally {
      signup_button.disabled = false;
      signup_button.textContent = "Create Account";
    }
  });
});

function handle_registration_error(response_data: any) {
  let error_message = "Registration failed. Please try again.";

  if (response_data.email && Array.isArray(response_data.email)) {
    error_message = response_data.email[0];
  } else if (response_data.username && Array.isArray(response_data.username)) {
    error_message = response_data.username[0];
  } else if (response_data.password && Array.isArray(response_data.password)) {
    error_message = response_data.password[0];
  } else if (response_data.detail) {
    error_message = response_data.detail;
  } else if (response_data.non_field_errors && Array.isArray(response_data.non_field_errors)) {
    error_message = response_data.non_field_errors[0];
  }

  show_message(error_message, "error");
}

// ----------------------------------------------
// LOGIN
// ----------------------------------------------
document.addEventListener("DOMContentLoaded", function () {
  const login_form = document.getElementById("login-form") as HTMLFormElement | null;
  const login_button = document.querySelector("#login-form button[type='submit']") as HTMLButtonElement | null;

  if (!login_form || !login_button) return;

  login_form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const user_email = (document.getElementById("login-email") as HTMLInputElement).value;
    const user_password = (document.getElementById("login-password") as HTMLInputElement).value;
    const csrf_token = (document.querySelector("[name=csrfmiddlewaretoken]") as HTMLInputElement)?.value || "";

    login_button.disabled = true;
    login_button.textContent = "Signing in...";

    try {
      const response = await fetch(API_ENDPOINTS.auth.login, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify({
          email_or_username: user_email,
          password: user_password,
        }),
      });

      const response_data = await response.json();

      if (response.ok) {
        if (response_data.token) {
          localStorage.setItem("authToken", response_data.token);
        }

        store_message("Welcome back! You've been successfully logged in.", "success");

        setTimeout(() => {
          window.location.href = API_BASE_URL;
        }, 100);
      } else {
        handle_login_error(response_data);
      }
    } catch (error) {
      show_message("Unable to sign in. Please check your connection and try again.", "error");
    } finally {
      login_button.disabled = false;
      login_button.textContent = "Sign In";
    }
  });
});

function handle_login_error(response_data: any) {
  let error_message = "Login failed. Please check your credentials.";

  if (response_data.non_field_errors && Array.isArray(response_data.non_field_errors)) {
    error_message = response_data.non_field_errors[0];
  } else if (response_data.detail) {
    error_message = response_data.detail;
  } else if (response_data.email_or_username && Array.isArray(response_data.email_or_username)) {
    error_message = response_data.email_or_username[0];
  } else if (response_data.password && Array.isArray(response_data.password)) {
    error_message = response_data.password[0];
  }

  show_message(error_message, "error");
}
