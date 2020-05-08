Images
======

Not to be confused with actual Docker images, Wilfred images are configuration files used by Wilfred to create game servers. It tells Wilfred which Docker container to run the server in, with which command the server is started with and how to initially install libraries etc.

Wilfred images are formatted in JSON.

This is the configuration file for Vanilla Minecraft.

.. code-block:: json

    {
        "meta": {
            "api_version": 2
        },
        "uid": "minecraft-vanilla",
        "name": "Vanilla Minecraft",
        "author": "vilhelm@prytznet.se",
        "docker_image": "wilfreddev/java:latest",
        "command": "java -Xms128M -Xmx{{SERVER_MEMORY}}M -jar server.jar",
        "user": "container",
        "stop_command": "stop",
        "default_image": true,
        "config": {
            "files": [
                {
                    "filename": "server.properties",
                    "parser": "properties",
                    "environment": [
                        {
                            "config_variable": "server-port",
                            "environment_variable": "SERVER_PORT",
                            "value_format": null
                        }
                    ],
                    "action": {
                        "difficulty": "difficulty {}",
                        "white-list": "whitelist {}"
                    }
                }
            ]
        },
        "installation": {
            "docker_image": "wilfreddev/alpine:latest",
            "shell": "/bin/ash",
            "script": [
                "apk add curl --no-cache --update jq",
                "if [ \"$MINECRAFT_VERSION\" == \"latest\" ]; then",
                "   VERSION=`curl https://launchermeta.mojang.com/mc/game/version_manifest.json | jq -r '.latest.release'`",
                "else",
                    "VERSION=\"$MINECRAFT_VERSION\"",
                "fi",
                "MANIFEST_URL=$(curl -sSL https://launchermeta.mojang.com/mc/game/version_manifest.json | jq --arg VERSION $VERSION -r '.versions | .[] | select(.id== $VERSION )|.url')",
                "DOWNLOAD_URL=$(curl ${MANIFEST_URL} | jq .downloads.server | jq -r '. | .url')",
                "curl -o server.jar $DOWNLOAD_URL",
                "if [ \"$EULA_ACCEPTANCE\" == \"true\" ]; then",
                "   echo \"eula=true\" > eula.txt",
                "fi",
                "curl -o server.properties https://raw.githubusercontent.com/wilfred-dev/images/master/configs/minecraft/standard/server.properties",
                "sed -i \"s/{{SERVER_PORT}}/$SERVER_PORT/g\" server.properties",
                "chown -R container:container /server"
            ]
        },
        "variables": [
            {
                "prompt": "Which Minecraft version to use during install?",
                "variable": "MINECRAFT_VERSION",
                "install_only": true,
                "default": "latest",
                "hidden": false
            },
            {
                "prompt": "Do you agree to the Minecraft EULA (https://account.mojang.com/documents/minecraft_eula)?",
                "variable": "EULA_ACCEPTANCE",
                "install_only": true,
                "default": "true",
                "hidden": false
            }
        ]
    }

Image syntax
------------

**All** variables are required for image configurations.

- `meta`
    - `api_version` - Version of configuration.
- `uid` - A unique ID for this config, do not uses spaces. **Must be lowercase.**
- `name` - Name of image to be displayed to user.
- `author` - Email of author.
- `docker_image` - Docker image to run server in.
- `command` - Command to be executed on start.
- `user` - User to run command as, leave empty for default `root`.
- `stop_command` - Command to send to STDIN in order to stop the container.
- `default_image` - Indicates to Wilfred that the image is an official image from the Wilfred project.
- `config` - Configuration files and how Wilfred should parse them, used within the `wilfred config` command (such as `server.properties` for Minecraft or `config.yml` for BungeeCord).
    - `files` - List of files to parse.
        - `filename` - The filename to read and write to.
        - `parser` - What parser Wilfred should use (file-type). Currently, only `properties`, `yaml` and `json` are supported parsers.
        - `environment` - List of environment variables to link to specific config settings.
            - `config_variable` - The setting (variable name) as it's named within the configuration file (e.g. `server-port` as that's the name of the setting in `server.properties`).
            - `environment_variable` - A valid environment variable to link with the specified setting. Apart from the variables specified in the image config, `SERVER_PORT` and `SERVER_MEMORY` are valid values.
            - `value_format` - Can be used to append a prefix to the value. Specifying `null` just replaces the value of the setting with the value of the environment variable, without prefixes and suffixes. Otherwise, use `{}` to indicate where the actual value should be set (e.g. `0.0.0.0:{}` is valid syntax).
        - `action` - Dictionary, sends a command to the STDIN of the container when the setting updates.
            - `{SETTING_NAME}` - The value should contain the command that should be sent to the container when the specified setting changes. Use `{}` to indicate where the actual value should be set (e.g. `whitelist {}` would send `whitelist on` if the user runs `wilfred config my-server white-list "on"`).
- `installation`
    - `docker_image` - Docker image to use during installation.
    - `shell` - Shell to use (usually `/bin/ash` for Alpine or `/bin/bash` for Ubuntu/Debian).
    - `script` - List (array) of commands to execute during installation.
- `variables` - List of environment variables.
    - `prompt` - Prompt during server creation/modification.
    - `variable` - Name of environment variable.
    - `install_only` - boolean, variable will only be accessible during installation if `true`.
    - `default` - Default value for prompt, use boolean `true` in order to make variable required but not set a default value and use `""` to make it optional, without default value.
    - `hidden` - Boolean, decides whether this value should be hidden from the user (i.e. static variables).

Environment Variables
---------------------

Environment variables can be defined in the image configuration. The user will be prompted to enter values for these variables when creating a new server.

The variables are accessible from the installation script and the startup command. But referring to them is slightly different.

To access an environment variable named `MINECRAFT_VERSION` from the installation script, one can use `$MINECRAFT_VERSION` (just as you'd expect it to work).

And to access an environment variable from the startup command, refer to it as `{{image.env.KEY}}` (e.g. `{{image.env.MINECRAFT_VERSION}}` in this case).

Default Variables
-----------------

The variable `SERVER_MEMORY` and `SERVER_PORT` (so `{{SERVER_MEMORY}}` from the startup command and `$SERVER_MEMORY` from the installation script) are always defined and can be accessed in both the installation script and the startup command.

Default Images
--------------

You can find the default images `here <https://github.com/wilfred-dev/images/tree/master/images>`__.


Creating a custom image
-----------------------

When creating a custom image, make sure to **not** put it in the same folder as the default ones. The `default` folder is deleted when Wilfred updates the images from GitHub.
