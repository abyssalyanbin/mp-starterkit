# LVGL Starter Kit for VS Code

> 一键点亮你的 ESP32 + LVGL 屏幕。  
> 让 MicroPython 开发体验更像桌面 IDE。

---

## 功能概述

LVGL Starter Kit 是一个专为 **ESP32 + LVGL 显示屏** 设计的 VS Code 扩展，  
帮助你快速完成从烧录固件到运行 Demo 的全流程：

-  **设备识别与端口选择** — 自动列出串口设备，一键连接。
-  **一键烧录固件** — 内置编译好的 ESP32-S3 + MicroPython + LVGL 固件。
-  **运行示例** — 内置多个基础示例（文字 / 按钮 / 图片）。
-  **串口 REPL 控制台** — 支持命令交互与调试输出高亮。
-  **暂时仅支持Windows** 

---

##  安装说明

1. 从 [VS Code Marketplace](https://marketplace.visualstudio.com/) 搜索并安装 **“LVGL Starter Kit”**。  
2. 或者手动安装：
   ```bash
   npx vsce package
   code --install-extension lvgl-starterkit-x.y.z.vsix


## 🧭 未点亮排查指南

若运行示例后屏幕未显示，请按以下步骤排查：

1. **检查连接**  
   - 重新插拔 USB 数据线，确认设备管理器中出现 COM 端口。  
   - 若无端口，请安装对应驱动（CH340 / CP210x）。  

2. **检查固件**  
   - 在控制面板点击 “烧录默认固件”，等待进度完成。  
   - 若烧录失败，请按住开发板的 BOOT 键重试。  

3. **检查文件同步**  
   - 在控制台查看是否有 `fs cp` 成功日志。  
   - 若提示空间不足，可先执行 “清空设备文件系统”。  

4. **检查屏幕接线**  
   - 对照示例中的 `pin_config.py` 检查引脚定义。  
   - 确保屏幕供电正常（3.3V / 5V）。  

5. **检查 LVGL 是否初始化**  
   - 打开 REPL，手动输入：  
     ```python
     import lvgl; lvgl.init()
     ```  
     若提示 `No module named lvgl`，说明固件版本不对，请重新烧录内置固件。

---

## ❓ 常见问题（FAQ）

**Q1. 未识别到串口**  
→ 请确认安装了串口驱动，如CH340。

**Q2. 烧录失败或超时**
→ 确认已按住 BOOT 键进入下载模式，或尝试更换数据线。

**Q3. 控制面板打不开**
→ 请更新 VS Code 至 1.90 以上，或运行命令：
LVGL Starter Kit: 打开控制面板

**Q4. 屏幕白屏但串口无报错**
→ 检查屏幕型号和引脚定义是否匹配 Demo 示例。
---



## 💡 反馈与建议

我们非常希望了解你希望这个扩展未来支持的功能，比如：

- 新的 **屏幕型号**（如 ILI9341 / GC9A01 / SSD1306 / ST7735 等）  
- 不同的 **LVGL 版本**（例如 8.x、9.x）  
- 更多的 **示例场景**（动画、触摸、UI 组件、图片显示等）  
- 或任何使用过程中的问题与想法  

请通过以下方式告诉我们你的建议：

- 在 [GitHub Issues](https://github.com/abyssalyanbin/mp-lvgl-starterkit/issues) 中选择 “Feature request” 模板提交；

每条反馈都会被阅读，并在下一版开发计划中优先考虑。  
社区共建让这个 Starter Kit 更强大！ 



