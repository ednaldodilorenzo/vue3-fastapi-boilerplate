export default {
  mounted(el, binding) {
    if (binding.value) {
      el.focus();
    }
  },
};
