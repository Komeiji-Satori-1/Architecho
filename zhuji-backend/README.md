# 筑迹后端 · zhuji-backend

> **筑迹（Architecho）— A Sanctuary for Ancient Timber**
> 一座守护古建木构的数字圣所 · 后端工程

---

## 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [环境要求](#环境要求)
- [从 GitHub 拉取项目](#从-github-拉取项目)
- [环境配置步骤](#环境配置步骤)
- [MySQL 数据库下载安装与配置](#mysql-数据库下载安装与配置)
- [项目数据库配置](#项目数据库配置)
- [初始化数据](#初始化数据)
- [运行开发服务器](#运行开发服务器)

---

## 技术栈

| 分类 | 技术 | 版本 |
|------|------|------|
| 语言 | Python | 3.12.x |
| Web 框架 | Django | 6.0.3 |
| REST API | Django REST Framework | 3.17.1 |
| 跨域处理 | django-cors-headers | 4.9.0 |
| 图片处理 | Pillow | 12.2.0 |
| 数据库驱动 | mysqlclient | 最新稳定版 |
| 数据库 | MySQL | 8.0 |

---

## 项目结构

```
zhuji-backend/
├── manage.py
├── core/                     # Django 项目配置
│   ├── settings.py           # 全局配置（数据库、CORS、DRF 等）
│   ├── urls.py               # 根路由
│   ├── asgi.py
│   └── wsgi.py
├── users/                    # 用户模块（自定义 User、通知、奖励）
├── monuments/                # 古建筑模块（遗存、打卡进度、投稿）
├── quiz/                     # 答题模块（题目、答题记录）
├── forum/                    # 论坛模块（板块、帖子、图片、评论）
├── cocreation/               # 筑品共创模块（作品提交、图片）
├── stamps/                   # 集章印记模块（印章、图层、用户集章）
├── system/                   # 系统管理模块（敏感词、AI 配置、节点状态）
├── api/                      # 通用 API 入口（保留）
└── media/                    # 上传文件存放目录（运行时自动创建）
```

---

## 环境要求

| 工具 | 最低版本 | 说明 |
|------|---------|------|
| Python | 3.12.x | 推荐使用虚拟环境（venv） |
| pip | 23.x | 随 Python 附带 |
| MySQL | 8.0 | 见下方安装说明 |

验证已安装版本：

```bash
python --version
pip --version
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

### 3. 进入后端目录

```bash
cd architecho/zhuji-backend
```

---

## 环境配置步骤

### 1. 创建并激活虚拟环境

**Windows：**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux：**

```bash
python3 -m venv venv
source venv/bin/activate
```

激活成功后，命令行提示符前会出现 `(venv)` 标识。

### 2. 安装 Python 依赖

```bash
pip install django==6.0.3 djangorestframework==3.17.1 django-cors-headers==4.9.0 Pillow mysqlclient
```

> **注意**：安装 `mysqlclient` 前需要本机已安装 MySQL（或其开发头文件）。Windows 用户若安装失败，可先安装 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)，或使用预编译包：
> ```bash
> pip install mysqlclient --only-binary :all:
> ```

---

## MySQL 数据库下载安装与配置

### 1. 下载 MySQL 8.0

前往官方下载页面：[https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)

- 选择 **MySQL Community Server 8.0.x**
- Windows 推荐下载 **MySQL Installer（.msi）**；macOS 下载 **DMG Archive**

### 2. 安装 MySQL

**Windows（Installer）：**

1. 运行 `.msi` 安装包，选择 **Developer Default** 或 **Server only**
2. 设置 root 用户密码（请妥善保管，后续项目配置需要用到）
3. 确保勾选 **Start the MySQL Server at System Startup**
4. 完成安装后，验证服务是否运行：

```bash
mysql --version
```

**macOS（Homebrew）：**

```bash
brew install mysql@8.0
brew services start mysql@8.0
mysql_secure_installation   # 设置 root 密码
```

### 3. 连接 MySQL 并创建数据库

以 root 身份登录 MySQL 控制台：

```bash
mysql -u root -p
```

输入密码后，依次执行以下 SQL 命令：

```sql
-- 创建数据库，使用 utf8mb4 字符集以支持中文及 Emoji
CREATE DATABASE architecho CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 验证数据库已创建
SHOW DATABASES;

-- 退出控制台
EXIT;
```

---

## 项目数据库配置

打开 `core/settings.py`，找到 `DATABASES` 部分，按本机 MySQL 实际情况填写：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'architecho',       # 数据库名（与上方创建的一致）
        'USER': 'root',             # MySQL 用户名
        'PASSWORD': 'your_password_here',  # 替换为你的 MySQL root 密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

> **安全提示**：生产环境中请将密码等敏感信息通过环境变量注入，而非直接硬编码在 `settings.py` 中。

---

## 初始化数据

### 1. 生成数据库迁移文件

```bash
python manage.py makemigrations users monuments quiz forum cocreation stamps system
```

> 若 Django 询问字段重命名（如 `Was monument.title renamed to monument.name?`），输入 `y` 确认。

### 2. 执行数据库迁移

```bash
python manage.py migrate
```

执行成功后，MySQL 中的 `architecho` 数据库将自动创建所有数据表。

### 3. 创建超级管理员账号

```bash
python manage.py createsuperuser
```

按提示依次输入用户名、邮箱（可留空）、密码，完成后即可使用该账号登录 Django Admin 后台。

### 4. 创建媒体文件目录（首次运行）

```bash
mkdir media
```

> Django 在处理图片上传时会自动使用此目录，也可跳过此步骤（运行时自动创建）。

---

## 运行开发服务器

```bash
python manage.py runserver
```

默认监听 `127.0.0.1:8000`，启动成功后可访问：

| 地址 | 说明 |
|------|------|
| `http://127.0.0.1:8000/admin/` | Django 管理后台 |
| `http://127.0.0.1:8000/api/users/` | 用户 API |
| `http://127.0.0.1:8000/api/monuments/` | 古建筑 API |
| `http://127.0.0.1:8000/api/forum/` | 论坛 API |
| `http://127.0.0.1:8000/api/stamps/` | 集章 API |
| `http://127.0.0.1:8000/api/cocreation/` | 共创 API |
| `http://127.0.0.1:8000/api/quiz/` | 答题 API |
| `http://127.0.0.1:8000/api/system/` | 系统管理 API |

如需指定端口或允许外部访问：

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## API 路由总览

```
/admin/                    # Django Admin 后台
/api/auth/                 # DRF 内置会话认证
/api/users/                # 用户注册、登录、个人信息
/api/monuments/            # 古建筑列表、详情、打卡
/api/quiz/                 # 答题题库、提交答案
/api/forum/                # 论坛板块、帖子、评论
/api/cocreation/           # 筑品共创投稿
/api/stamps/               # 集章印记
/api/system/               # 管理后台系统配置
```

---

## CORS 跨域配置

默认允许以下前端地址跨域访问（`core/settings.py`）：

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

前端开发服务器运行在其他端口时，在此列表中追加对应地址即可。
