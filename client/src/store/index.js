import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import userModule from "./user/index";

const store = createStore({
  plugins: [createPersistedState()],
  modules: {
    currentUser: userModule,
  },
});

export default store;
