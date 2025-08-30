export const API_BASE_URL = "http://0.0.0.0:8000";

const API_AUTH = `${API_BASE_URL}/api/auth`;
const API_USERS = `${API_BASE_URL}/api/users`;
const API_RECIPES = `${API_BASE_URL}/api/recipes`;

export const API_ENDPOINTS = {
  auth: {
    register: `${API_AUTH}/register/`,
    login: `${API_AUTH}/login/`,
    logout: `${API_AUTH}/logout/`,
    activate: `${API_AUTH}/activate/`,
    google: `${API_AUTH}/google/`,
    google_callback: `${API_AUTH}/google/callback/`,
  },
  users: {
    list: `${API_USERS}/`,
    me: `${API_USERS}/me/`,
    update_me: `${API_USERS}/me/`, // same as me
    delete_me: `${API_USERS}/me/delete/`,
    public_detail: (username: string) => `${API_USERS}/view/${username}/`,
  },
  recipes: {
    list: `${API_RECIPES}/`,
    admin_list: `${API_RECIPES}/list/`,
    create: `${API_RECIPES}/create/`,
    random: `${API_RECIPES}/random/`,
    deleted: `${API_RECIPES}/deleted/`,
    detail: (slug: string) => `${API_RECIPES}/view/${slug}/`,
    update: (slug: string) => `${API_RECIPES}/view/${slug}/update/`,
    delete: (slug: string) => `${API_RECIPES}/view/${slug}/delete/`,
    restore: (slug: string) => `${API_RECIPES}/view/${slug}/restore/`,
    export: (slug: string) => `${API_RECIPES}/view/${slug}/export/`,
    report: (slug: string) => `${API_RECIPES}/view/${slug}/report/`,
    ban: (slug: string) => `${API_RECIPES}/view/${slug}/ban/`,
    like: (slug: string) => `${API_RECIPES}/view/${slug}/like/`,
    statistics: (slug: string) => `${API_RECIPES}/view/${slug}/statistics/`,
  },
};
