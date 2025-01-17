import { createApp } from "vue";
import App from "./App.vue";
import router from "@/router/index";
import store from "./store";
import "./assets/styles.css";
import Toast from "vue-toastification";
import "bootstrap/dist/css/bootstrap.css";
import "vue-toastification/dist/index.css";

import authPermission from "./components/auth.directive";
import VOnClickOutside from "./components/clickoutside.directive";
import autofocus from "./components/focus.directive";
import tooltip from "./components/tooltip.directive";

const app = createApp(App);

app.use(store);
app.use(router);
app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 20,
  newestOnTop: true,
});

app.directive("permission", authPermission);
app.directive("clickOutside", VOnClickOutside);
app.directive("autofocus", autofocus);
app.directive("tooltip", tooltip);

app.mount("#app");

window.__store__ = store;

import "bootstrap/dist/js/bootstrap.bundle.js";
