# 推送代码到 GitHub - 完整指南

## 前提条件

- ✅ GitHub 账号：`qqpotato`
- ✅ 本地 git 仓库已初始化
- ✅ 远程仓库已配置：`https://github.com/qqpotato/gomoku-game.git`

---

## 步骤 1：创建 Personal Access Token

### 1.1 访问 Token 设置页面

打开浏览器访问：
**https://github.com/settings/tokens**

### 1.2 生成新 Token

1. 点击 **"Generate new token"** 按钮
2. 选择 **"Generate new token (classic)"**

### 1.3 填写 Token 信息

| 字段 | 填写内容 |
|------|----------|
| **Note** | `Gomoku Game Push`（随便填，能识别就行） |
| **Expiration** | `90 days` 或 `No expiration`（推荐 90 天） |
| **Scopes/Permissions** | 勾选 **`repo`**（全选） |

### 1.4 生成并复制 Token

1. 点击页面底部的 **"Generate token"** 按钮
2. ⚠️ **立即复制 Token**（以 `ghp_` 开头的一长串字符）
3. 保存到安全的地方（只显示一次！）

---

## 步骤 2：推送代码到 GitHub

### 方法 A：使用 Token 推送（推荐）

在终端执行（替换 `YOUR_TOKEN` 为你刚生成的 Token）：

```bash
cd /Users/potato/.openclaw/workspace/gomoku-game

git push -u origin https://YOUR_TOKEN@github.com/qqpotato/gomoku-game.git main
```

**示例**（假设你的 Token 是 `ghp_abc123...`）：
```bash
git push -u origin https://ghp_abc123xyz789@github.com/qqpotato/gomoku-game.git main
```

### 方法 B：配置 Git 使用 Token

```bash
# 配置 git 记住凭据
git config --global credential.helper store

# 然后正常推送（会提示输入用户名和密码）
git push -u origin main
```

输入：
- Username: `qqpotato`
- Password: 粘贴你的 Token（`ghp_xxx`）

---

## 步骤 3：验证推送成功

推送成功后，访问你的仓库：
**https://github.com/qqpotato/gomoku-game**

应该能看到所有文件：
- ✅ `gomoku.py` - 游戏源码
- ✅ `README.md` - 项目说明
- ✅ `.github/workflows/build-windows.yml` - Actions 配置
- ✅ `build-windows.bat` - Windows 打包脚本
- ✅ 等等...

---

## 步骤 4：启用 GitHub Actions

### 4.1 启用 Actions

1. 访问 **https://github.com/qqpotato/gomoku-game/actions**
2. 如果是第一次使用，点击 **"I understand my workflows, go ahead and enable them"**

### 4.2 手动触发构建（可选）

1. 在 Actions 页面，点击左侧 **"Build Windows Executable"**
2. 点击 **"Run workflow"** 按钮
3. 选择 `main` 分支
4. 点击 **"Run workflow"**

### 4.3 下载构建的 exe

构建完成后（约 5-10 分钟）：
1. 点击最近的构建记录
2. 在页面底部找到 **"Artifacts"**
3. 点击 **`Gomoku-Windows`** 下载
4. 解压得到 `五子棋游戏.exe`

---

## 步骤 5：自动构建（可选）

每次推送 tag 时会自动构建 Windows exe：

```bash
# 创建版本标签
git tag v1.0.0

# 推送标签（触发自动构建）
git push origin v1.0.0
```

---

## 🔐 Token 安全提示

1. **不要分享 Token** - 就像密码一样
2. **Token 泄露了怎么办** - 立即在 GitHub 删除并重新生成
3. **Token 过期** - 重新生成一个新的
4. **建议** - 使用 90 天过期时间，定期更新

---

## ❓ 常见问题

### Q: 推送时提示 403 Forbidden？
A: Token 权限不足，确保勾选了 `repo` 权限。

### Q: 推送时提示 404 Not Found？
A: 检查仓库名是否正确，确保仓库已创建。

### Q: Actions 没有运行？
A: 检查：
1. Actions 是否已启用（Settings → Actions）
2. 工作流文件是否存在

### Q: 构建失败？
A: 点击失败的构建记录，查看日志排查问题。

---

## 📞 需要帮助？

如果遇到问题，告诉我具体错误信息，我会帮你解决！

---

*最后更新：2026-03-15*
