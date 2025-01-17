import { reactive, createApp } from "vue";
import LoadingScreen from "./loading-screen.vue";

export function useLoadingScreen() {
  const state = reactive({
    isLoading: false,
  });

  const show = () => {
    state.isLoading = true;
    mountLoadingScreen();
  };

  const hide = () => {
    state.isLoading = false;
    unmountLoadingScreen();
  };

  let appInstance = null;

  const mountLoadingScreen = () => {
    if (!appInstance) {
      const app = createApp(LoadingScreen, { loading: state.isLoading });
      const container = document.createElement("div");
      document.body.appendChild(container);
      appInstance = app.mount(container);
    }
  };

  const unmountLoadingScreen = () => {
    if (appInstance) {
      appInstance.$el.remove();
      appInstance = null;
    }
  };

  return {
    show,
    hide,
  };
}
