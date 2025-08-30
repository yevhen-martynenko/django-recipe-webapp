export function init_image_uploader(
  input_id: string = "main_image",
  content_id: string = "image_upload_content",
  container_id: string = "main_image_container"
): void {
  const file_input = document.getElementById(input_id) as HTMLInputElement;
  const upload_content = document.getElementById(content_id) as HTMLDivElement;
  const container = document.getElementById(container_id) as HTMLDivElement;

  if (!file_input || !upload_content || !container) {
    console.warn("Image uploader: input, content, or container not found");
    return;
  }

  function handle_file(file: File) {
    if (!file.type.startsWith("image/")) return;

    const reader = new FileReader();
    reader.onload = function (e) {
      const result = e.target?.result as string;

      upload_content.innerHTML = `<img src="${result}" alt="Uploaded preview" style="max-width: 100%; max-height: 400px; width: auto; border-radius: 0.5rem;" />`;
    };

    container.classList.remove(`image-upload--empty`);
    reader.readAsDataURL(file);
  }

  file_input.addEventListener("change", (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      handle_file(target.files[0]);
    }
  });

  upload_content.addEventListener("dragover", (e) => {
    e.preventDefault();
    upload_content.classList.add("dragover");
  });

  upload_content.addEventListener("dragleave", () => {
    upload_content.classList.remove("dragover");
  });

  upload_content.addEventListener("drop", (e: DragEvent) => {
    e.preventDefault();
    upload_content.classList.remove("dragover");
    const file = e.dataTransfer?.files?.[0];
    if (file) handle_file(file);
  });

  window.addEventListener("paste", (e: ClipboardEvent) => {
    const items = e.clipboardData?.items;
    if (!items) return;

    for (const item of items) {
      if (item.type.startsWith("image/")) {
        const file = item.getAsFile();
        if (file) {
          handle_file(file);
          break;
        }
      }
    }
  });
}
