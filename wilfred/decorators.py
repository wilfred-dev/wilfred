####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

from functools import wraps

from wilfred.message_handler import error


def configuration_present(config):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not config.configuration:
                error("Wilfred has not been configured", exit_code=1)

        return decorated_function

    return decorator
