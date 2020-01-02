# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import json

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

    def _read_images(self):
        self.images = []

        for root, dirs, files in walk(self.image_dir):
            for file in files:
                if file.endswith(".json"):
                    with open(join(root, file)) as f:
                        _image = json.loads(f.read())

                        if _image["meta"]["version"] != API_VERSION:
                            error(
                                f"{file} image has API level {_image['meta']['version']}, Wilfreds API level is {API_VERSION}",
                                exit_code=1,
                            )

                        self.images.append(_image)

    def pretty(self):
        _images = self.images

        for d in _images:
            del d["meta"]
            del d["installation"]
            del d["docker_image"]
            del d["command"]

        headers = {
            "uuid": "UUID",
            "name": "Image Name",
            "author": "Author",
            "default_image": "Default Image",
        }

        return tabulate(_images, headers=headers, tablefmt="fancy_grid")

    def get_image(self, uuid):
        return list(filter(lambda img: img["uuid"] == uuid, self.images))
