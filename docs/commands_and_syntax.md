
# Commands and syntax

Basic commands and syntax available for Wilfred.

- `--version` - Print version and exit.
- `--path` - Print paths for configurations and server data.
- `console` - Attaches the terminal to the console of a server (view running log, send commands).
  - Required argument `NAME` - Name of the server.
- `create` - Create a new server.
  - Optional option `--console` - Attach to console of server immediately after server start.
  - Optional option `--detach` - Skip waiting for the installation to finish (useful for games that take some time to install). Installation process continues in the background.
- `delete` - Delete already existing server.
  - Required argument `NAME` - Name of the server.
- `edit` - Edit already existing server.
  - Required argument `NAME` - Name of the server.
- `images` - List all images.
  - Optional option `--refresh` - Updates all default image configs from GitHub.
- `kill` - Kill container of a running server.
  - Required argument `NAME` - Name of the server.
- `servers` - List existing servers, prints as a table.
- `setup` - Used for initial configuration, set the path for storing server files.
- `start` - Start the server.
  - Required argument `NAME` - Name of the server.
- `stop` - Gracefully stop the container, sends stop command and waits for the container to die.
  - Required argument `NAME` - Name of the server.
- `restart` - Restart server (using graceful stop).
  - Required argument `NAME` - Name of the server.
- `command` - Send command to STDIN of server (without attaching to console).
  - Required argument `NAME` - Name of the server.
  - Required argument `COMMAND` - Command to send, can be put in `"` for commands with whitespaces. Example: `wilfred command <name> "say Hello World"`.
