# SpektraLab Windows 便携版

这是非官方 Windows 社区测试版。完整解压本文件夹后，双击 `spektralab.exe`；`host` 和 `agents` 文件夹必须与 EXE 放在一起。需要 Windows x64、支持 Vulkan 的显卡驱动及 Microsoft Edge WebView2 Runtime。

照片编辑记录默认保存在当前 Windows 用户的应用数据目录，而不是便携目录。程序不覆盖原始 RAW；导出时请检查输出目录和文件名。

CLI/MCP 默认关闭。需要时在软件 Settings → Agents 打开访问，查看软件提供的配置；`spektralab-cli.cmd help` 可查看命令。移动程序目录后，应重新安装软件提供的 CLI 包装器。

本程序未签名。版本、源码、校验值和完整说明：<https://github.com/huof2034/SpektraLab-Windows/releases/tag/v1.3.1-windows.1>。应用采用 GPL-3.0-or-later，胶片/相纸配置和 LUT 数据采用 CC BY-SA 4.0，具体许可与署名见 `COPYING`、`THIRD_PARTY_NOTICES.md` 和 `host/licenses/`。
