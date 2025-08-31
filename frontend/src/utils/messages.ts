type MessageType = "success" | "error" | "warning" | "info";

interface StoredMessage {
  message: string;
  type: MessageType;
  timestamp: number;
}

function get_container(container_id: string): HTMLElement {
  let container = document.getElementById(container_id);
  if (!container) {
    container = document.createElement("div");
    container.id = container_id;
    container.className = "messages";
    document.body.appendChild(container);
  }
  return container;
}

export function show_message(
  text: string,
  type: MessageType = "info",
  duration: number = 5000,
  container_id: string = "messages",
  animation_duration: number = 300
): void {
  const container = get_container(container_id);

  const message = document.createElement("div");
  message.className = `messages__item messages__item--${type}`;
  message.innerHTML = `<div class="messages__text">${text}</div>`;

  const close_btn = document.createElement("button");
  close_btn.className = "messages__close";
  close_btn.innerHTML = "&times;";
  close_btn.addEventListener("click", () => hide_message(message, animation_duration));
  message.appendChild(close_btn);

  container.appendChild(message);

  requestAnimationFrame(() => {
    message.classList.add("messages__item--show");
  });

  if (duration > 0) {
    setTimeout(() => hide_message(message, animation_duration), duration);
  }
}

export function hide_message(message: HTMLElement, animation_duration: number = 300): void {
  message.classList.remove("messages__item--show");
  setTimeout(() => message.remove(), animation_duration);
}

export function store_message(message: string, type: MessageType, container_id: string = "messages"): void {
  const existing: StoredMessage[] = JSON.parse(localStorage.getItem("messages") || "[]");
  existing.push({ message, type, timestamp: Date.now() });
  localStorage.setItem("messages", JSON.stringify(existing));
}

function get_stored_messages(): StoredMessage[] {
  const messages: StoredMessage[] = JSON.parse(localStorage.getItem("messages") || "[]");
  localStorage.removeItem("messages");
  return messages;
}

export function show_stored_messages(container_id: string = "messages", animation_duration: number = 300): void {
  get_stored_messages().forEach((msg) => show_message(msg.message, msg.type, 4000, container_id, animation_duration));
}
