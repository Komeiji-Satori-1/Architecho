## 模块二：古建科普答题（联动功能）✅ 已实现

### 1. 要实现的功能
**1.0 具体功能**：题目**嵌入每个文章页底部**，翻页前强制答题；答对后解锁对应印章层，集齐全部层触发庆典动画。
**1.1 引入的新库**：无。
**1.2 后端 App**：`monuments`（文章/页）+ `quiz`（题目/选项/作答记录）。
**1.3 数据表结构**（已有，无需修改）：
* `QuizQuestion`（表 `quiz_question`）：含 `article_page` FK → `MonumentArticlePage`，`monument` FK，`question_type`（`single`/`multi`），`points`。关联关系**反向存储**在 `QuizQuestion` 上，无需给 `MonumentArticlePage` 添加字段。
* `QuizOption`（表 `quiz_option`）：含 `question` FK，`text`，`is_correct`。

**1.4 序列化器**（已有，无需新增）：`MonumentArticlePageSerializer.get_quiz_questions()` 通过反向关系 `article_page.quiz_questions` 直接嵌套完整的 `QuizQuestionSerializer` 数据（含选项）。
**1.5 API 接口**（已有）：`GET /api/monuments/articles/by-monument/{monument_id}/` 一次性返回文章 + 分页 + 嵌套题目，无需独立 quiz 接口。提交答案使用 `POST /api/quiz/submit-answer/`。
**1.6 前端组件**（已实现）：`MonumentArticle.vue` 每页底部弹出题目卡片，答对后自动翻页，无需独立路由跳转。

### 2. 实现路径（已完成，仅供参考）
**2.1 后端 View**：`MonumentArticleViewSet.by_monument` action 预取 `pages__quiz_questions__options`，一并返回。
**2.2 后端 Models**：利用 `QuizQuestion.article_page` 的反向关系 (`obj.quiz_questions`) 查询，无需在 `MonumentArticle` 上添加方法。
**2.4 前端函数**：文章加载时题目随数据一并到达；`submitAnswer()` 调用 `POST /api/quiz/submit-answer/`（payload: `question_id` + `selected_option_ids`），接收 `is_correct`、`points_earned`、`stamp_unlocked`。

---

## 模块三：筑品共创（审核与上传）⏳ 部分待实现

### 1. 要实现的功能
**1.0 具体功能**：
* **用户端**：完善文创想法（图片+文字）的上传功能（当前前端用 picsum 占位，图片字段未真实上传）。
* **管理端**：增加审核流程，可推进状态（`submitted` → `reviewing` → `sampling` → `producing` → `adopted` / `rejected`）。
* **详情展示**：点击文创卡片弹出 Modal（弹窗）展示设计初衷与细节。

**1.1 引入的新库**：无（`Pillow` 已被 `monuments`/`users` 模块引入，无需重复安装）。
**1.2 后端 App**：`cocreation`。
**1.3 数据表结构**（已有，无需新建）：
* `cocreation_cocreationitem`：`title`, `author` FK, `material`, `desc`, `cover`（主图），`featured`, `likes`, `status`（字符串枚举：`submitted`/`reviewing`/`sampling`/`producing`/`adopted`/`rejected`），`progress_percent`。
* `CoCreationImage`（关联图集）：`item` FK, `image`。

**1.4 序列化器**（部分已有）：复用 `CoCreationListSerializer`（已支持列表/创建/展示）；管理端审核可参照 `SubmissionViewSet.audit` 新增 `audit` action + 专用序列化器。
**1.5 API 接口**：
* 创建：复用已有 `POST /api/cocreation/items/`（`CoCreationItemViewSet.create`，需补全 `cover` 图片字段）。
* 管理端审核：新增 `POST /api/cocreation/items/{id}/audit/`（参照 `SubmissionViewSet.audit`，限制 `IsAdminUser`）。

**1.6 前端组件（待新建）**：`IdeaDetailModal.vue`。

### 2. 实现路径（待实现部分）
**2.1 后端 View**：在 `CoCreationItemViewSet` 中新增 `audit` action（参照 `SubmissionViewSet.audit`），使用 `IsAdminUser` 权限；`perform_create` 已绑定 `author=request.user`，仅需前端传入 `multipart/form-data` 格式的 `cover` 字段。
**2.4 前端函数**：使用 `FormData` 上传 `cover` 图片至 `POST /api/cocreation/items/`；`openModal(item)` 将当前选中的文创数据传入 `IdeaDetailModal.vue`。

---

## 模块四：个人中心与权限管理⏳ 后端已就绪，前端待实现

### 1. 要实现的功能
**1.0 具体功能**：
* **权限分流**：根据登录返回的 `role` 字段（`superadmin`/`moderator`/`user`），跳转至 `AdminDashboard` 或 `UserProfile` 页面。
* **数据动态化**：将 `UserProfile.vue` 中硬编码的 mock 数据替换为真实 API 数据。

**1.1 引入的新库**：无（`djangorestframework-simplejwt` 已在 `users` App 中使用）。
**1.2 后端 App**：`users`。
**1.3 数据表结构**（已有，无需修改）：用户数据存于 `users_user`（继承 `AbstractUser`），已含 `level_num`、`level_title`、`influence_power`、`quiz_correct_count`、`quiz_total_count`、`footprint_count` 及 `quiz_accuracy` property。

**1.4 序列化器**：新增 `UserProfileSerializer`，复用 `User` 模型字段，供 `MeView` 返回个人主页所需完整数据。（已有的 `UserDetailSerializer` 用于管理端，字段不同，分开维护。）
**1.5 API 接口**（后端已有）：`GET /api/users/me/`（`MeView`），需扩充返回字段（`quiz_correct_count`、`quiz_total_count`、`footprint_count`、集章/帖子统计）。
**1.6 前端组件**：`UserProfile.vue`（文件已存在，当前全部为 mock 数据，需接入 API）。

### 2. 实现路径（待实现部分）
**2.1 后端 View**：`MeView`（已实现），仅需扩展序列化字段，复用 `User` 模型上已有的统计字段和 property。
**2.4 前端函数**：
* **路由守卫**：在 `router/index.js` 中完善 `beforeEach`，依据 `localStorage` 中存储的 `role` 字段拦截非管理员访问 `/admin`。
* `initUserData()`: 页面挂载时调用 `GET /api/users/me/`，将结果绑定至各统计区块（等级、答题正确率、探索足迹、集章记录）。

---

### 给开发者的特别建议（基于你的习惯）：

1.  **权限校验**：`SubmissionViewSet`、`UserViewSet` 等管理端 ViewSet 已配置 `IsAdminUser`/`IsAdminOrModerator`，新增审核类 action 时记得同步添加权限类，勿遗漏。
2.  **算法性能**：热度算法建议在后端通过 SQL 原生查询或 `annotate` 实现，避免在内存中循环计算大量数据。
3.  **图片上传**：前端表单涉及图片字段时，需将 `Content-Type` 设为 `multipart/form-data`；后端 `ImageField` 已就绪，无需额外处理。