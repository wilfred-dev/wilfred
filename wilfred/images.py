# Wilfred
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>
#
# Licensed under the terms of the MIT license, see LICENSE.
# https://github.com/wilfred-dev/wilfred

import json
import click

from tabulate import tabulate
from appdirs import user_config_dir
from pathlib import Path
from os.path import isdir, join
from os import walk, remove
from requests import get
from zipfile import ZipFile
from shutil import move, rmtree

from wilfred.message_handler import warning, error

API_VERSION = 0


class Images(object):
    def __init__(self):
        self.config_dir = f"{user_config_dir()}/wilfred"
        self.image_dir = f"{self.config_dir}/images"

        if not isdir(self.image_dir):
            Path(self.image_dir).mkdir(parents=True, exist_ok=True)

        if not isdir(f"{self.image_dir}/default"):
            warning(
                "default image directory does not exist, downloading default images"
            )
            self.download_default()

        self._read_images()

    def download_default(self):
        rmtree(f"{self.image_dir}/default", ignore_errors=True)

        with open(f"{self.config_dir}/img.zip", "wb") as f:
            response = get(
                "https://github.com/wilfred-dev/images/archive/master.zip", stream=True
            )
            f.write(response.content)

        with ZipFile(f"{self.config_dir}/img.zip", "r") as obj:
            obj.extractall(f"{self.config_dir}/temp_images")

        move(
            f"{self.config_dir}/temp_images/images-master/images",
            f"{self.image_dir}/default",
        )

        remove(f"{self.config_dir}/img.zip")
        rmtree(f"{self.config_dir}/temp_images")

        self._read_images()

    def pretty(self):
        _images = self.images

        for d in _images:
            try:
                del d["meta"]
                del d["installation"]
                del d["docker_image"]
                del d["command"]
                del d["stop_command"]
                del d["variables"]
            except Exception:
                pass

        headers = {
            "uid": "UID",
            "name": "Image Name",
            "author": "Author",
            "default_image": "Default Image",
        }

        return tabulate(_images, headers=headers, tablefmt="fancy_grid")

    def get_image(self, uid):
        self._read_images()

        image = list(filter(lambda img: img["uid"] == uid, self.images))

        return image[0] if image else None

    def _read_images(self):
        self.images = []

        for root, dirs, files in walk(self.image_dir):
            for file in files:
                if file.endswith(".json"):
                    with open(join(root, file)) as f:
                        _image = json.loads(f.read())

                        try:
                            if _image["meta"]["api_version"] != API_VERSION:
                                error(
                                    " ".join(
                                        (
                                            f"{file} image has API level {_image['meta']['api_version']},",
                                            "Wilfreds API level is {API_VERSION}",
                                        )
                                    ),
                                    exit_code=1,
                                )
                        except Exception as e:
                            error(
                                f"could not parse config, has API level changed? - {click.style(str(e), bold=True)}"
                            )

                        self.images.append(_image)
