import axios from "axios";

const api = axios.create({ baseURL: "/api" });

export default {
  list: (params) => api.get("/tasks/", { params }).then((r) => r.data),
  dashboard: () => api.get("/tasks/dashboard/").then((r) => r.data),
  week: () => api.get("/tasks/week/").then((r) => r.data),
  late: () => api.get("/tasks/late/").then((r) => r.data),
  critical: () => api.get("/tasks/critical/").then((r) => r.data),
  create: (t) => api.post("/tasks/", t).then((r) => r.data),
  update: (id, t) => api.patch(`/tasks/${id}/`, t).then((r) => r.data),
  remove: (id) => api.delete(`/tasks/${id}/`),
};
