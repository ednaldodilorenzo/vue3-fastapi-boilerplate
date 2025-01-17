import { createApp } from "vue";
import DialogScreen from "./dialog-screen.vue";
import { Modal } from "bootstrap/dist/js/bootstrap.esm.min.js";

export function useDialogScreen(message, title) {
  let modalInstance = null;

  const show = () => {
    return new Promise((resolve) => {
      mountDialogScreen(resolve);
    });
  };

  const hide = () => {
    unmountDialogScreen();
  };

  let appInstance = null,
    app = null;

  const mountDialogScreen = (resolve) => {
    if (!appInstance) {
      app = createApp(DialogScreen, {
        message: message,
        title: title,
        onCancel: () => {
          resolve(false);
          modalInstance.hide();
          unmountDialogScreen();
        },
        onConfirm: () => {
          resolve(true);
          modalInstance.hide();
          unmountDialogScreen();
        },
      });
      const container = document.createElement("div");
      document.body.appendChild(container);
      appInstance = app.mount(container);
      modalInstance = new Modal(appInstance.$el);
      modalInstance.show();
      // Listen for the Bootstrap `hide.bs.modal` event
      appInstance.$el.addEventListener("hide.bs.modal", () => {
        resolve(false); // Treat keyboard-triggered hide (e.g., Escape key) as cancel
        unmountDialogScreen();
      });
    }
  };

  const unmountDialogScreen = () => {
    if (appInstance) {
      const parentNode = appInstance.$el.parentElement;
      if (parentNode) {
        parentNode.remove();
      }
      app.unmount();
      app = null;
      appInstance = null;
    }
  };

  return {
    show,
    hide,
  };
}
