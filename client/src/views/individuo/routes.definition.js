const namespace = "individuo";

const ROUTE_NAMES = {
  INDEX: namespace,
  ADD: `${namespace}-add`,
  EDIT: `${namespace}-edit`,
};

const ROUTES_DEFINITIONS = [
  {
    path: "/individuos",
    name: ROUTE_NAMES.INDEX,
    component: () => import("./indiviuo-lista.vue"),
    meta: {
      label: "Indivíduos",
      icon: "bx bxs-contact",
      requiresAuth: true,
    },
  },
  {
    path: "/individuos/novo",
    name: ROUTE_NAMES.ADD,
    component: () => import("./individuo-change.vue"),
    meta: {
      label: "Indivíduos",
      requiresAuth: true,
    },
  },
  {
    path: "/individuos/:id",
    name: ROUTE_NAMES.EDIT,
    component: () => import("./individuo-change.vue"),
    meta: {
      label: "Indivíduos",
      requiresAuth: true,
    },
  },
];

export { ROUTE_NAMES, ROUTES_DEFINITIONS };
