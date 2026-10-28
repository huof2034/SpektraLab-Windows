# Windows x64 源码构建

本仓库基于上游 `97b9b2243217036c5ea8eef2951147b0e39f0cf9` 的源码快照。社区发行改动包括公开文档与许可汇总、关闭本副本上的上游 CI 自动触发、将 NSIS 改为当前用户安装，以及要求发布构建的 mock host 显式指定脚本路径，避免把构建者的路径嵌入二进制。上游原始构建流程见 `engine/LINUX_WINDOWS.md` 和 `desktop/AGENTS-CLI.md`。

本机使用 Windows x64、MinGW-w64 GCC 13.1（POSIX/SEH）、MSVC 19.44、Windows SDK、CMake 3.31.6、glslang 16.2.0、Python 3.12、Meson 1.9.2、Ninja 1.13、Rust 1.99.1 和 Node.js 24.19.0。安装器打包脚本要求 Node 24.19.0。需要 Git Bash、Vulkan-Headers、Vulkan 驱动和 nasm；编译工具版本与路径可按上游说明调整。

准备依赖（在仓库根目录）：

1. 创建独立依赖目录，例如 `build/deps`，将匹配版本的 MinGW、CMake、glslang、Python 和 Rust 加入当前终端 PATH。安装 Python 模块 `meson==1.9.2` 和 `ninja==1.13.0`。
2. 将 Releases 的 `SpektraLab-Windows-1.3.1-dependency-sources.zip` 解压并核对其中 `SHA256SUMS.txt`。归档是第三方源码存档；上游设置脚本仍可能联网获取其固定的 Git 仓库和软件包。
3. 按 `engine/setup-deps.sh` 的固定提交获取 Vulkan-Headers，按 `engine/setup-libraw.ps1 -DependencyDirectory <依赖目录>` 获取 LibRaw；按 `engine/setup-codecs.ps1 -DependencyDirectory <依赖目录>/export-codecs` 获取导出编解码器。所有下载应通过脚本中的固定哈希检查。
4. 分别运行 `engine/setup-input-codecs.py` 和 `engine/setup-lens-codecs.py`，以 `MinGW Makefiles` 生成器构建对应依赖，安装到 `<依赖目录>/input-codecs/install` 和 `<依赖目录>/lens-codecs/install`。具体参数参考 `engine/LINUX_WINDOWS.md`。

公开发行构建还应在编译所有 C/C++ 目标时设置 `-ffile-prefix-map=<本机构建路径>=/build`，并给 Rust 设置 `--remap-path-prefix=<本机构建路径>=/build`，避免将开发者路径嵌入二进制。Windows 静态 GLib 使用 `GLIB_LOCALE_DIR` 的最后 `/share/locale` 部分计算运行时相对路径；可对其 Meson 生成的 `config.h` 运行 `python engine/tools/sanitize_glib_locale.py <config.h>`，然后重新编译并安装 GLib，以保留这个后缀并移除构建前缀。构建完成后检查可执行文件是否仍含私有路径。

使用新建构建目录配置本机 CMake；按实际路径替换下面占位项：

```powershell
cmake -S . -B build/windows -G 'MinGW Makefiles' `
  -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=ON `
  -DSPEKTRALAB_REQUIRE_VULKAN=ON -DSPEKTRALAB_BUILD_NATIVE_RAW=ON `
  -DSPEKTRALAB_BUILD_DESKTOP=OFF -DSPEKTRALAB_BUILD_HOST=ON `
  -DSPEKTRALAB_STATIC_RUNTIME=ON `
  -DSPEKTRALAB_DEPS_DIR='<依赖目录>' `
  -DSPEKTRALAB_LIBRAW_SOURCE='<依赖目录>/LibRaw-0.22.2' `
  -DSPEKTRALAB_VULKAN_HEADERS='<依赖目录>/Vulkan-Headers/include' `
  -DSPEKTRALAB_GLSLANG='<glslang可执行文件路径>' `
  -DSPEKTRALAB_INPUT_CODEC_PREFIX='<依赖目录>/input-codecs/install' `
  -DSPEKTRALAB_LENS_PREFIX='<依赖目录>/lens-codecs/install' `
  -DSPEKTRALAB_CODECS_DIR='<依赖目录>/export-codecs'
cmake --build build/windows --parallel 8
ctest --test-dir build/windows --output-on-failure
```

用 Git Bash 调用 `engine/stage-host.sh build/windows build/host-win-x64 spektralab-host.exe`，并设置 `SPEKTRALAB_DEPS_DIR` 为依赖目录；目标暂存目录必须专供本次构建。接着在 `desktop/` 下运行 `npm ci`、`npm run check`、`npm run build:agent`、`npm run build:web` 和 `node scripts/package.mjs win`。后者将本地 host、资源、许可和精确版本的 Node 运行时打包。

打包后应在新的隔离目录验证安装器、Vulkan host、RAW 解码、MCP 与导出；不要将用户照片、编辑数据库、日志、凭据或构建缓存加入发行包。源代码与静态链接依赖的来源和许可见 `THIRD_PARTY_NOTICES.md`。
