import requester from "./request";

class GenericService {
  constructor(serviceURL) {
    this.url = serviceURL;
  }

  async findAll(params = {}) {
    const resp = await requester.get(`${this.url}/`, params);
    return resp.data;
  }

  async findById(id) {
    const resp = await requester.get(`${this.url}/${id}`);
    return resp.data;
  }

  async create(item) {
    const resp = await requester.post(`${this.url}/`, item);
    return resp;
  }

  async modify(id, item) {
    const resp = await requester.patch(`${this.url}/${id}`, item);
    return resp.data;
  }
}

export default GenericService;
