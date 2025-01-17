import { createApp } from "vue";
import { Modal } from "bootstrap/dist/js/bootstrap.esm.min.js";

export function useModalScreen(modal) {
  let modalInstance = null;

  const show = (item = undefined) => {
    return new Promise((resolve) => {
      mountModalScreen(resolve, item);
    });
  };

  const hide = () => {
    unmountModalScreen();
  };

  let appInstance = null,
    app = null;

  const mountModalScreen = (resolve, item) => {
    if (!appInstance) {
      app = createApp(modal, {
        item: item,
        onCancelModal: () => {
          resolve(false);
          modalInstance.hide();
          unmountModalScreen();
        },
        onSaveModal: () => {
          resolve(true);
          modalInstance.hide();
          unmountModalScreen();
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
        unmountModalScreen();
      });
    }
  };

  const unmountModalScreen = () => {
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
