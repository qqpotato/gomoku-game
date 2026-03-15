# 五子棋游戏 - Windows 打包指南

本指南教你如何在 Windows 系统上生成可执行的 `.exe` 文件。

---

## 📋 系统要求

- Windows 10/11
- Python 3.8 或更高版本
- 约 500MB 可用磁盘空间

---

## 🚀 快速打包（推荐）

### 方法一：使用 PowerShell 脚本

1. **右键点击** `build-windows.ps1` 文件
2. 选择 **「使用 PowerShell 运行」**
3. 等待打包完成（约 2-5 分钟）
4. 生成的 exe 文件在 `dist\五子棋游戏.exe`

### 方法二：使用命令提示符

1. 打开 **命令提示符** 或 **PowerShell**
2. 进入项目目录：
   ```cmd
   cd 路径\到\gomoku-game
   ```
3. 运行批处理脚本：
   ```cmd
   build-windows.bat
   ```
4. 等待完成，exe 在 `dist\五子棋游戏.exe`

---

## 🔧 手动打包

如果想手动操作，按以下步骤：

### 1. 安装 Python

下载地址：https://www.python.org/downloads/

⚠️ **重要**：安装时勾选 「Add Python to PATH」

### 2. 打开命令行

```cmd
# 进入项目目录
cd 路径\到\gomoku-game

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

### 3. 安装依赖

```cmd
pip install --upgrade pip
pip install pygame pyinstaller
```

### 4. 打包成 exe

```cmd
pyinstaller --onefile --windowed --name "五子棋游戏" gomoku.py
```

### 5. 获取 exe 文件

打包完成后，可执行文件位于：
```
dist\五子棋游戏.exe
```

---

## 📦 分发游戏

### 方案 A：只分发 exe（推荐）

将 `dist\五子棋游戏.exe` 单独复制给其他用户即可运行。

- ✅ 优点：单文件，方便分发
- ❌ 缺点：文件较大（约 30-40 MB）

### 方案 B：分发整个文件夹

将 `dist` 文件夹整体打包成 zip 发送。

---

## 🎯 高级选项

### 添加游戏图标

1. 准备 `.ico` 格式的图标文件（如 `icon.ico`）
2. 修改打包命令：
   ```cmd
   pyinstaller --onefile --windowed --name "五子棋游戏" --icon=icon.ico gomoku.py
   ```

### 不创建控制台窗口

已包含 `--windowed` 参数，不会显示命令行窗口。

### 减小文件体积

```cmd
# 使用 UPX 压缩（需要额外安装 UPX）
pyinstaller --onefile --windowed --name "五子棋游戏" --upx-dir=upx gomoku.py
```

---

## ⚠️ 常见问题

### 1. 提示「找不到 Python」

- 确保安装了 Python
- 安装时勾选了「Add Python to PATH」
- 重启命令行后再试

### 2. 杀毒软件报毒

这是误报。PyInstaller 打包的程序有时会被误判。
- 将 `dist` 文件夹添加到杀毒软件白名单
- 或使用数字签名（需要购买证书）

### 3. 运行时闪退

- 确保安装了 Visual C++ Redistributable
- 下载地址：https://aka.ms/vs/17/release/vc_redist.x64.exe

### 4. 中文显示乱码

- 确保系统区域设置支持中文
- Windows 10/11 默认已支持

---

## 📊 打包参数说明

| 参数 | 说明 |
|------|------|
| `--onefile` | 打包成单个 exe 文件 |
| `--windowed` | 不显示控制台窗口 |
| `--name` | 指定 exe 文件名 |
| `--icon` | 指定图标文件 |
| `--add-data` | 添加额外数据文件 |

---

## 🎮 运行游戏

双击 `五子棋游戏.exe` 即可启动游戏！

功能：
- ✅ 双人对战
- ✅ 人机对战
- ✅ 悔棋功能
- ✅ 重新开始

---

## 📝 技术支持

如有问题，请检查：
1. Python 版本是否为 3.8+
2. 是否正确安装依赖
3. 杀毒软件是否拦截

---

*最后更新：2026-03-15*
