import axios from 'axios';

const service = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  timeout: 5000
});

// 请求拦截器：自动注入 token
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

// 响应拦截器：token 过期时自动刷新，刷新失败才踢出登录
service.interceptors.response.use(
  response => response.data,
  async error => {
    const originalRequest = error.config;

    // 403 = token 无效/过期，且不是重试请求，且有 refresh_token
    if (
      error.response?.status === 403 &&
      !originalRequest._retry &&
      localStorage.getItem('refresh_token')
    ) {
      originalRequest._retry = true;
      try {
        // 用 axios 原始实例刷新，避免触发自身拦截器死循环
        const res = await axios.post(
          `${service.defaults.baseURL}/api/users/token/refresh/`,
          { refresh: localStorage.getItem('refresh_token') }
        );
        const newToken = res.data.access;
        localStorage.setItem('access_token', newToken);
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
        return service(originalRequest); // 重试原请求
      } catch {
        // refresh token 也过期，清除登录状态
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
      }
    }

    if (error.response?.status === 401) {
      localStorage.clear();
      window.location.href = '/';
    }

    return Promise.reject(error);
  }
);

export default service;