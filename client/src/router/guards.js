import { ROUTE_NAMES as LOGIN_ROUTE_NAMES } from "@/views/auth/routes.definition";
import store from "@/store/index";
import jsCookie from "js-cookie";

const checkAuth = (to, from, next) => {
  const requiresAuth = to?.meta?.requiresAuth;

  if (requiresAuth && !jsCookie.get("jwtToken")) {
    next({ name: LOGIN_ROUTE_NAMES.LOGIN });
  } else if (!requiresAuth && jsCookie.get("jwtToken")) {
    next("/");
  } else {
    const routeRoles = to?.meta?.roleList;

    if (routeRoles) {
      const user = store.getters["currentUser/getUser"];
      const userRole = user.role;

      if (routeRoles.includes(userRole)) {
        next();
      } else {
        next({ name: "denied" });
      }
    } else {
      next();
    }
  }
};

export { checkAuth };
