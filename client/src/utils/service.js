import requester from "./request";

class GenericService {
  constructor(serviceURL) {
    this.url = serviceURL;
  }

  async findAll(params = {}) {
    const resp = await requester.get(`${this.url}`, params);
    return resp.data;
  }

  findById = async (id) => {
    const resp = await requester.get(`${this.url}/${id}`);
    return resp.data;
  };

  create = async (item) => {
    const resp = await requester.post(`${this.url}`, item);
    return resp;
  };

  modify = async (id, item) => {
    const resp = await requester.patch(`${this.url}/${id}`, item);
    return resp.data;
  };
}

export default GenericService;
