# 五子棋游戏 - 跨平台打包方案

本文档说明如何在不同操作系统上打包五子棋游戏。

---

## 📦 已生成的打包文件

### macOS ✅

| 文件 | 位置 | 大小 |
|------|------|------|
| `Gomoku.dmg` | `/Users/potato/.openclaw/workspace/gomoku-game/` | 30 MB |
| `五子棋游戏.app` | `dist/五子棋游戏.app` | - |

**运行方式：**
```bash
open Gomoku.dmg
# 拖拽应用到「应用程序」文件夹
```

---

## 🪟 Windows 打包方案

由于当前是 macOS 系统，无法直接生成 Windows exe。以下是三种方案：

### 方案一：在 Windows 上运行打包脚本 ⭐ 推荐

**步骤：**

1. 将整个 `gomoku-game` 文件夹复制到 Windows 电脑
2. 双击运行 `build-windows.bat`（或右键 `build-windows.ps1` → PowerShell 运行）
3. 等待 2-5 分钟，exe 生成在 `dist\五子棋游戏.exe`

**优点：**
- ✅ 最简单可靠
- ✅ 无需额外配置
- ✅ 自动处理所有依赖

**脚本位置：**
- `build-windows.bat` - 命令提示符版本
- `build-windows.ps1` - PowerShell 版本

---

### 方案二：GitHub Actions 自动构建 ☁️

**步骤：**

1. 将代码推送到 GitHub 仓库
2. 在 GitHub 上点击 Actions → "Build Windows Executable" → Run workflow
3. 构建完成后下载 artifact（`五子棋游戏.exe`）

**优点：**
- ✅ 无需 Windows 电脑
- ✅ 云端自动构建
- ✅ 可配置自动发布

**工作流文件：** `.github/workflows/build-windows.yml`

---

### 方案三：手动在 Windows 上打包

**Windows 电脑上执行：**

```cmd
cd gomoku-game

REM 创建虚拟环境
python -m venv venv
venv\Scripts\activate

REM 安装依赖
pip install pygame pyinstaller

REM 打包
pyinstaller --onefile --windowed --name "五子棋游戏" gomoku.py
```

**输出位置：** `dist\五子棋游戏.exe`

---

## 🐧 Linux 打包

```bash
cd gomoku-game

# 安装依赖
pip install pygame pyinstaller

# 打包
pyinstaller --onefile --windowed --name "gomoku" gomoku.py
```

**输出位置：** `dist/gomoku`

---

## 📊 打包对比

| 平台 | 工具 | 输出 | 大小 | 状态 |
|------|------|------|------|------|
| macOS | py2app + create-dmg | .dmg + .app | 30 MB | ✅ 已完成 |
| Windows | PyInstaller | .exe | ~35 MB | 📝 需 Windows 环境 |
| Linux | PyInstaller | 二进制文件 | ~35 MB | 📝 需 Linux 环境 |

---

## 🎯 快速开始

### macOS 用户
直接打开 `Gomoku.dmg` 安装即可！

### Windows 用户
1. 复制项目到 Windows
2. 运行 `build-windows.bat`
3. 运行生成的 `dist\五子棋游戏.exe`

### 没有 Windows 电脑？
使用 GitHub Actions 自动构建（方案二）

---

## 📁 文件清单

```
gomoku-game/
├── Gomoku.dmg                    # macOS 安装包 ✅
├── gomoku.py                     # 游戏源代码
├── setup.py                      # macOS 打包配置
├── build-windows.bat             # Windows 打包脚本 ⭐
├── build-windows.ps1             # Windows 打包脚本 (PS) ⭐
├── WINDOWS-BUILD.md              # Windows 详细指南
├── CROSS-PLATFORM-BUILD.md       # 本文档
├── .github/workflows/
│   └── build-windows.yml         # GitHub Actions ⭐
└── dist/
    └── 五子棋游戏.app            # macOS 应用 ✅
```

---

## 💡 提示

1. **分发游戏**：直接发送对应平台的打包文件即可
2. **更新游戏**：修改 `gomoku.py` 后重新运行打包脚本
3. **添加图标**：准备 `.ico` (Windows) 或 `.icns` (macOS) 文件

---

*最后更新：2026-03-15*
