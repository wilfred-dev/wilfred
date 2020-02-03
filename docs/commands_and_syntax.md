
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
- `top` - Displays server statistics such as CPU load, memory usage etc., updates in real-time (like `top`)
- `config` - View and edit configuration settings for a specific server. It parses configuration files for supported games and allows the user to modify settings without ever touching the actual config file (such as `server.properties` for Minecraft). Example: `wilfred config server-name white-list "on"`
  - Required argument `NAME` - Name of the server.
  - Optional argument `VARIABLE` - Name of an available setting. Displays the value of the specified variable if a new value is not set.
  - Optional argument `VALUE` - The new value for the variable setting.
