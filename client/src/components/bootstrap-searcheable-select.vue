<template>
  <div class="container">
    <label
      for="searchable-select"
      class="form-label"
      v-if="label"
      :for="$attrs['id']"
      >{{ label }}</label
    >
    <div class="position-relative">
      <input
        title="Buscar"
        v-bind="$attrs"
        type="search"
        v-model="searchQuery"
        id="searchable-select"
        class="form-control"
        @change="onSelectChange"
        @input="filterOptions"
        @blur="validateSelection"
        @keydown.down="navigateOptions(1)"
        @keydown.up="navigateOptions(-1)"
        @keydown.enter="selectHighlightedOption"
      />
      <ul
        v-if="filteredOptions.length > 0"
        ref="dropdown"
        class="dropdown-menu show position-absolute w-100"
        @click="onDropdownClick"
      >
        <li
          v-for="(option, index) in filteredOptions"
          :key="index"
          :class="['dropdown-item', { active: highlightedIndex === index }]"
          @click="selectOption(option)"
          @mouseover="highlightOption(index)"
        >
          {{ option[displayField] }}
        </li>
      </ul>
    </div>
    <!-- <div v-if="!isValid" class="text-danger mt-2">
      Please select a valid option from the list.
    </div> -->
  </div>
</template>

<script setup>
import { ref, defineEmits, watch, nextTick } from "vue";
import { debounce } from "@/utils/support";

const searchQuery = ref("");
const selectedValue = ref(null);
const isValid = ref(true);
const highlightedIndex = ref(-1);
const dropdown = ref(null);

const props = defineProps({
  displayField: {
    type: String,
    required: false,
    default: () => "",
  },
  label: {
    type: String,
    required: false,
    default: () => "",
  },
  options: {
    type: [Array, Function],
    default: () => [],
  },
  test: {
    type: Number,
    required: false,
  },
});

const emit = defineEmits(["change"]);

const modelValue = defineModel("modelValue");

const fetchOptions = (filter) => {
  if (typeof props.options === "function") {
    return props.options(filter).then((result) => result);
  } else {
    return new Promise((resolve, reject) => {
      const result = props.options.filter((option) => {
        return option[props.displayField]
          ?.toLowerCase()
          .includes(searchQuery.value.toLowerCase());
      });

      resolve(result);
    });
  }
};

const loadItems = (value) => {
  fetchOptions(value).then((resp) => {
    filteredOptions.value = resp;
  });
};

// Debounced function for calling `props.items`
const fetchOptionsDebounced = debounce(loadItems, 1000); // Debounce for 1s

watch(
  () => modelValue.value,
  (value) => {
    if (value) {
      selectOption(value);
    } else {
      selectedValue.value = null;
      searchQuery.value = "";
    }
  },
  { immediate: true }
);

const onSelectChange = (e) => {
  emit("change", e);
};

const filteredOptions = ref([]);

const filterOptions = (event) => {
  // Trigger computation of filteredOptions
  if (!event.target.value) {
    highlightedIndex.value = -1;
    modelValue.value = undefined;
    filteredOptions.value = [];
  } else {
    fetchOptionsDebounced(event.target.value, 1000);
  }
};

const selectOption = async (option) => {
  searchQuery.value = option[props.displayField];
  selectedValue.value = option[props.valueField];
  // defer unting the screen is mounted.
  await nextTick();
  if (dropdown.value) {
    dropdown.value.style.display = "none";
  }
  isValid.value = true;
  modelValue.value = option;
};

const validateSelection = () => {
  //if (!props.options.includes(searchQuery.value)) {
  //  isValid.value = false;
  //  selectedValue.value = null;
  //} else {
  //  isValid.value = true;
  //}
  hideOptions();
};

const navigateOptions = (direction) => {
  if (filteredOptions.value.length === 0) return;
  highlightedIndex.value =
    (highlightedIndex.value + direction + filteredOptions.value.length) %
    filteredOptions.value.length;
};

const selectHighlightedOption = () => {
  if (highlightedIndex.value !== -1) {
    const option = filteredOptions.value[highlightedIndex.value];
    selectOption(option);
  }
};

const highlightOption = (index) => {
  highlightedIndex.value = index;
};

const hideOptions = () => {
  highlightedIndex.value = -1;
};

const onDropdownClick = () => {
  if (dropdown.value) {
    dropdown.value.style.display = "none";
  }
};
</script>

<style>
.dropdown-menu {
  max-height: 200px;
  overflow-y: auto;
}

.dropdown-item.active {
  background-color: #007bff;
  color: white;
}
</style>
