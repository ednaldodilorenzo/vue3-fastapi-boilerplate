import { Tooltip } from "bootstrap/dist/js/bootstrap.bundle.js";
// Use "mounted" hook
export default {
  mounted(el, binding) {
    const tooltip = new Tooltip(el, {
      placement: binding.arg || "top",
      title: binding.value,
      trigger: "hover",
    });

    // Hacking to make tooltip hide after clicking.
    el.addEventListener("click", () => {
      tooltip.hide();
    });
  },
};
