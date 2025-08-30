export function setup_tag_input(input_id: string, container_id: string) {
  const input = document.getElementById(input_id) as HTMLInputElement | null;
  const container = document.getElementById(container_id) as HTMLElement | null;

  if (!input || !container) {
    throw new Error("Invalid input or container ID");
  }

  const create_tag_element = (text: string): HTMLElement => {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = text;

    const remove_btn = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    remove_btn.setAttribute("viewBox", "0 0 16 16");
    remove_btn.setAttribute("width", "12");
    remove_btn.setAttribute("height", "12");
    remove_btn.classList.add("tag__remove");
    remove_btn.innerHTML = `
      <path d="M4 4 L12 12 M12 4 L4 12" 
            stroke="black" stroke-width="2" stroke-linecap="round"/>
    `;

    remove_btn.addEventListener("click", () => {
      container.removeChild(tag);
    });

    tag.appendChild(remove_btn);
    return tag;
  };

  input.addEventListener("keydown", (e: KeyboardEvent) => {
    if (e.key === "," || e.key === "Enter") {
      e.preventDefault();
      const value = input.value.trim().replace(/,$/, "");
      if (value !== "") {
        const tag = create_tag_element(value);
        container.insertBefore(tag, input);
        input.value = "";
      }
    }
  });
}
