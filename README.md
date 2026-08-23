# dsh-gui

A small POSIX-shell helper for macOS that manages the [DeepSeek Harness](https://www.npmjs.com/package/@deepseek-ai/dsh) web GUI: it starts the `dsh web` service when needed, opens the *DeepSeek Harness* Chrome app, and can tunnel to remote instances over SSH.

## Requirements

- macOS (`open`, `defaults`, `lsof`)
- `curl`, `ssh`
- DeepSeek Harness, launchable as `dsh` on `PATH` or via `npx` (`@deepseek-ai/dsh`)
- Google Chrome (for app windows and/or the installed *DeepSeek Harness* Chrome app)

## Installation

```sh
git clone git@github.com:jyshangguan/dsh-gui.git
ln -s "$PWD/dsh-gui/dsh-gui" ~/.local/bin/dsh-gui   # any directory on your PATH works
```

## Usage

| Command | Effect |
| --- | --- |
| `dsh-gui` | start `dsh web` if it is not running (default port 3080), then open the Chrome app |
| `dsh-gui --port 8080` | same, but use/check a non-default local port |
| `dsh-gui --remote sgdesk --port 8080` | tunnel local `8080` → `127.0.0.1:8080` on `sgdesk` via `ssh -o ExitOnForwardFailure=yes -N -L …`, wait until it serves HTTP, then open the app on it |
| `dsh-gui --remote user@host` | same, with an explicit remote user (default: `$USER`) |
| `dsh-gui ps` | list running dsh processes and dsh-gui ssh tunnels |
| `dsh-gui kill` | list them, then interactively pick what to kill (PID / `all` / quit) |
| `dsh-gui kill all` | kill every listed process (asks for confirmation) |
| `dsh-gui kill PID...` | kill the given PID(s) |
| `dsh-gui help` | show help |

Unknown flags are forwarded to `dsh web` on a cold start (e.g. `dsh-gui --host 127.0.0.1`).

### Behavior notes

- **Service**: started in the background with `nohup`; log goes to `~/.dsh/dsh-web.log`.
- **Tunnels**: log goes to `~/.dsh/dsh-tunnel-<target>.log`. If the local port already has a listener, a matching existing tunnel is *reused*; any other listener is reported and the script refuses to shadow it.
- **App window**: Chrome ties an app's identity to a single URL. dsh-gui scans the installed Chrome apps (`Chrome Apps.localized`) for one whose URL matches the target and opens it (this is how the *DeepSeek Harness* app opens for the local URL). Any other URL — e.g. a remote/tunneled one — opens as a Chrome `--app` window (borderless, no separate app registration). If you ever install such a URL as a Chrome app manually, dsh-gui will prefer the installed app automatically.
- **Killing**: sends `SIGTERM`, waits up to 5 s, then escalates to `SIGKILL`. Killing the process that serves the GUI port disconnects any live session on it; the script warns before doing so.

## Environment variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `DSH_CMD` | `dsh` if on `PATH`, else `npx -y @deepseek-ai/dsh` | command that launches dsh |
| `DSH_GUI_PORT` | `3080` | listen port to use/check |
| `DSH_GUI_TIMEOUT` | `60` | seconds to wait for the service/tunnel to come up |
| `DSH_PROC_PATTERN` | built-in | ERE matching dsh process command lines |
| `DSH_TUNNEL_PATTERN` | built-in | ERE matching dsh-gui ssh tunnels |
| `DSH_HOME` | `~/.dsh` | where log files are written |

## License

[MIT](LICENSE)
