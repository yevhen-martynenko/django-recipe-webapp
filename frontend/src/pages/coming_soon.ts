import "@styles/main.scss";
import "@styles/pages/coming_soon.scss";


function set_random_background_image() {
  const images_context = require.context('@images', false, /coming-soon\.\d+\.jpg$/);
  const images: string[] = images_context.keys().map(images_context);
  if (images.length === 0) return;

  const random_image = images[Math.floor(Math.random() * images.length)];
  const container = document.querySelector('.coming-soon') as HTMLElement | null;

  if (container) {
    Object.assign(container.style, {
      backgroundImage: `url('${random_image}')`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    });
  }
}

function set_social_media_icons() {
  const social_links = document.querySelectorAll('.coming-soon__social-link');
  if (social_links.length === 0) return;

  const icons_context = require.context('@images/icons', false, /social_media\.[a-zA-Z]+\.svg$/);
  const icon_keys = icons_context.keys();

  social_links.forEach((link) => {
    const platform = link.getAttribute('aria-label')?.toLowerCase();
    if (!platform) return;

    const match_key = icon_keys.find(key => key.includes(`social_media.${platform}.svg`));
    if (!match_key) {
      console.warn(`No icon found for platform: ${platform}`);
      return;
    }

    const icon_path = icons_context(match_key);

    fetch(icon_path)
      .then(res => res.text())
      .then(svg_text => {
        const parser = new DOMParser();
        const svg_doc = parser.parseFromString(svg_text, 'image/svg+xml');
        const svg = svg_doc.querySelector('svg');

        if (svg) {
          svg.classList.add('coming-soon__social-icon');
          link.appendChild(svg);
        }
      })
      .catch(err => {
        console.warn(`Failed to load icon for: ${platform}`, err);
      });
  });
}

function start_countdown() {
  const countdown = document.getElementById('countdown');
  const future_time_str = countdown?.getAttribute('data-future-time');
  if (!future_time_str) return;

  const future_time = new Date(future_time_str).getTime();
  const elements = ['days', 'hours', 'minutes', 'seconds'].map(id => document.getElementById(id));

  const update_countdown = () => {
    const now = Date.now();
    const diff = future_time - now;

    if (elements.some(el => !el)) return;

    if (diff <= 0) {
      elements.forEach(el => el!.textContent = '0');
      clearInterval(interval);
      return;
    }

    const seconds = Math.floor((diff / 1000) % 60);
    const minutes = Math.floor((diff / 1000 / 60) % 60);
    const hours = Math.floor((diff / 1000 / 60 / 60) % 24);
    const days = Math.floor(diff / 1000 / 60 / 60 / 24);

    [days, hours, minutes, seconds].forEach((val, i) => elements[i]!.textContent = val.toString());
  };

  update_countdown();
  const interval = setInterval(update_countdown, 1000);
}


document.addEventListener('DOMContentLoaded', () => {
  set_random_background_image();
  set_social_media_icons();
  start_countdown();
});
