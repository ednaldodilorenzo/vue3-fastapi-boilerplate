<template>
  <label class="form-label" v-if="label" :for="$attrs['id']">{{ label }}</label>
  <textarea
    v-bind="$attrs"
    class="form-control"
    :value="result"
    @input="onInput"
    :class="{ 'is-invalid': errors.length }"
  ></textarea>
  <div class="invalid-feedback">
    <div v-for="error in errors" :key="error">
      {{ error }}
    </div>
  </div>
</template>
<script>
export default {
  name: "BootstrapTextArea",
  emits: ["update:modelValue"],
  props: {
    modelValue: {
      type: String,
      default: "",
    },
    errors: {
      type: Array,
      default: () => [],
    },
    label: {
      type: [String, Boolean],
      default: false,
    },
  },
  data() {
    return {
      result: this.modelValue?.[this.displayField],
    };
  },
  methods: {
    onInput(event) {
      this.result = event.target.value;
      this.$emit("update:modelValue", this.result);
    },
  },
  watch: {
    modelValue(val) {
      this.result = val;
    },
  },
};
</script>
