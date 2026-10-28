# SpektraLab Windows 社区构建

基于开源 SpektraLab Windows 移植代码构建的胶片与相纸模拟软件，支持导入照片、调整胶片和冲印参数、预览与导出，也提供可选的 CLI 和 MCP 接口。

> **非官方实验版。** 本项目不是 SpektraLab 官方 Windows 正式发行版，也不代表上游作者对本仓库或安装包的认可。Windows 移植仍在开发，功能及画面结果不保证与 macOS 版完全一致。

## 下载和安装

前往 [Windows 社区测试版下载页](https://github.com/huof2034/SpektraLab-Windows/releases/tag/v1.3.1-windows.1)：

- **安装版**：下载 `SpektraLab-Windows-1.3.1-setup.exe`，运行后按提示选择安装目录。安装到当前用户，无需为应用本身安装 Python、Node.js 或 Vulkan SDK。
- **便携版**：下载 `SpektraLab-Windows-1.3.1-portable.zip`，完整解压到一个文件夹，运行其中的 `spektralab.exe`。不要只复制单个 EXE；旁边的 `agents` 和 `host` 目录是运行所需文件。
- **源码和构建依赖**：下载带版本号的源码 ZIP 与依赖源码 ZIP；各文件的 SHA-256 见 `SHA256SUMS.txt`。

Windows x64 需要可用的 Vulkan 显卡驱动与 Microsoft Edge WebView2 Runtime。安装器在缺少 WebView2 时会尝试下载微软组件；便携版需要系统已有该组件。建议使用 Windows 10/11 x64；目前本仓库的实际照片测试仅覆盖 Windows 11、NVIDIA RTX 5070 Laptop，其他 GPU 和 Windows 版本有待验证。

安装包和便携版 **没有数字签名**，Windows 可能显示未知发布者提示。请从本仓库 Releases 下载并核对 SHA-256。不要关闭系统安全防护。

## 快速使用

1. 打开软件，导入受支持的 RAW 或图像文件。
2. 选择胶片和相纸，例如 Kodak Portra 400 与 Kodak Portra Endura，执行 Process/配光。
3. 调整曝光、白平衡及其他可用参数，确认预览。
4. 导出照片。需要 sRGB JPEG 时，在导出界面选择或创建对应的 JPEG/sRGB 配方；默认 JPEG 配方可能为 Display P3。

导出前确认输出目录与命名规则，建议先使用原图副本。相机 RAW 支持取决于 LibRaw 和文件编码，例如 Nikon HE/HE* 并非均受支持。

## 可选：CLI 和 Codex MCP

软件的 **Settings → Agents** 默认关闭。启用后，设置页面可以安装 `spektralab` 命令并显示实际的 MCP 命令；移动便携文件夹后需要重新安装该命令。便携版根目录也提供 `spektralab-cli.cmd`，可直接用于 `help` 和 `status`。

Codex 使用 `~/.codex/config.toml`，在备份现有文件后追加如下结构，并把路径替换为设置页面显示的实际安装路径：

```toml
[mcp_servers.spektralab]
command = 'C:\实际安装目录\agents\node.exe'
args = ['C:\实际安装目录\agents\agent.mjs', 'mcp']
enabled = true
startup_timeout_sec = 20
tool_timeout_sec = 300
default_tools_approval_mode = 'prompt'
```

重启 Codex，先运行 `codex mcp list`，再实际调用 `list_stocks`；注册成功不等于连接和调用成功。关闭软件 Agents 开关可阻止之后的工具调用。工具包含 `get_schema`、`list_stocks`、`list_recipes`、`describe_image`、`get_edit`、`edit_image`、`reset_edit`、`process_image`、`measure_latitude`、`place_scene`、`preview_image` 和 `export_image`，以软件实际返回结果为准。详见 [CLI/MCP 上游说明](desktop/AGENTS-CLI.md)。

示例提示词：

> 使用 SpektraLab 将这张照片处理成 Kodak Portra 400 的自然胶片风格，适当调整曝光和白平衡，先展示预览，再导出高质量 sRGB JPEG，不要覆盖原始照片。

## 本次验证与限制

基于上游提交 `97b9b2243217036c5ea8eef2951147b0e39f0cf9`。本机 Windows 11 / RTX 5070 Laptop：原生 CTest 40/40，前端单元 341 通过、1 跳过，Rust 23 通过、1 忽略，浏览器模拟测试 37/37。使用 CC0 Sony ARW 副本，经隔离测试配置的真实 MCP 完成 Portra 400、Portra Endura、曝光和白平衡调整及 sRGB JPEG 导出，结果为 3880×2608，源文件哈希未改变。

以上测试不代表所有相机、GPU、显示器和设置组合均已验证；macOS/Metal 的整图像素一致性、HDR 及广色域显示尚未完成本机验证。最终安装包和便携包的额外验证范围以 [发布说明](RELEASE_NOTES.md) 为准。

## 来源与许可

本项目继承 [JamesQiu2005/SpektraLab](https://github.com/JamesQiu2005/SpektraLab) 的 Windows 移植草稿 [PR #14](https://github.com/JamesQiu2005/SpektraLab/pull/14)，其胶片模型源自 [andreavolpato/spektrafilm](https://github.com/andreavolpato/spektrafilm)。感谢所有原作者和贡献者。

软件代码为 **GPL-3.0-or-later**；胶片/相纸配置及 LUT 数据为 **CC BY-SA 4.0**，其他第三方组件各有许可。完整条款、来源和构建说明见 [COPYING](COPYING)、[第三方声明](THIRD_PARTY_NOTICES.md)、[上游 README](README.upstream.md) 和 [Windows 构建指南](WINDOWS_BUILD.md)。
