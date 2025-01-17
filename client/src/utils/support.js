import { onMounted, onBeforeUnmount } from "vue";

export function debounce(fn, wait) {
  let timer;
  return function (...args) {
    if (timer) {
      clearTimeout(timer); // clear any pre-existing timer
    }
    const context = this; // get the current context
    timer = setTimeout(() => {
      fn.apply(context, args); // call the function if time expires
    }, wait);
  };
}

export default function useClickOutside(component, callback, excludeComponent) {
  // fail early if any of the required params is missing
  console.log(component);
  if (!component) {
    throw new Error("A target component has to be provided.");
  }

  if (!callback) {
    throw new Error("A callback has to be provided.");
  }

  const listener = (event) => {
    if (
      event.target === component.value ||
      event.composedPath().includes(component.value) ||
      event.target === excludeComponent.value ||
      event.composedPath().includes(excludeComponent.value)
    ) {
      return;
    }
    if (typeof callback === "function") {
      callback();
    }
  };

  onMounted(() => {
    window.addEventListener("click", listener);
  });

  onBeforeUnmount(() => {
    window.removeEventListener("click", listener);
  });
}
