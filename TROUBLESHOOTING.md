# 故障排查（Troubleshooting）

## `zsh: command not found: dsh-gui`

### 现象

在任意目录下直接运行 `dsh-gui`，shell 报错：

```sh
zsh: command not found: dsh-gui
```

即使已经 `cd` 到仓库目录（例如 `~/Desktop/LLM/harness/dsh-gui_edge`），也可能出现这个错误。

### 原因

shell 只在 `PATH` 列出的目录里查找命令，**不会在当前目录里找**。脚本 `dsh-gui` 位于仓库目录，而仓库目录不在 `PATH` 中，因此：

1. 如果 `~/.local/bin`（或其他 `PATH` 目录）里没有指向它的链接，直接敲 `dsh-gui` 就找不到命令；
2. 即使 `~/.zshrc` 已经把 `~/.local/bin` 加入了 `PATH`，只要链接没建，命令同样找不到。

### 解决方法

**方法一：建立软链接（推荐，README 中的安装方式）**

```sh
cd ~/Desktop/LLM/harness/dsh-gui_edge   # 换成你的实际仓库路径
ln -s "$PWD/dsh-gui" ~/.local/bin/dsh-gui
```

链接指向源文件本身，以后修改脚本会立即生效，无需重装。

**方法二：暂时用相对路径运行**

```sh
./dsh-gui
```

只对当前会话方便，不适合长期使用。

### 如果建好链接后仍然报错

1. 确认 `~/.local/bin` 在 `PATH` 里：

   ```sh
   echo "$PATH" | tr ':' '\n' | grep "\.local/bin"
   ```

   没有输出的话，把下面这行加到 `~/.zshrc`（或 `~/.bashrc`）：

   ```sh
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. 刷新当前终端的命令缓存（或直接新开一个终端窗口）：

   ```sh
   hash -r      # zsh/bash 均可
   # 或
   exec zsh     # 重新加载 zsh 配置
   ```

3. 验证：

   ```sh
   command -v dsh-gui   # 应输出 /Users/<你>/.local/bin/dsh-gui
   dsh-gui help         # 应输出帮助信息
   ```

### 本次实际处理记录（2026-08-25）

- 环境：macOS + zsh；`~/.zshrc` 已含 `export PATH="$HOME/.local/bin:$PATH"`。
- 但 `~/.local/bin` 中没有 `dsh-gui` 链接，所以报 `command not found`。
- 处理：执行 `ln -sfn "$PWD/dsh-gui" ~/.local/bin/dsh-gui`，随后 `command -v dsh-gui` 与 `dsh-gui help` 均正常。

---

## 将 Harness 安装为 Edge 应用（How-to）

用 dsh-gui 把 Harness 配置跑起来之后，可以再把它「包装」成 Edge 应用：获得独立的 Dock 图标、独立窗口和 Cmd-Tab 切换项。装好之后 dsh-gui 会自动优先打开这个已安装的应用。

### 前置条件

- `dsh web` 服务正在运行（先执行一次 `dsh-gui`，或已有 launchd 自启保活）；
- 在 Edge 的**普通标签页**里操作。注意：dsh-gui 打开的是无地址栏的 `--app` 窗口，那个窗口的 `⋯` 菜单是精简版，**没有**「应用」选项，必须回到普通标签页。

### 步骤

1. 在 Edge 地址栏打开 `http://127.0.0.1:3080`（使用 `--port` 时换成对应端口）。
2. 点击右上角 `⋯`（设置及更多）按钮。
3. 找到「应用」入口。不同版本的 Edge 位置略有差异：
   - 实测路径：`⋯` → **更多工具** → **应用**；
   - 部分版本：`⋯` 菜单里直接就有 **应用**；
   - 英文界面为 *More tools* → *Apps*。
4. 点击 **「将此站点作为应用安装」**（*Install this site as an app*）。
5. 在弹窗中命名（如 `DeepSeek Harness`），点击 **安装**。

备用方法：在地址栏输入 `edge://apps` 回车，页面右上角有 **「安装应用」** 按钮，按提示操作即可。

### 验证

- 应用出现在 `~/Applications/Edge Apps.localized/DeepSeek Harness.app`；
- 运行 `./dsh-gui`，输出应为 `dsh-gui: opened DeepSeek Harness`（说明已走「打开已安装应用」分支，而非临时 `--app` 窗口）。

### 注意事项

- 安装的应用与 URL 精确绑定（含端口）：默认是 `http://127.0.0.1:3080`；使用 `--port 8080` 时需要为 8080 另装一个应用。
- 若 `dsh web` 由 launchd 自启保活（本机为 `~/Library/LaunchAgents/com.deepseek.dsh.plist`，`RunAtLoad` + `KeepAlive`），安装后可直接从 Dock / 启动台打开应用，日常无需再运行 dsh-gui；但远程隧道、进程管理、服务兜底启动等能力仍需要 dsh-gui。
