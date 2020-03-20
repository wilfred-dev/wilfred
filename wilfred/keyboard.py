####################################################################
#                                                                  #
# Wilfred                                                          #
# Copyright (C) 2020, Vilhelm Prytz, <vilhelm@prytznet.se>, et al. #
#                                                                  #
# Licensed under the terms of the MIT license, see LICENSE.        #
# https://github.com/wilfred-dev/wilfred                           #
#                                                                  #
####################################################################

import threading


class KeyboardThread(threading.Thread):
    def __init__(self, input_callback, params):
        self._running = True
        self.input_callback = input_callback
        self.params = params

        super(KeyboardThread, self).__init__(name="wilfred-console-input", daemon=True)

        self.start()

    def run(self):
        while self._running:
            try:
                self.input_callback(input(), self.params)
            except Exception:
                self._running = False
