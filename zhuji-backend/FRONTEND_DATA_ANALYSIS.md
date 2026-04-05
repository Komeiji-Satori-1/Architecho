# 筑迹前端数据模型全量分析报告

> 源文件范围：`zhuji-frontend/src/` 下全部 7 个视图 + 4 个组件/路由  
> 用途：指导后端 Django models.py 完整重构  
> 生成日期：2026-04-04

---

## 一、页面 & 数据对应速查

| Vue 文件 | 涉及数据实体 |
|---|---|
| `Home.vue` | ForumPost(hotTopics), UserStamp(StampLayer 进度), CoCreationAnnouncement |
| `ForumList.vue` | ForumCategory, ForumPost, User(topUsers+活跃榜), Badge/UserStamp(勋章馆) |
| `PostDetail.vue` | ForumPost, Comment(含嵌套 replies), User(isAdmin) |
| `StampDiscovery.vue` | Monument(buildings档案), QuizQuestion, Stamp(套色印章), StampColorLayer, UserStamp |
| `CoCreation.vue` | CoCreationItem(coCreations+myProgress), CoCreationImage(form.images) |
| `UserProfile.vue` | User(quiz正确率/足迹), UserStamp(印章册), Notification(messages), Reward |
| `AdminDashboard.vue` | User(userList), ArticleSubmission(auditItems), SensitiveWord(keywords), AIConfig, NodeStatus |
| `PostCard.vue` | ForumPost(id, title, cover, category, author, views, comments) |
| `StampLayer.vue` | UserStamp(progress, collected, total, description) |
| `AuthModal.vue` | User(账号登录) |

---

## 二、各页面常量/变量字段清单

### 2.1 AdminDashboard.vue

#### `auditItems`（投稿审核队列）
```ts
{
  id: number
  title: string          // 标题
  author: string         // "@用户名"
  time: string           // "HH:MM"
  status: '待处理' | '已驳回' | '已通过'
  image: string          // 图片 URL
  desc: string           // 正文摘要
}
```

#### `userList`（用户管理表）
```ts
{
  id: number
  name: string           // 显示名（用户名）
  email: string
  role: '超级管理员' | '版主' | '普通用户'
  roleBg: string         // Tailwind class，由 role 计算
  active: boolean        // true=正常 false=已封禁
  avatar: string         // 头像 URL
}
```

#### `stats`（统计大盘）
```ts
{
  label: '今日新增投稿' | '待审核任务' | '活跃工匠数' | 'AI 拦截率'
  value: string
  unit?: string          // "次/日"
  trend: string
  trendClass: string
  color: string
}
```

#### `keywords`（敏感词库）
```ts
string[]  // ['历史争议', '恶意广告', '违规外链']
```

#### 节点负载（系统健康度）
```ts
// 3个节点，各有 load_percentage
node_index: 1 | 2 | 3
load_percentage: number  // 0–100
```

---

### 2.2 ForumList.vue

#### `categories`（论坛板块）
```ts
{
  name: '营造法式' | '古建摄影' | '模型制作' | '木作工艺' | '彩画装饰'
  count: string     // "2.4k" 帖子数
  hot: boolean      // Hot 标签
}
```

#### `posts`（帖子列表）
```ts
{
  id: number
  title: string
  excerpt: string
  author: string
  authorAvatar: string
  category: string
  time: string           // "3小时前"
  views: string          // "1.2w"
  likes: string          // "856"
  comments: number
  isTop: boolean         // 置顶
  isEssence: boolean     // 精华
  images?: string[]      // 可选图片组
}
```

#### `topUsers`（活跃榜）
```ts
{
  name: string
  power: string      // 影响力值 "9.8k"
  avatar: string
  badges: number     // 勋章数量
}
```

#### `tabs`（筛选标签）
```ts
['全部动态', '精华帖', '最新发布']
```

---

### 2.3 PostDetail.vue

#### `post`（帖子详情）
```ts
{
  id: number
  title: string
  author: string
  authorAvatar: string
  category: string
  time: string           // "2024-03-20"
  lastEdit: string       // "2024-03-21 14:30"
  likes: number
  isTop: boolean
  isEssence: boolean
  content: string[]      // 段落数组
  images?: string[]
}
```

#### `comments`（评论列表，支持二级嵌套）
```ts
{
  id: number
  author: string
  avatar: string
  time: string
  text: string
  likes: number
  replies: {
    id: number
    author: string
    avatar: string
    time: string
    text: string
  }[]
}
```

---

### 2.4 StampDiscovery.vue

#### `buildings`（古建档案卡）
```ts
{
  id: number
  name: string           // "佛光寺东大殿"
  location: string       // "山西 · 五台山"
  status: '进行中' | '已解锁' | '未开始'   // ← per-user 状态
  image: string
  desc: string           // 短摘要
  fullDesc: string       // 详细描述（Modal 展示）
  era: string            // "唐大中十一年 (857年)"
  type: string           // "殿堂式木构"
}
```

#### `quizOptions`（答题选项）
```ts
{
  image: string          // 选项图片
}[]  // 支持2–4选项（图选题）
```

#### `stampSteps`（套色层）
```ts
{
  name: string   // "第一层：素胎底框"
  color: string  // "#e2e2e2"
}[]
```

#### 印章进度（StampLayer 组件 props → StampDiscovery 集章册）
```ts
{
  title: string
  progress: number    // 0–100
  collected: number   // 已收集印章数
  total: number       // 总印章数
  description: string
}
```

---

### 2.5 CoCreation.vue

#### `coCreations`（众创灵感瀑布流）
```ts
{
  id: number
  title: string
  author: string
  avatar: string      // 用户头像
  likes: string       // "1.2k"
  image: string       // 封面图
  featured: boolean   // 本周精选
}
```

#### `myProgress`（我的创意进度）
```ts
{
  id: number
  name: string        // 筑品名称
  status: '已采纳' | '待审核'
  percent: number     // 0–100 官方反馈进度
  image: string
}
```

#### `form`（提交表单）
```ts
{
  name: string        // 筑品名称
  material: '原木' | '青砖' | '石材' | '金属'
  desc: string        // 创意描述
  images: string[]    // 灵感图（多图）
}
```

#### 进度步骤（固定，前端硬编码）
```ts
['提交', '初审', '打样', '投产']
```

---

### 2.6 UserProfile.vue

#### `menuItems`（导航）
```ts
['进度看板', '印章册', '我的奖励', '消息管理']
```

#### 用户等级（侧边栏）
```ts
{
  level_num: number     // 2
  level_label: string   // "二级 · 营造生"
}
```

#### `footprintStats`（探索足迹分类统计）
```ts
{
  label: '宫廷建筑' | '园林景观' | '民居建筑'
  percent: number
}[]
```

#### 答题正确率 Dashboard
```ts
{
  accuracy_percent: number   // 89
  total_questions: number    // 240
  rank_percent: number       // "领先 92% 的营造师"
  footprint_total: number    // 42/150
}
```

#### `stamps`（印章册）
```ts
{
  id: number
  name: string        // "故宫 · 角楼"
  unlocked: boolean
  image?: string
}[]
```

#### `messages`（消息通知）
```ts
{
  id: number
  title: string       // "李工 回复了你的评论"
  content: string
  time: string        // "10分钟前"
  unread: boolean
  icon: Component     // 图标（由 type 决定）
  typeBg: string      // Tailwind bg class
  typeColor: string   // Tailwind text class
}
// 消息类型枚举（隐含）：reply | announcement | badge | reward
```

#### `rewards`（我的奖励）
```ts
{
  id: number
  name: string        // "故宫门票优惠券"
  desc: string        // "有效期至 2026-12-31"
  icon: Component     // TicketIcon | AwardIcon
}
```

---

### 2.7 Home.vue

#### `hotTopics`（论坛热门话题）
```ts
{
  title: string
  author: string
  reads: string    // "1.2k"
}[]
```

#### 共创动态（硬编码，需后端支撑`CoCreationAnnouncement`）
- **官方采纳**：某用户提交被列入试产计划  
- **新挑战开启**：某主题周边设计挑战赛启动  

---

### 2.8 PostCard.vue（组件 Props）
```ts
interface Post {
  id: number
  title: string
  cover: string     // 封面图
  category: string
  author: string
  views: string
  comments: number
}
```

---

## 三、完整数据模型与 Django App 映射

### 新增应用（相较初始设计）

| App | 说明 |
|---|---|
| `forum` | 论坛板块、帖子、帖子图片、评论（含二级嵌套） |
| `cocreation` | 共创筑品条目、多图上传 |
| `stamps` | 印章定义、套色层、用户印章收藏 |

### 各 Model 对应关系总览

```
users/
  User                  ← AdminDashboard.userList + UserProfile 用户信息
  Notification          ← UserProfile.messages
  Reward                ← UserProfile.rewards

monuments/
  Monument              ← StampDiscovery.buildings（大幅扩展字段）
  UserMonumentProgress  ← buildings.status（per-user 探索进度）
  ArticleSubmission     ← AdminDashboard.auditItems（论坛投稿审核）

forum/
  ForumCategory         ← ForumList.categories
  ForumPost             ← ForumList.posts + PostDetail.post + PostCard
  PostImage             ← post.images[]
  Comment               ← PostDetail.comments（含 parent 自关联）

cocreation/
  CoCreationItem        ← CoCreation.coCreations + myProgress + form
  CoCreationImage       ← form.images[]

stamps/
  Stamp                 ← UserProfile.stamps + StampDiscovery.集章册
  StampColorLayer       ← StampDiscovery.stampSteps
  UserStamp             ← UserStamp M2M through（含 unlocked_layers）

quiz/
  QuizQuestion          ← StampDiscovery.quizOptions（扩展图选题）
  UserQuizRecord        ← UserProfile.答题正确率统计

system/
  SensitiveWord         ← AdminDashboard.keywords
  AIConfig              ← AdminDashboard.AI 监管配置
  AIInterceptionLog     ← dashboard.AI 拦截率统计
  NodeStatus            ← 系统健康度节点负载
```

---

## 四、前端 → 后端字段精确映射表

### User 模型关键字段
| 前端字段 | 后端字段 | 备注 |
|---|---|---|
| `name` | `username` | AbstractUser 自带 |
| `email` | `email` | AbstractUser 自带 |
| `role` | `role` (CharField) | superadmin/moderator/user |
| `roleBg` | — | serializer 计算 |
| `active` | `is_active` | AbstractUser 自带 |
| `avatar` | `avatar` (ImageField) | — |
| `"二级·营造生"` | `level_num` + `level_title` | — |
| `power "9.8k"` | `influence_power` (IntegerField) | — |
| `accuracy 89%` | `quiz_correct_count / quiz_total_count` | 计算属性 |
| `42/150 足迹` | `footprint_count` | — |

### Monument 模型关键字段
| 前端字段 | 后端字段 | 备注 |
|---|---|---|
| `name` | `name` | — |
| `location` | `location` | — |
| `status` | `UserMonumentProgress.status` | per-user，独立模型 |
| `image` | `cover_image` (ImageField) | — |
| `desc` | `desc` (CharField 500) | 短摘要 |
| `fullDesc` | `full_desc` (TextField) | Modal 详情 |
| `era` | `era` | "唐大中十一年 (857年)" |
| `type` | `structure_type` | "殿堂式木构" |

### ArticleSubmission 模型关键字段
| 前端字段 | 后端字段 | 备注 |
|---|---|---|
| `author "@墨染匠心"` | `author` (FK User) | serializer 加 @ 前缀 |
| `time "14:20"` | `time` (DateTimeField) | serializer format HH:MM |
| `status '待处理'` | `status` 枚举 | pending/approved/rejected |
| `desc` | `desc` | — |
| `image` | `image` (ImageField) | — |
| — | `feedback` | 审核反馈建议 |

### ForumPost 模型关键字段
| 前端字段 | 后端字段 | 备注 |
|---|---|---|
| `isTop` | `is_top` | — |
| `isEssence` | `is_essence` | — |
| `views "1.2w"` | `views` (IntegerField) | serializer 格式化 |
| `time "3小时前"` | `created_at` | serializer 相对时间 |
| `lastEdit` | `updated_at` | — |
| `content: string[]` | `content` (TextField) | JSON段落数组 |
| `excerpt` | `excerpt` (CharField 500) | — |
| `cover` | `cover` (ImageField) | PostCard 封面 |
| `images?` | `PostImage` (FK) | 独立图片表 |
| `comments: number` | 关联 `Comment` count | — |

### CoCreationItem 模型关键字段
| 前端字段 | 后端字段 | 备注 |
|---|---|---|
| `title`/`form.name` | `title` | — |
| `material` | `material` | 原木/青砖/石材/金属 |
| `desc`/`form.desc` | `desc` | — |
| `featured` | `featured` | 本周精选 |
| `likes "1.2k"` | `likes` (IntegerField) | — |
| `status '已采纳'` | `status` | submitted/reviewing/sampling/producing/adopted/rejected |
| `percent 75` | `progress_percent` | 官方反馈进度 0-100 |
| `form.images[]` | `CoCreationImage.image` | 独立图片表 |

### UserStamp 关键字段
| 前端字段 | 后端字段 | 备注 |
|---|---|---|
| `stamp.unlocked` | `UserStamp.unlocked_layers > 0` | 属性计算 |
| `unlockedLayers (1-3)` | `UserStamp.unlocked_layers` | — |
| `stampSteps[].name` | `StampColorLayer.layer_name` | — |
| `stampSteps[].color` | `StampColorLayer.color` | — |
| `collected 6/10` | `UserStamp` count | serializer 聚合 |

### Comment 关键字段
| 前端字段 | 后端字段 | 备注 |
|---|---|---|
| `author` | `author` (FK User) | — |
| `avatar` | `author.avatar` | — |
| `text` | `text` | — |
| `likes 24` | `likes` (IntegerField) | — |
| `replies[]` | `Comment.parent` 自关联 | null=一级，非null=回复 |
| `time "2小时前"` | `created_at` | serializer 相对时间 |

---

_本文档由代码分析自动生成，应随前端迭代同步更新。_

---

## 四、已实现 API 接口对照（2026-04-05 更新）

### 4.1 已上线接口

| 接口 | 方法 | 路径 | 对应组件 | 说明 |
|---|---|---|---|---|
| 精选古建 | GET | `/api/monuments/featured/` | `Home.vue` Hero 区 | 最新 `is_published=True` 的 Monument |
| 论坛热门 | GET | `/api/forum/hot-topics/` | `Home.vue` 热门话题栏 | 按 views 降序取前 5 |
| 共创动态 | GET | `/api/cocreation/recent-news/` | `Home.vue` 共创动态栏 | `status=adopted` 最近 2 条 |
| 集章进度 | GET | `/api/stamps/my-progress/` | `Home.vue` StampLayer 组件 | 需 JWT，返回用户进度最深的印章 |
| 论坛分类 | GET | `/api/forum/categories/` | `ForumList.vue` 左侧分类栏 | 全部分类，含 post_count |
| 论坛帖子 | GET | `/api/forum/posts/` | `ForumList.vue` + `PostCard.vue` | 支持 `?category=id&is_essence=true&ordering=-created_at` |
| 帖子详情 | GET | `/api/forum/posts/:id/` | `PostDetail.vue` | ForumPostDetailSerializer |
| 评论列表 | GET | `/api/forum/comments/?post=id` | `PostDetail.vue` | 含嵌套 replies |
| 用户登录 | POST | `/api/users/login/` | `AuthModal.vue` | 返回 JWT access + refresh + user info |
| 当前用户 | GET | `/api/users/me/` | 全局登录态检测 | 需 JWT |
| Token 刷新 | POST | `/api/users/token/refresh/` | axios 拦截器（待实现） | — |

### 4.2 前端组件字段映射更新

#### PostCard.vue（已更新 interface）
| 前端字段 | 后端字段（ForumPostListSerializer） | 说明 |
|---|---|---|
| `title` | `title` | — |
| `cover` | `cover`（ImageField URL，可 null） | null 时前端显示占位图 |
| `category_name` | `category_name` | ~~原 `category`~~ |
| `author` | `author`（username） | — |
| `author_avatar` | `author_avatar`（可 null） | — |
| `views` | `views`（number） | ~~原 string~~ |
| `comment_count` | `comment_count` | ~~原 `comments`~~ |

#### StampLayer.vue（已动态化）
| 前端 prop | 后端字段（StampProgressSerializer） | 说明 |
|---|---|---|
| `title` | `stamp.name` | — |
| `progress` | `(unlocked_layers / total_layers) * 100` | 0-100 整数 |
| `collected` | `unlocked_layers` | — |
| `total` | `stamp.total_layers` | — |
| `description` | 自动生成文案 | 剩余层数提示 |

### 4.3 待接入接口（暂用占位数据）

| 组件/功能 | 期望接口 | 当前状态 |
|---|---|---|
| `ForumList.vue` 活跃榜 topUsers | `GET /api/users/top-users/` | 占位数据 |
| `PostDetail.vue` 帖子内容 | `GET /api/forum/posts/:id/` | 硬编码 |
| `StampDiscovery.vue` 古建列表 | `GET /api/monuments/` | 硬编码 |
| `CoCreation.vue` 共创列表 | `GET /api/cocreation/items/` | 硬编码 |
| `UserProfile.vue` 用户信息 | `GET /api/users/me/` | 硬编码 |
