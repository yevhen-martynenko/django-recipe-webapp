declare const __PLATFORM__: "desktop" | "mobile";
declare const __MODE__: "production" | "development";


declare module "*.module.scss" {
  const classNames: { [key: string]: string };
  export default classNames;
}
declare module "*.module.css" {
  const classes: { [key: string]: string };
  export default classes;
}

declare module "*.png";
declare module "*.svg";
declare module "*.jpg";
declare module "*.jpeg";
declare module "*.gif";

