
# Commands

- `console` - attatches the terminal to the console of a server (view running log, send commands)
  - Required argument `NAME` - name of server
- `create` - create new server
  - Optional option `--console` - attach to console of server immediately after server start
  - Optional option `--detach` - skip waiting for installation to finish (useful for games that take some time to install). Installation process continues in the background.
- `delete` - delete already existing server
  - Required argument `NAME` - name of server
- `edit` - edit already existing server
  - Required argument `NAME` - name of server
- `images` - list all images
  - Optional option `--refresh` - updates all default image configs from GitHub
- `kill` - kill container of running server
  - Required argument `NAME` - name of server
- `servers` - list servers, prints as table
- `setup` - used for initial configuration, set the path for storing server files
- `start` - start server
  - Required argument `NAME` - name of server
- `stop` - gracefully stop container, sends stop command and waits for server to die
  - Required argument `NAME` - name of server
