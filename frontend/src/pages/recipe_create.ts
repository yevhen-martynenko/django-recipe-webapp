import "@styles/main.scss";
import "@styles/pages/recipe_create.scss";
import { API_BASE_URL, API_ENDPOINTS } from "@/api.ts";
import { text_icon, image_icon } from "@utils/recipe_icon_handling.ts";
import { setup_tag_input } from "@utils/tag_input.ts";
import { init_image_uploader } from "@utils/image_uploader.ts";
import { init_icons, inject_recipe_svgs } from "@utils/recipe_icon_handling.ts";

init_icons();
inject_recipe_svgs();
setup_tag_input("recipe_tags", "tag_container");
init_image_uploader();

// ==================================================
// Ingredients
// ==================================================
let ingredient_count = 1;
const ingredients_list = document.getElementById("ingredients_list") as HTMLElement;
const add_ingredient_btn = document.getElementById("add_ingredient") as HTMLButtonElement;

const create_ingredient_html = (index: number): string => `
  <tr class="ingredient-row">
    <td>
      <input 
        type="number" 
        id="ingredient_quantity_${index}"
        name="ingredient_quantities[]" 
        placeholder="2" 
        min="0" 
        max="9999" 
        step="0.1" 
        required
        aria-label="Quantity for ingredient ${index}"
      />
    </td>
    <td>
      <select 
        id="ingredient_unit_${index}" 
        name="ingredient_units[]" 
        required 
        aria-label="Unit for ingredient ${index}">
        <option value="">Unit</option>
        <option value="cups">cups</option>
        <option value="tsp">tsp</option>
        <option value="tbsp">tbsp</option>
        <option value="oz">oz</option>
        <option value="lbs">lbs</option>
        <option value="g">g</option>
        <option value="kg">kg</option>
        <option value="ml">ml</option>
        <option value="l">l</option>
        <option value="piece">piece</option>
        <option value="clove">clove</option>
        <option value="pinch">pinch</option>
        <option value="dash">dash</option>
        <option value="can">can</option>
        <option value="package">package</option>
      </select>
    </td>
    <td>
      <input 
        type="text" 
        id="ingredient_name_${index}"
        name="ingredient_names[]" 
        placeholder="flour" 
        maxlength="100" 
        required
        aria-label="Name for ingredient ${index}"
      />
    </td>
    <td>
      <button 
        type="button" 
        class="ingredient-item__remove" 
        aria-label="Remove ingredient ${index}" 
        title="Remove this ingredient">
        ❌
      </button>
    </td>
  </tr>
`;

const add_ingredient = () => {
  ingredient_count++;
  const ingredient_html = create_ingredient_html(ingredient_count);
  const wrapper = document.createElement("tbody");
  wrapper.innerHTML = ingredient_html.trim();
  const new_row = wrapper.firstElementChild as HTMLTableRowElement;
  const remove_btn = new_row.querySelector(".ingredient-item__remove") as HTMLButtonElement;
  remove_btn.addEventListener("click", () => new_row.remove());
  const tbody = ingredients_list.querySelector("tbody")!;
  tbody.appendChild(new_row);
};

document.querySelectorAll<HTMLButtonElement>(".ingredient-item__remove").forEach((button) => {
  button.addEventListener("click", (e) => {
    const item = (e.currentTarget as HTMLElement).closest(".ingredient-item");
    item?.remove();
  });
});

add_ingredient_btn.addEventListener("click", add_ingredient);

// ==================================================
// Blocks
// ==================================================
const blocks_container = document.getElementById("blocks_container")!;
const add_text_btn = document.getElementById("add_text_button")!;
const add_image_btn = document.getElementById("add_image_button")!;

let block_counter = 0;

function get_next_block_id() {
  return block_counter++;
}

const block_actions = (id: number) => `
  <div class="block-actions" id="block_actions_${id}">
    ${["up", "down", "delete"]
      .map((type) => {
        const paths = {
          up: `<path d="M18 15l-6-6-6 6"/>`,
          down: `<path d="M6 9l6 6 6-6"/>`,
          delete: `<path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>`,
        };
        const title = {
          up: "Move up",
          down: "Move down",
          delete: "Delete",
        };
        return `
        <button 
          type="button" 
          class="block-action block-action--${type}${type === "delete" ? " block-action--delete" : ""}"
          data-action="${type}" 
          data-id="${id}" 
          title="${title[type]}" 
          aria-label="${title[type]} block ${id}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
            ${paths[type]}
          </svg>
        </button>`;
      })
      .join("")}
  </div>
`;

function image_upload_html(id: number) {
  return `
  <div class="image-upload image-upload--empty" id="image_container_${id}" tabindex="0" role="button">
    <input
      type="file"
      id="image_${id}"
      name="image_${id}"
      accept="image/jpeg,image/png,image/gif,image/webp"
      class="image-upload__input"
    />
    <div class="image-upload__content" id="image_content_${id}">
      <div class="image-upload__icon" aria-hidden="true">
        <svg width="48" height="48" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
      </div>
      <div class="image-upload__text">
        <span class="image-upload__text--primary">Drop your image here or click to browse</span>
        <span class="image-upload__text--secondary">JPG, PNG, GIF, or WebP up to 10MB</span>
      </div>
    </div>
  </div>
`;
}

const create_text_block_html = (id: number) => `
  <div class="content-block" id="content_block_${id}" data-block-type="text">
    <div class="content-block__header">
      <div class="content-block__title">
        ${text_icon()}
        <h3>Text Block</h3>
      </div>
      ${block_actions(id)}
    </div>
    <div class="content-block__content">
      <textarea id="text_block_${id}" name="text_blocks[]" class="form__field form__textarea"
        placeholder="Write your text here..."
        aria-describedby="text_block_${id}_help"
      ></textarea>
    </div>
  </div>
`;

const create_image_block_html = (id: number) => `
  <div class="content-block" id="content_block_${id}" data-block-type="image">
    <div class="content-block__header">
      <div class="content-block__title">
        ${image_icon()}
        <h3>Image Block</h3>
      </div>
      ${block_actions(id)}
    </div>
    <div class="content-block__content">
      <div class="form form--spaced">
        ${image_upload_html(id)}
      </div>
      <label for="image_caption_${id}" class="form__label">Image caption</label>
      <input type="text" id="image_caption_${id}" name="image_captions[]" class="form__field"
             placeholder="Add a caption for your image..." maxlength="200">
    </div>
  </div>
`;

function create_element_from_html(html: string): HTMLElement {
  const template = document.createElement("template");
  template.innerHTML = html.trim();
  return template.content.firstElementChild as HTMLElement;
}

add_text_btn.addEventListener("click", () => {
  const id = get_next_block_id();
  const block = create_element_from_html(create_text_block_html(id));
  blocks_container.appendChild(block);
});

add_image_btn.addEventListener("click", () => {
  const id = get_next_block_id();
  const block = create_element_from_html(create_image_block_html(id));
  blocks_container.appendChild(block);
  init_image_uploader(`image_${id}`, `image_content_${id}`, `image_container_${id}`);
});

blocks_container.addEventListener("click", (e) => {
  const target = (e.target as HTMLElement).closest(".block-action");
  if (!target) return;

  const action = target.getAttribute("data-action");
  const id = target.getAttribute("data-id");
  const content = document.getElementById(`content_block_${id}`);
  const block = content;

  if (!block) return;

  if (action === "delete") {
    block.remove();
  } else if (action === "up") {
    const prev = block.previousElementSibling;
    if (prev) {
      blocks_container.insertBefore(block, prev);
    }
  } else if (action === "down") {
    const next = block.nextElementSibling;
    if (next) {
      blocks_container.insertBefore(block, next.nextSibling);
    }
  }
});
