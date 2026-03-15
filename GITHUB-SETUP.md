# 五子棋游戏 - GitHub 上传指南

## 方法一：使用 GitHub 网页（推荐 ⭐）

### 步骤 1：在 GitHub 创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `gomoku-game`（或你喜欢的名字）
   - **Description**: 五子棋游戏 - 跨平台 Gomoku game with Python + Pygame
   - **Public/Private**: 选择公开或私有
   - ❌ 不要勾选 "Initialize this repository with a README"
3. 点击 **"Create repository"**

### 步骤 2：复制仓库 URL

创建后，GitHub 会显示类似这样的命令：
```
git remote add origin https://github.com/YOUR_USERNAME/gomoku-game.git
```

### 步骤 3：运行推送命令

在终端执行（替换 YOUR_USERNAME 为你的 GitHub 用户名）：

```bash
cd /Users/potato/.openclaw/workspace/gomoku-game

# 添加远程仓库（替换为你的仓库 URL）
git remote add origin https://github.com/YOUR_USERNAME/gomoku-game.git

# 推送代码
git push -u origin main
```

### 步骤 4：启用 GitHub Actions

1. 在 GitHub 仓库页面，点击 **"Actions"** 标签
2. 点击 **"I understand my workflows, go ahead and enable them"**
3. 现在每次推送代码都会自动构建 Windows exe！

---

## 方法二：使用 GitHub CLI

如果已安装 `gh` 命令行工具：

```bash
cd /Users/potato/.openclaw/workspace/gomoku-game

# 创建仓库并推送
gh repo create gomoku-game --public --source=. --remote=origin --push
```

---

## 方法三：手动上传 ZIP

1. 在 GitHub 创建空仓库
2. 点击 **"uploading an existing file"**
3. 拖拽项目文件上传
4. 提交更改

---

## 启用自动构建 Windows exe

推送代码后，GitHub Actions 会自动运行：

1. 访问 `https://github.com/YOUR_USERNAME/gomoku-game/actions`
2. 点击左侧 **"Build Windows Executable"**
3. 点击 **"Run workflow"**（如果需要手动触发）
4. 构建完成后，在 **Artifacts** 中下载 `五子棋游戏.exe`

### 自动触发

每次推送 tag 时会自动构建：
```bash
# 创建版本标签并推送
git tag v1.0.0
git push origin v1.0.0
```

---

## 下载 Windows exe

构建完成后：
1. 访问 Actions 页面
2. 点击最近的构建记录
3. 在 **Artifacts** 部分下载 `Gomoku-Windows`
4. 解压得到 `五子棋游戏.exe`

---

## 常见问题

### Q: 推送时提示需要认证？
A: 使用 GitHub Personal Access Token：
1. 访问 https://github.com/settings/tokens
2. 创建新 token（勾选 repo 权限）
3. 推送时使用：`https://TOKEN@github.com/USERNAME/REPO.git`

### Q: Actions 没有运行？
A: 检查：
1. Actions 是否已启用（Settings → Actions）
2. 工作流文件是否正确（`.github/workflows/build-windows.yml`）

### Q: 构建失败？
A: 查看 Actions 日志，常见问题：
- Python 版本不匹配
- 依赖安装失败
- 打包路径错误

---

*最后更新：2026-03-15*
