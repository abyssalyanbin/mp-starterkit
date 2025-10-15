# ESP32 Starter Kit 初学者指南

这份文档面向第一次接触编程与硬件的新手，帮助你理解 VS Code 扩展 **mp-lvgl-starterkit** 如何工作，以及日常应该怎么使用它来和 ESP32 开发板互动。

---

## 1. 它能做什么？

- **自动识别串口**：帮你找到电脑上连接的 ESP32 开发板。
- **一键烧录固件**：把 `.bin` 固件文件写入板子，快速刷新系统。
- **上传与运行 Python 文件**：把当前编辑的脚本推送到板子上，并直接运行。
- **批量同步文件/文件夹**：把你挑选的项目文件夹原样复制到板子内部，保持目录结构。
- **演示项目**：一键复制示例程序并自动重启板子，方便验证屏幕或外设是否工作。
- **记录操作日志**：把烧录、上传等操作记录到本地日志，发生问题时可追踪。

---

## 2. 必备知识（超轻量）

| 概念 | 简单解释 |
|------|----------|
| **串口 (Serial Port)** | 电脑与开发板通过 USB 交流用的通道，名字通常是 `COMx`（Windows）或 `/dev/ttyUSBx`（macOS/Linux）。 |
| **固件 (Firmware)** | 决定开发板“开机后跑什么”的基础程序，相当于手机系统。烧录固件 = 重装系统。 |
| **MicroPython / mpremote** | MicroPython 是运行在板子上的轻量 Python，`mpremote` 是与它沟通的命令行工具。 |
| **esptool** | 专门负责向 ESP32 写入固件的命令行工具。 |
| **工作区 (Workspace)** | VS Code 中打开的项目文件夹。扩展会在这里寻找要上传的文件。 |

---

## 3. 使用前准备

1. **安装扩展**：打开 VS Code，安装本扩展（mp-lvgl）。
2. **连接设备**：用 USB 线连好 ESP32 开发板，建议使用带数据线功能的好线材。
3. **确认驱动**：Windows 用户若使用 CH34x 或 CP210x 转串口芯片，需要先装好驱动。
4. **打开工作区**：把你要上传的项目文件夹用 VS Code 打开。

> 提示：如果想批量上传文件，确保它们已经在 VS Code 里可见，扩展才能找到。

---

## 4. 常用命令一览

> 如果想直接在 VS Code 中与板子交互，使用 "Starter Kit: 打开 REPL 终端"，扩展会自动帮你打开一个与设备相连的终端窗口。

在 VS Code 按 `Ctrl+Shift+P`（Windows）或 `Command+Shift+P`（macOS）呼出命令面板，输入关键字即可使用。

| 命令名称 | 什么时候用 | 它背后做了什么 |
|----------|------------|----------------|
| **Starter Kit: 选择设备串口** | 第一次连接或更换开发板时 | 扫描电脑串口，调用 Python 里的 `serial.tools.list_ports` 列表，再用 `mpremote` 尝试读取板子信息，最后记住选择结果。 |
| **Starter Kit: 烧录 Starter Kit 固件** | 想刷写 `.bin` 固件时 | 打开文件对话框让你选固件 → 调用 `esptool` 刷写 → 在“输出”面板显示进度。 |
| **Starter Kit: 打开控制面板** | 想用图形界面执行常用任务 | 打开扩展自带的 Webview 面板，通过按钮调用串口选择、烧录、上传等命令，避免频繁打开命令面板。|
| **Starter Kit: Upload Files/Folders to Device** | 想上传项目目录到板子 | 让你多选目录或文件 → 计算公共根目录 → 逐级在板子上创建目录 → 使用 `mpremote fs cp` 逐项复制。 |
| **Starter Kit: 上传文件到设备** | 只想上传当前编辑中的 Python 文件 | 确认你已打开一个 `.py` 文件 → 用 `mpremote cp` 把它复制到板子 `/` 根目录。 |
| **Starter Kit: 运行设备上的文件** | 想在板上执行已经上传的脚本 | 读取当前编辑文件名 → 调用 `mpremote run <文件名>`。 |
| **Starter Kit: Run Example Project** | 想快速验证板子是否正常工作 | 把扩展自带示例目录复制到板子 → 执行 `machine.reset()` 重启板子。 |

所有命令都会在 VS Code 左下角的状态栏显示当前串口；命令运行失败时，会弹出错误提示。

---

## 5. 项目目录导览

```
mp-lvgl-starterkit/
├── src/
│   ├── extension.ts         # VS Code 的主入口，负责注册命令与状态栏
│   ├── services/
│   │   └── starter.ts        # 串口选择、烧录、上传等核心流程
│   ├── tools/
│   │   ├── mpremote.ts       # 对 mpremote 的封装：列设备、复制文件等
│   │   └── esptool.ts        # 对 esptool 的封装：刷固件、显示输出
│   └── utils/
│       └── logger.ts         # 输出面板与 JSONL 日志
├── bin/win/                 # 打包好的 Windows 版 mpremote.exe、esptool.exe
├── example/basic/           # 运行示例用的 MicroPython 工程
├── docs/beginner-guide.md   # （本文档）
└── package.json             # 扩展元数据、命令注册、脚本
```

> 如果你使用 macOS 或 Linux，目前需要自备 `mpremote` 和 `esptool`，未来可在这里扩展多平台支持。

---

## 6. 工作流程拆解

下面逐步解释主要类型脚本在做什么，帮助你在需要时定位问题。

### 6.1 `src/extension.ts`

- 激活扩展时，先调用 `gcOldLogs(7)` 清理 7 天前的日志。
- 创建左下角的状态栏按钮，默认文案是 `Starter Kit: No device selected`。
- 从 `workspaceState` 里读取最近一次成功选择的串口，若仍然存在就直接显示。
- 注册所有命令，命令的共性是：
  1. 调用 `ensurePort()`，确认有可用串口（必要时弹框让你选）；
  2. 调用 `services/starter.ts` 里对应的函数完成实际工作；
  3. 捕获异常并用 `showErrorMessage` 告知用户。

### 6.2 `src/services/starter.ts`

- **串口识别**：
  - `listPortsWithMeta()` 通过 Python 的 `serial.tools.list_ports` 获取端口、厂商等信息。
  - `probeViaMpremote()` 运行 `mpremote connect ... exec`，尝试读取 `os.uname()` 判断固件与芯片类型。
  - `usbHint()` 用 VID/PID 提示可能的芯片厂商。
  - `pickPortOrThrow()` 综合以上步骤，让你选端口并缓存到 `workspaceState`。

- **日志与路径**：
  - `normalizeRelative()` 防止 Windows 相对路径带盘符导致 `mpremote` 报错。
  - `commonAncestor()` 找出多个文件/目录的公共父目录。

- **上传流程**（`doSyncWorkspace`）：
  1. `pickLocalEntries()` 通过文件对话框让你多选条目（Windows 下仅能选目录时，可结合“上传当前文件”命令使用）。
  2. 计算每个条目相对公共父目录的路径，并转换成 POSIX 形式。
  3. 目录：先确保设备上存在对应父目录，再调用 `copyDirectory()` 递归复制。
  4. 文件：按需创建父目录，然后 `copyFileTo()` 覆盖同名文件。
  5. 最后给出提示，并记录日志 `upload_selection`。

- **其他命令**：`doFlash`、`doRunExample`、`doUploadFile`、`doRunFile` 分别对应烧录、示例、单文件上传、运行文件。

### 6.3 `src/tools/mpremote.ts`

- `execMpremote()` 是统一的运行函数，封装了超时、错误提示。
- `ensureRemoteDirectories()` 用 `mpremote fs mkdir :/path` 逐级创建文件夹。
- `copyDirectory()`、`copyFileTo()` 则用 `mpremote fs cp -r` 和 `mpremote cp` 完成复制。
- `runFile()` 现在直接接受文件的绝对路径，确保 `mpremote` 能读取本地脚本内容。
- 所有路径调用前都会把 Windows 反斜杠替换成 POSIX `/`，并统一加上 `:/` 前缀，这是 mpremote 的路径规则。

### 6.4 `src/tools/esptool.ts`

- `writeFlash()` 会多次尝试不同波特率刷写固件，实时把输出写入 VS Code 的“Starter Kit”面板，方便观察进度。
- 遇到常见错误（如 `Stub flasher JSON file ... not found`）会自动切换参数重试。

### 6.5 `src/utils/logger.ts`

- 创建 `Starter Kit` 输出面板，用于实时显示命令进度。
- 把所有操作写进 `~/.mpkit/logs/<串口>.jsonl`，每行一条 JSON 记录，便于 debug。
- `gcOldLogs(days)` 会自动删除过期日志，避免占满磁盘。

---

## 7. 常见问题与排查

| 提示信息 | 可能原因 | 解决思路 |
|----------|----------|-----------|
| `No active editor.` | 你在没有打开文件的情况下执行了“上传文件到设备”命令 | 先打开要上传的 `.py` 文件再执行，或改用“Upload Files/Folders to Device”。 |
| `Permission denied` | 板子处在只读模式、空间不足、或目标路径无效 | 确认板子未处于安全模式；手动运行 `mpremote connect <port> fs cp` 看具体报错；必要时删除旧文件或重新烧录固件。 |
| `No serial port detected` | 数据线、驱动、或权限问题 | 换线、装驱动、确认 USB 接口；macOS/Linux 可用 `ls /dev/tty.*` 手动确认。 |
| `Failed to connect`（刷固件时） | 板子未进入下载模式或端口被占用 | 按住 BOOT、点一下 RST 再放开；关闭占用串口的程序。 |

> 建议：在“输出”面板（视图 → 输出 → Starter Kit）以及 `~/.mpkit/logs` 查找更详细的错误信息。

---

## 8. 工作流示例

1. **第一次使用**
   - 打开 VS Code，连接 ESP32 → 执行 “Starter Kit: 选择设备串口” → 成功后状态栏显示 `Starter Kit: COMx`。
2. **烧录固件**
   - 执行 “Starter Kit: 烧录 Starter Kit 固件” → 选择 `.bin` 文件 → 等待输出面板显示成功提示。
3. **上传项目**
   - 执行 “Starter Kit: Upload Files/Folders to Device” → 在对话框中勾选需要的目录 → 扩展会在日志中记录上传列表。
4. **调试单个脚本**
   - 打开 `main.py` → 修改后保存 → 执行 “Starter Kit: 上传文件到设备” → 如需立即运行，再执行 “Starter Kit: 运行设备上的文件”。
5. **实时交互**
   - 执行 “Starter Kit: 打开 REPL 终端” 或在控制面板点击对应按钮 → VS Code 会弹出一个与板子连接的终端窗口，可直接查看输出与键入命令。
   - 如果打开了 REPL 终端，串口会被占用；执行烧录/上传/同步等命令时，扩展会提示先关闭 REPL，可在控制面板或命令面板运行 “Starter Kit: 关闭 REPL 终端”。

---

## 9. 常用扩展配置

当前版本没有暴露 VS Code 设置项，所有行为都写死在代码中。如果你希望自定义例如“上传时的忽略规则”或“默认固件路径”，可以在 `src/services/starter.ts` 中改动相关常量，或向项目提交 Issue/PR。

---

## 10. 术语表

- **板子 / 设备**：指 ESP32 开发板。
- **烧录**：把固件写入板子的 Flash。
- **串口**：电脑与板子通讯的接口。
- **固件**：运行在板子上的底层程序。
- **脚本**：这里指 MicroPython `.py` 文件。
- **工作区**：VS Code 打开的项目目录。
- **日志 (log)**：记录操作过程的文件，位于 `~/.mpkit/logs`。

---

## 11. 下一步可以做什么？

- 想了解更多命令细节，可阅读 `src/services/starter.ts` 中对应函数，本文已注明关键流程。
- 若想扩展到 macOS/Linux，可在 `src/tools/paths.ts` 添加不同平台的二进制路径引用。
- 欢迎把常见问题或改进建议整理后更新本指南，让后续的新手更快上手。

祝你玩得愉快！
---

## 12. 文件管理面板

安装新版扩展后，活动栏会出现 “Starter Kit” 视图，其中包含两个树：本地文件 和 设备文件。你可以：

- 在 本地文件 树里浏览当前工作区；
- 将文件或文件夹拖拽到 设备文件 树的任意目录，扩展会使用 mpremote 自动上传；
- 右键树视图标题选择“刷新”同步最新目录；
- 结合命令面板的上传/运行命令完成快速调试。

> 拖拽上传依赖当前串口选择，必要时先执行 “Starter Kit: 选择设备串口”。
