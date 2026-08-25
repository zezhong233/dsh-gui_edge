# dsh-gui

A small POSIX-shell helper for macOS that manages the [DeepSeek Harness](https://www.npmjs.com/package/@deepseek-ai/dsh) web GUI: it starts the `dsh web` service when needed, opens the *DeepSeek Harness* app window in Microsoft Edge, and can tunnel to remote instances over SSH.

## Requirements

- macOS (`open`, `defaults`, `lsof`)
- `curl`, `ssh`
- DeepSeek Harness, launchable as `dsh` on `PATH` or via `npx` (`@deepseek-ai/dsh`)
- Microsoft Edge (for app windows and/or the installed *DeepSeek Harness* Edge app)

## Installation

```sh
git clone git@github.com:jyshangguan/dsh-gui.git
ln -s "$PWD/dsh-gui/dsh-gui" ~/.local/bin/dsh-gui   # any directory on your PATH works
```

## Usage

| Command | Effect |
| --- | --- |
| `dsh-gui` | start `dsh web` if it is not running (default port 3080), then open the app window |
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
- **App window**: Edge ties an app's identity to a single URL. dsh-gui scans the installed Edge apps (`Edge Apps.localized`) for one whose URL matches the target and opens it (this is how the *DeepSeek Harness* app opens for the local URL). Any other URL — e.g. a remote/tunneled one — opens as an Edge `--app` window (borderless, no separate app registration). If you ever install such a URL as an Edge app manually, dsh-gui will prefer the installed app automatically. See [Install as an Edge app (optional)](#install-as-an-edge-app-optional).
- **Killing**: sends `SIGTERM`, waits up to 5 s, then escalates to `SIGKILL`. Killing the process that serves the GUI port disconnects any live session on it; the script warns before doing so.

## Install as an Edge app (optional)

Once the GUI is up (run `dsh-gui` once), you can install it as an Edge app so it gets its own Dock icon and window — dsh-gui then opens the installed app automatically. In a **normal Edge tab** (the `--app` window dsh-gui opens has a reduced menu without this option), open `http://127.0.0.1:3080` and go to:

`⋯` → **More tools** → **Apps** → **Install this site as an app** (on some versions, **Apps** sits directly in the `⋯` menu).

Name the app (e.g. *DeepSeek Harness*) and click **Install**. The app is bound to the exact URL, so install one per port if you use `--port`. If `dsh web` is kept alive by launchd, the installed app can be opened straight from the Dock without running dsh-gui. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for the full walkthrough.

## Environment variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `DSH_CMD` | `dsh` if on `PATH`, else `npx -y @deepseek-ai/dsh` | command that launches dsh |
| `DSH_GUI_PORT` | `3080` | listen port to use/check |
| `DSH_GUI_TIMEOUT` | `60` | seconds to wait for the service/tunnel to come up |
| `DSH_PROC_PATTERN` | built-in | ERE matching dsh process command lines |
| `DSH_TUNNEL_PATTERN` | built-in | ERE matching dsh-gui ssh tunnels |
| `DSH_HOME` | `~/.dsh` | where log files are written |
| `DSH_BROWSER_APP` | `Microsoft Edge` | browser app used for app windows (a name or path accepted by `open -a`, e.g. `Google Chrome`) |

## License

[MIT](LICENSE)
