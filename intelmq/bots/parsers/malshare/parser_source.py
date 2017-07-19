# -*- coding: utf-8 -*-
"""
MalshareSourceParserBot parses data from http://malshare.com/api.php?api_key=<api_key>&action=getsourcesraw.

"""

from intelmq.lib.bot import ParserBot
from intelmq.lib import utils

class MalshareSourceParserBot(ParserBot):
    def process(self):
        report = self.receive_message()
        raw_report = utils.base64_decode(report.get('raw'))
        for line in raw_report.split("\n"):
            event = self.new_event(report)
            event.add('source.url', line)
            event.add('classification.type', 'malware')
            event.add('raw', line)
            self.send_message(event)
        self.acknowledge_message()
BOT = MalshareSourceParserBot