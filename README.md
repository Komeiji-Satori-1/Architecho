## 第一阶段：安全克隆
新建一个你本地的项目文件夹如：D:\my_projects\web\（以下所有操作均以该文件夹为例）
在该文件夹的空白处右键选择“选择更多选项” --> “open git bash here”
```bash
# 1. 克隆仓库（建议使用 SSH 或确定的 HTTPS 链接）
git clone https://github.com/Komeiji-Satori-1/Architecho.git

# 2. 进入目录
cd Architecho

# 3. 立即检查 .gitignore（这是安全的第一步！）
# 确认里面有 zhuji-backend/venv/ 和 **/___pycache__/
直接在vscode里面打开根目录下的.gitignore文件
```

---

## 第二阶段：建立并切换分支
**永远不要在 `main` 分支上直接写代码。** 每一个新功能（如“筑迹”的印章系统或古建资料展示）都应该有自己的分支。

```bash
# 1. 先确保本地 main 是最新的
git checkout main
git pull origin main

# 2. 创建并切换到新分支 (例如开发“共创”模块)
# 格式建议：dev/你的名字-功能。比如
git checkout -b dev/lixinde-cocreation-api（以下所有操作以该分支为例）
# 3. 验证当前所在分支
git branch
```

---

## 第三阶段：本地开发与环境隔离 (Develop)
vscode打开文件夹D:\my_projects\web\。上方点击“终端”、“新建终端”
在终端输入
```powershell
# 1. 进入后端目录重建虚拟环境
cd Architecho/zhuji-backend
python -m venv venv
.venv/Scripts/activate

# 2. 安装依赖
pip install -r requirements.txt
```

---

## 第四阶段：提交与推送 (Commit & Push)
当你写好了代码（比如修复了那个 `CoCreation.vue` 的路径报错），按照以下步骤推送。
**重点：修改哪个文件就只提交哪个文件。禁止提交项目下全部文件**
```bash
# 1. 查看改动了哪些文件
git status

# 2. 暂存改动（只添加你确定的代码文件，千万别点到 venv！）
git add zhuji-frontend/src/views/CoCreation.vue

# 3. 提交到本地仓库
git commit -m "fix(frontend): 修复别名路径别名报错并更新 tsconfig" #引号内为你对此次提交的说明

# 4. 推送到远程分支
# 第一次推送新分支需要关联远程
git push -u origin dev/lixinde-cocreation-api
```

---

## 💡 核心安全贴士（避坑指南）

### 1. 为什么用 `-u`？
`git push -u origin [分支名（比如zjy_commit、zjy-cocreation-api）]` 中的 `-u` (upstream) 会建立本地分支与远程分支的追踪关系。以后你在这个分支上只需要输入 `git push` 或 `git pull`，Git 就知道该往哪发，不容易出错。

### 2. 万一不小心 `add` 错了怎么办？
如果你发现 `git status` 里出现了 `venv/` 里的文件，**千万别 commit**！立即运行：
```bash
git reset HEAD <文件名>  # 撤销某个文件的暂存
# 或者彻底重置暂存区
git reset .
```

### 3. 如何保持分支不过时？
如果你在 `dev` 分支写了很久，`main` 分支已经领先你了，记得定期“同步”：
```bash
git checkout dev/cocreation-api
git fetch origin main
git merge origin/main
```
