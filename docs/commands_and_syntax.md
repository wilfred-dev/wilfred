
# Commands and syntax

Basic commands and syntax available for Wilfred.

- `--version` - Print version and exit.
- `--path` - Print paths for configurations and server data.
- `console` - Attatches the terminal to the console of a server (view running log, send commands).
  - Required argument `NAME` - Name of server.
- `create` - Create a new server.
  - Optional option `--console` - Attach to console of server immediately after server start.
  - Optional option `--detach` - Skip waiting for installation to finish (useful for games that take some time to install). Installation process continues in the background.
- `delete` - Delete already existing server.
  - Required argument `NAME` - Name of server.
- `edit` - Edit already existing server.
  - Required argument `NAME` - Name of server.
- `images` - List all images.
  - Optional option `--refresh` - Updates all default image configs from GitHub.
- `kill` - Kill container of running server.
  - Required argument `NAME` - Name of server.
- `servers` - List existing servers, prints as table.
- `setup` - Used for initial configuration, set the path for storing server files.
- `start` - Start server.
  - Required argument `NAME` - Name of server.
- `stop` - Gracefully stop container, sends stop command and waits for container to die.
  - Required argument `NAME` - Name of server.
