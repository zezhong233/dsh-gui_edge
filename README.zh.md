# dsh-gui

一个用于 macOS 的 POSIX shell 小工具，用来管理 [DeepSeek Harness](https://www.npmjs.com/package/@deepseek-ai/dsh) 的 Web 界面：按需启动 `dsh web` 服务、打开 *DeepSeek Harness* Chrome 应用，并支持通过 SSH 隧道连接远程实例。

## 依赖

- macOS（使用 `open`、`defaults`、`lsof`）
- `curl`、`ssh`
- DeepSeek Harness：`PATH` 中有 `dsh` 命令，或可通过 `npx` 运行（`@deepseek-ai/dsh`）
- Google Chrome（用于应用窗口和/或已安装的 *DeepSeek Harness* Chrome 应用）

## 安装

```sh
git clone git@github.com:jyshangguan/dsh-gui.git
ln -s "$PWD/dsh-gui/dsh-gui" ~/.local/bin/dsh-gui   # 任何在 PATH 中的目录均可
```

## 用法

| 命令 | 作用 |
| --- | --- |
| `dsh-gui` | 若 `dsh web` 未运行则启动（默认端口 3080），然后打开 Chrome 应用 |
| `dsh-gui --port 8080` | 同上，但使用/检查非默认本地端口 |
| `dsh-gui --remote sgdesk --port 8080` | 通过 `ssh -o ExitOnForwardFailure=yes -N -L …` 把本地 `8080` 隧道到 `sgdesk` 的 `127.0.0.1:8080`，等待 HTTP 就绪后打开应用 |
| `dsh-gui --remote user@host` | 同上，显式指定远程用户（默认：`$USER`） |
| `dsh-gui ps` | 列出正在运行的 dsh 进程和 dsh-gui 的 ssh 隧道 |
| `dsh-gui kill` | 列出后交互式选择要结束的进程（PID / `all` / 退出） |
| `dsh-gui kill all` | 结束全部列出的进程（需确认） |
| `dsh-gui kill PID...` | 结束指定 PID |
| `dsh-gui help` | 显示帮助 |

无法识别的参数会在冷启动时转发给 `dsh web`（例如 `dsh-gui --host 127.0.0.1`）。

### 行为说明

- **服务**：以 `nohup` 后台启动，日志写入 `~/.dsh/dsh-web.log`。
- **隧道**：日志写入 `~/.dsh/dsh-tunnel-<target>.log`。若本地端口已有监听：匹配的已有隧道会被*复用*；其他占用者会被提示，脚本拒绝覆盖。
- **应用窗口**：已安装的 *DeepSeek Harness* Chrome 应用内置的 URL 从其 `Info.plist`（`CrAppModeShortcutURL`）读取。URL 完全一致时打开该应用本身；其他 URL（不同端口、远程实例）以 Chrome `--app` 窗口打开——同样是沉浸式窗口体验。
- **结束进程**：先发 `SIGTERM`，最多等 5 秒，仍存活则升级为 `SIGKILL`。结束正在服务 GUI 端口的进程会断开其上的活动会话，脚本会事先警告。

## 环境变量

| 变量 | 默认值 | 含义 |
| --- | --- | --- |
| `DSH_CMD` | `PATH` 中有 `dsh` 则用之，否则 `npx -y @deepseek-ai/dsh` | 启动 dsh 的命令 |
| `DSH_GUI_PORT` | `3080` | 使用/检查的监听端口 |
| `DSH_GUI_TIMEOUT` | `60` | 等待服务/隧道就绪的秒数 |
| `DSH_PROC_PATTERN` | 内置 | 匹配 dsh 进程命令行的 ERE |
| `DSH_TUNNEL_PATTERN` | 内置 | 匹配 dsh-gui ssh 隧道的 ERE |
| `DSH_HOME` | `~/.dsh` | 日志文件写入位置 |

## 许可证

[MIT](LICENSE)
