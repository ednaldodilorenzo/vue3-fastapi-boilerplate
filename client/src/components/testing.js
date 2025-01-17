// Create a file for your plugin, e.g., myComponentPlugin.js

import { render, createVNode } from "vue";
import BootstrapToast from "./BootstrapToast.vue"; // Replace this with your component file

const MyComponentPlugin = {
  install(app) {
    const show = () => {
      const toastWrapper = document.createElement("div");

      // Create a new Vue app for the component
      const toastVM = createVNode(BootstrapToast);
      render(toastVM, toastWrapper);
      document.body.appendChild(toastWrapper);
    };

    // Optionally, you can expose the component instance globally
    app.config.globalProperties.$myToast = show;
  },
};

export default MyComponentPlugin;
