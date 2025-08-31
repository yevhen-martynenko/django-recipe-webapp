import "@styles/main.scss";
import "@styles/pages/password_reset.scss";

class PasswordValidator {
  private password_input = document.getElementById("new_password") as HTMLInputElement;
  private confirm_password_input = document.getElementById("confirm_new_password") as HTMLInputElement;
  private strength_bar = document.querySelector(".password-strength__fill") as HTMLElement;
  private strength_text = document.querySelector(".password-strength__text") as HTMLElement;
  private error_div = document.getElementById("new_password_error") as HTMLElement;
  private success_div = document.getElementById("new_password_success") as HTMLElement;
  private confirm_error_div = document.getElementById("confirm_new_password_error") as HTMLElement;

  constructor() {
    this.password_input?.addEventListener("input", () => this.validate_password());
    this.confirm_password_input?.addEventListener("input", () => this.validate_password_match());
    this.setup_visibility_toggles();
  }

  private validate_password(): void {
    const password = this.password_input.value;
    const validation = this.check_password_strength(password);
    const strength = this.get_strength_level(validation.score, validation.is_strictly_valid);
    this.update_strength_indicator(validation.score, strength);
    this.toggle_messages(validation);
    this.toggle_field_error(this.password_input, validation.is_strictly_valid);
  }

  private validate_password_match(): void {
    const is_match = this.password_input.value === this.confirm_password_input.value;
    const field = this.confirm_password_input.closest(".form__field");

    if (this.confirm_password_input.value && !is_match) {
      this.confirm_error_div.textContent = "Passwords don't match";
      this.confirm_error_div.style.display = "block";
      field?.classList.add("form__field--error");
    } else {
      this.confirm_error_div.style.display = "none";
      field?.classList.remove("form__field--error");
    }
  }

  private check_password_strength(password: string) {
    const errors: string[] = [];
    let score = 0;

    if (password.length >= 8) score++;
    else errors.push("Password must be at least 8 characters long");

    if (/[A-Z]/.test(password)) score++;
    else errors.push("Add at least one uppercase letter");

    if (/[a-z]/.test(password)) score++;
    else errors.push("Add at least one lowercase letter");

    if (/\d/.test(password)) score++;
    else errors.push("Add at least one number");

    const has_special = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    if (has_special) score++;
    const special_char_note = "For very strong, add at least one special character";

    return {
      score,
      strength: this.get_strength_level(score),
      errors: errors.length ? [errors[0]] : !has_special ? [special_char_note] : [],
      is_strictly_valid: errors.length === 0,
    };
  }

  private get_strength_level(score: number, is_valid: boolean): string {
    if (!is_valid) return "weak";
    return ["weak", "fair", "good", "strong", "very-strong"][Math.min(score - 1, 4)];
  }

  private update_strength_indicator(score: number, strength: string): void {
    const strength_levels = ["weak", "fair", "good", "strong", "very-strong"];
    const index = strength_levels.indexOf(strength);

    let percent: number;
    if (strength === "very-strong") {
      percent = 100;
    } else {
      percent = ((index + score) / 2 / strength_levels.length) * 100;
    }
    this.strength_bar.style.width = `${percent}%`;

    let visual_strength: string;
    if (percent < 20) {
      visual_strength = "weak";
    } else if (percent < 40) {
      visual_strength = "fair";
    } else if (percent < 60) {
      visual_strength = "good";
    } else if (percent < 80) {
      visual_strength = "strong";
    } else {
      visual_strength = "very-strong";
    }

    this.strength_bar.className = `password-strength__fill password-strength__fill--${visual_strength}`;
    this.strength_text.className = `password-strength__text password-strength__text--${visual_strength}`;
  }

  private toggle_messages(validation: { errors: string[]; is_strictly_valid: boolean }): void {
    if (validation.errors.length) {
      this.strength_text.style.display = "block";
      this.strength_text.textContent = validation.errors[0];
      this.success_div.style.display = "none";
    } else {
      this.strength_text.style.display = "none";
      this.success_div.textContent = "Password is strong and meets all requirements";
      this.success_div.style.display = "block";
    }
  }

  private toggle_field_error(input: HTMLInputElement, is_valid: boolean): void {
    const field = input.closest(".form__field");
    if (field) field.classList.toggle("form__field--error", !is_valid);
  }

  private setup_visibility_toggles(): void {
    const toggle_buttons = document.querySelectorAll<HTMLButtonElement>(".form__icon");

    toggle_buttons.forEach((button) => {
      const target_input_id = button.dataset.toggle;
      const input = document.getElementById(target_input_id!) as HTMLInputElement;

      button.addEventListener("click", () => {
        const isCurrentlyVisible = input.type === "text";
        const newType = isCurrentlyVisible ? "password" : "text";
        input.type = newType;

        button.setAttribute("aria-expanded", String(!isCurrentlyVisible));

        const icon = button.querySelector("span");
        if (icon) {
          icon.classList.remove("form__icon--eye-open", "form__icon--eye-closed");
          icon.classList.add(newType === "text" ? "form__icon--eye-open" : "form__icon--eye-closed");
        }
      });
    });
  }
}

document.addEventListener("DOMContentLoaded", () => new PasswordValidator());
