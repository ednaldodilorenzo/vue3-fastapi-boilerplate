<template>
  <div v-if="loading" class="backdrop">
    <div class="spinner-border" role="status"></div>
  </div>
</template>
<script>
export default {
  props: {
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
};
</script>
<style scoped>
.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 999;
  background: rgb(0, 0, 0, 0.2);
}

.backdrop .spinner-border {
  display: block;
  position: fixed;
  top: 50%;
  right: 50%;
}
</style>
