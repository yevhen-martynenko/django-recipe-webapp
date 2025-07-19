import icon_add from "@icons/icon.add.svg";
import icon_eye from "@icons/eye-open.svg";

export function init_icons() {
  const add_text = document.getElementById("icon_add_text") as HTMLImageElement | null;
  if (add_text) add_text.src = icon_add;

  const add_image = document.getElementById("icon_add_image") as HTMLImageElement | null;
  if (add_image) add_image.src = icon_add;
}

export const text_icon = () => `
  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14,2 14,8 20,8"/>
  </svg>
`;
export const image_icon = () => `
  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
    <circle cx="9" cy="9" r="2"/>
    <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>
  </svg>
`;
