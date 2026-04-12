import axios from 'axios';

// 基础路径逻辑：如果环境变量没配，默认走代理前缀 /api
const BASE_URL = import.meta.env.VITE_API_URL || '/api';

const service = axios.create({
  baseURL: BASE_URL,
  timeout: 5000
});

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// 响应拦截器
service.interceptors.response.use(
  response => response.data,
  async error => {
    const originalRequest = error.config;

    // 针对 Django SimpleJWT，通常过期返回的是 401 或 403
    // 这里建议同时兼容 401 和 403（根据你后端的实际设置来）
    if (
      (error.response?.status === 401 || error.response?.status === 403) &&
      !originalRequest._retry &&
      localStorage.getItem('refresh_token')
    ) {
      originalRequest._retry = true;
      try {
        // 使用相对路径，确保它能被 Vite 的 proxy 捕获并转发到 http://127.0.0.1:8000
        const res = await axios.post(`${BASE_URL}/users/token/refresh/`, {
          refresh: localStorage.getItem('refresh_token')
        });
        
        const newToken = res.data.access;
        localStorage.setItem('access_token', newToken);
        
        // 重试原始请求
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
        return service(originalRequest); 
      } catch (refreshError) {
        // Refresh Token 也失效了，彻底清理
        localStorage.clear(); // 简单粗暴，一次清理干净
        window.location.href = '/';
        return Promise.reject(refreshError);
      }
    }

    // 处理其他 401 错误（比如没登录直接访问）
    if (error.response?.status === 401 && !localStorage.getItem('refresh_token')) {
      localStorage.clear();
      window.location.href = '/';
    }

    return Promise.reject(error);
  }
);

export default service;