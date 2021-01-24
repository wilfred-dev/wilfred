#################################################################
#                                                               #
# Wilfred                                                       #
# Copyright (C) 2020-2021, Vilhelm Prytz, <vilhelm@prytznet.se> #
#                                                               #
# Licensed under the terms of the MIT license, see LICENSE.     #
# https://github.com/wilfred-dev/wilfred                        #
#                                                               #
#################################################################

from functools import wraps

from wilfred.message_handler import error
from wilfred.api.config_parser import Config, NoConfiguration

config = Config()

try:
    config.read()
except NoConfiguration:
    pass


def configuration_present(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not config.configuration:
            error("Wilfred has not been configured", exit_code=1)
        return f(*args, **kwargs)

    return decorated_function
