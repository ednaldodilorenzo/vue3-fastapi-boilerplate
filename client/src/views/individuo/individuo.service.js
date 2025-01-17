import requester from "@/utils/request";

const PREFIX = "/v1/individuo";

const individuoService = {
  findByToken: async (token) => {
    const resp = await requester.get(`${PREFIX}/token/${token}`, {});
    return resp.data;
  },
  findLoggedData: async () => {
    const resp = await requester.get(`${PREFIX}/logged/dados`);
    return resp.data;
  },
  update: async (id, individuo) => {
    const resp = await requester.patch(`${PREFIX}/${id}`, individuo);
    return resp.data;
  },
  create: async (individuo) => {
    const resp = await requester.post(PREFIX, individuo);
    return resp.data;
  },
  findAll: async (params = {}) => {
    const resp = await requester.get(PREFIX, params);
    return resp.data;
  },
  findById: async (id) => {
    const resp = await requester.get(`${PREFIX}/${id}`);
    return resp.data;
  },
};

export default individuoService;
