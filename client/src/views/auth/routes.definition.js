const namespace = "auth";

const ROUTE_NAMES = {
  INDEX: `${namespace}`,
  LOGIN: `${namespace}-login`,
  SIGNUP: `${namespace}-signup`,
};

const ROUTES_DEFINITIONS = [
  {
    path: "/auth",
    name: ROUTE_NAMES.INDEX,
    component: () => import("./auth-base.vue"),
    children: [
      {
        path: "/login",
        name: ROUTE_NAMES.LOGIN,
        component: () => import("./login-page.vue"),
      },
      {
        path: "/signup/:token",
        name: ROUTE_NAMES.SIGNUP,
        component: () => import("./sign-up.vue"),
      },
    ],
  },
];

export { ROUTE_NAMES, ROUTES_DEFINITIONS };
