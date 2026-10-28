# 版权、来源与第三方组件

这是独立发布的社区构建，与上游项目没有隶属或官方认证关系。本仓库保留上游代码、资源、版权声明和许可文本。不要移除胶片配置、LUT、镜头数据库或字体的署名和许可。

- SpektraLab 应用和引擎：GPL-3.0-or-later；原始许可位于 `COPYING` 与 `license/`。
- Andrea Volpato 的 spektrafilm 模型、胶片及相纸配置、LUT：胶片和相纸数据及 LUT 采用 CC BY-SA 4.0；版权和变更记录见 `licenses-windows/Profiles-and-LUTs-*` 和上游文件。
- SpektraLab B&W 产品材料与印字字体：见 `licenses-windows/Product-profiles-NOTICE.md`、`Imprint-fonts-LICENSE.txt` 和各资源目录中的声明。
- LibRaw、libheif、libde265、GLib、Lensfun 与其校准数据库，以及各自的依赖：见 `licenses-windows/` 及固定源码包。适用 LGPL、GPL、CC BY-SA 或相应许可，具体以各组件文本为准。
- Vulkan-Headers、volk、stb、OpenEXR、Imath、LittleCMS、libjpeg-turbo、libpng、zlib-ng、PCRE2、libffi、proxy-libintl 和 Node.js：见 `licenses-windows/`、`engine/third_party/`、依赖源码和其自身许可。
- Microsoft Edge WebView2 Runtime 由 Microsoft 提供，其下载和使用受 Microsoft 条款约束；本仓库不将该运行时声称为本项目所有。

源代码对应上游 SpektraLab 提交 `97b9b2243217036c5ea8eef2951147b0e39f0cf9`。本社区版本的改动和构建信息记录在仓库提交、[Windows 构建指南](WINDOWS_BUILD.md)和 [发布说明](RELEASE_NOTES.md)。发行二进制所用的固定第三方源码可从本仓库版本附件取得；上游 URL、版本与校验值也保留在 `engine/` 的依赖清单及设置脚本中。
