# 筑迹前端 · zhuji-frontend

> **筑迹（Architecho）— A Sanctuary for Ancient Timber**
> 一座守护古建木构的数字圣所 · 前端工程

---123456789

## 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [环境要求](#环境要求)
- [从 GitHub 拉取项目](#从-github-拉取项目)
- [环境配置步骤](#环境配置步骤)
- [运行开发服务器](#运行开发服务器)
- [构建生产版本](#构建生产版本)

---

## 技术栈

| 分类 | 技术 | 版本 |
|------|------|------|
| 核心框架 | Vue 3 (Composition API) | ^3.5.32 |
| 语言 | TypeScript | ~5.8.2 |
| 构建工具 | Vite | ^6.2.0 |
| 路由 | Vue Router | ^4.6.4 |
| CSS 框架 | Tailwind CSS | ^4.1.14 |
| 动效库 | Motion | ^12.23.24 |
| 图标库 | Lucide React | ^0.546.0 |
| AI 接入 | Google Gemini SDK | ^1.29.0 |
| 本地服务 | Express | ^4.21.2 |

---

## 项目结构

```
zhuji-frontend/
├── src/
│   ├── main.ts               # 应用入口
│   ├── App.vue               # 根组件
│   ├── index.css             # 全局样式（Tailwind 入口）
│   ├── env.d.ts              # 环境变量类型声明
│   ├── components/           # 公共组件
│   │   ├── Navbar.vue        # 顶部导航栏
│   │   ├── AuthModal.vue     # 登录 / 注册弹窗
│   │   ├── PostCard.vue      # 论坛帖子卡片
│   │   └── StampLayer.vue    # 集章图层组件
│   ├── router/
│   │   └── index.ts          # Vue Router 路由配置
│   └── views/                # 页面视图
│       ├── Home.vue          # 首页
│       ├── ForumList.vue     # 论坛列表
│       ├── PostDetail.vue    # 帖子详情
│       ├── StampDiscovery.vue # 集章发现
│       ├── CoCreation.vue    # 筑品共创
│       ├── UserProfile.vue   # 用户个人中心
│       └── AdminDashboard.vue # 管理后台
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── metadata.json
```

---

## 环境要求

| 工具 | 最低版本 | 说明 |
|------|---------|------|
| Node.js | 18.x LTS | 推荐 20.x LTS 或更高 |
| npm | 9.x | 随 Node.js 附带；也可使用 pnpm / yarn |

验证已安装版本：

```bash
node -v
npm -v
```

---

## 从 GitHub 拉取项目

### 1. 安装 Git

前往 [https://git-scm.com/downloads](https://git-scm.com/downloads) 下载并安装 Git，安装完成后验证：

```bash
git --version
```

### 2. 克隆仓库

```bash
git clone https://github.com/<your-username>/architecho.git
```

> 将 `<your-username>` 替换为实际的 GitHub 用户名或组织名。

### 3. 进入前端目录

```bash
cd architecho/zhuji-frontend
```

---

## 环境配置步骤

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

在 `zhuji-frontend/` 根目录创建 `.env` 文件（该文件已被 `.gitignore` 忽略，不会提交到仓库）：

```env
# Google Gemini API Key（AI 功能需要）
GEMINI_API_KEY=your_gemini_api_key_here
```

> 如暂不使用 AI 功能，可留空或跳过此步骤。

### 3. 确认后端地址（可选）

如需修改后端 API 地址，在 `vite.config.ts` 的 `server` 中添加代理配置：

```ts
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
  },
},
```

---

## 运行开发服务器

```bash
npm run dev
```

启动成功后，浏览器访问：

```
http://localhost:3000
```

> 开发服务器默认绑定 `0.0.0.0:3000`，局域网内其他设备也可通过本机 IP 访问。

---

## 构建生产版本

```bash
npm run build
```

构建产物输出至 `dist/` 目录，可部署到任意静态文件托管服务（Nginx、Vercel、OSS 等）。

预览构建结果：

```bash
npm run preview
```

---

## 页面路由一览

| 路径 | 视图 | 说明 |
|------|------|------|
| `/` | Home.vue | 首页 · 推荐古建 |
| `/forum` | ForumList.vue | 论坛广场 |
| `/forum/:id` | PostDetail.vue | 帖子详情 |
| `/stamps` | StampDiscovery.vue | 集章印记 |
| `/co-creation` | CoCreation.vue | 筑品共创 |
| `/profile` | UserProfile.vue | 个人中心 |
| `/admin` | AdminDashboard.vue | 管理后台（需权限） |
