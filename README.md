#
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
此处环境配置详细内容请参考前后端文件夹下的README.md
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

## “筑迹”项目工程开发与协作规范 (Standard Operating Procedure, SOP)

本规范旨在通过**流程化**与**标准化**的操作，规避以往开发中出现的代码污染、环境冲突及数据库版本断裂等问题，确保项目在多分支协作下的稳定性。

---

### 一、 仓库环境与文件管理规范

#### 1.1 严格执行 `.gitignore` 过滤
所有开发成员必须确保本地 `.venv`（虚拟环境）、`__pycache__`（编译缓存）、`*.pyc` 文件以及 `db.sqlite3`（本地数据库）处于非追踪状态。
* **操作标准**：在执行 `git add` 前，必须通过 `git status` 确认没有环境文件或临时文件进入暂存区。
* **清理机制**：若发现错误追踪，需执行 `git rm -r --cached [文件路径]` 将其从索引中剔除。

#### 1.2 分支切换准则
严禁在当前分支存在未提交（Uncommitted）改动的情况下强行切换分支。
* **标准流程**：
    1. 提交改动：`git commit -m "feat/fix: 描述"`。
    2. 若需保留进度但不生成提交：使用 `git stash` 暂存。
    3. 切换分支：`git checkout [目标分支]`。

---

### 二、 开发环境一致性要求

#### 1.3 数据库环境对齐
项目后端指定使用 **MySQL 8.x** 版本。
* **规范**：任何涉及数据库配置、加密方式或字符集的变更，必须同步更新开发文档。

#### 1.4 依赖同步机制
当功能涉及新增第三方库时，必须及时更新依赖表。
* **标准操作**：
    1. 导出依赖：`pip freeze > requirements.txt`。
    2. 同步依赖：团队成员在 `pull` 代码后，应立即执行 `pip install -r requirements.txt`。

---

### 三、 数据库迁移 (Migrations) 规范

#### 1.5 模型与迁移同步
数据库模型的改动与产生的 `migrations` 文件视为一个逻辑整体，必须在同一个 Commit 中提交。
* **合规性检查**：严禁仅提交 `models.py` 而遗漏 `00xx_initial.py` 等迁移脚本。

#### 1.6 迁移节点合并
在合并分支时，若出现迁移记录分叉（两个分支产生相同序号的迁移文件）：
* **处理流程**：执行 `python manage.py makemigrations --merge` 生成合并节点，随后执行 `python manage.py migrate` 同步数据库状态。

---

### 四、 隔离集成分支 (Integration Branch) 流程

为保护主分支（`main`）的稳定性，所有功能分支必须通过 **预合并集成分支** 进行验证。

#### 1.7 预合并操作模型

1.  **同步基准**：从最新的 `main` 分支拉取并创建 `pre-merge-test` 分支。
2.  **原子化集成**：在集成分支上逐一 `merge` 待上线的功能分支。
3.  **冲突处理原则**：
    * **内容冲突**：手动编辑文件保留逻辑。
    * **二进制/格式冲突**：对于 `requirements.txt` 等配置文件，若产生不可读冲突，优先使用稳定版本覆盖：`git checkout --theirs/--ours [路径]`，再进行增量修正。
4.  **回归测试**：
    * 运行 `python manage.py check` 检查静态逻辑。
    * 运行本地服务，针对 N+1 优化（`select_related`/`prefetch_related`）进行接口响应验证。

#### 1.8 最终发布
仅当 `pre-merge-test` 分支通过所有功能与环境测试后，方可由负责人将其合并至 `main` 分支并推送到远程仓库。

---

### 五、 异常中止与回滚

* **合并异常**：若 `merge` 过程中产生超出预期的逻辑混乱，应立即执行 `git merge --abort` 终止合并，清空工作区并重新评估集成策略。
* **版本回退**：若 `main` 分支出现重大故障，需通过 `git revert [commit_id]` 生成反向提交，确保开发记录的追溯性。