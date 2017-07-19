# -*- coding: utf-8 -*-
"""
CortexOutputBot stores data that it can be fetched from Cortex.

"""
from intelmq.lib.bot import Bot
import time

class CortexOutputBot(Bot):

    def process(self):
        event = self.receive_message()
        time.sleep(0.5)

BOT = CortexOutputBot