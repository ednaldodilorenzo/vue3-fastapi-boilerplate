export default {
  namespaced: true,
  state() {
    return {
      user: null,
    };
  },
  actions: {
    setUser({ commit }, payload) {
      commit("setUser", payload);
    },
  },
  mutations: {
    setUser(state, payload) {
      state.user = payload;
    },
  },
  getters: {
    hasRole(_, getters, role) {
      const user = getters.user;

      if (user?.roles.length > 0) {
        return user.roles.includes(role);
      } else {
        return false;
      }
    },
    getUser: (state) => state.user,
    getUserToken: (state) => state.user?.token,
    isAuthenticated: (state) => (state.user?.token ? true : false),
    userRoles: (state) => state.user?.roles,
    hasRoles: (state) => (roles) => {
      const user = state?.user;

      const userRoles = user?.roles;
      return userRoles
        ? roles?.some((role) => userRoles.includes(role))
        : false;
    },
  },
};
