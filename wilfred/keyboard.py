# wilfred
# https://github.com/wilfred-dev/wilfred
# (c) Vilhelm Prytz 2020

import threading


class KeyboardThread(threading.Thread):
    def __init__(self, input_callback, params):
        self.input_callback = input_callback
        self.params = params

        super(KeyboardThread, self).__init__(name="wilfred-console-input", daemon=True)

        self.start()

    def run(self):
        while True:
            self.input_callback(input(), self.params)
