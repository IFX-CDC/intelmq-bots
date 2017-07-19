# -*- coding: utf-8 -*-
"""
CortexParserBot parses data from Cortex.

"""
from intelmq.lib.bot import ParserBot

class CortexParserBot(ParserBot):
    def process(self):
        event = self.receive_message()
        self.send_message(event)
        self.acknowledge_message()

BOT = CortexParserBot