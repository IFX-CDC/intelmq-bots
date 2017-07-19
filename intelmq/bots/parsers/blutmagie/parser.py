# -*- coding: utf-8 -*-
"""
BlutmagieParserBot parses data from https://www.dan.me.uk/torlist/?exit.

"""
from intelmq.lib.bot import ParserBot
class BlutmagieParserBot(ParserBot):
    def parse_line(self, line, report):
        if not line.startswith('#') and not len(line) == 0:
            event = self.new_event(report)
            event.add('source.ip', line)
            event.add('source.tor_node', True)
            event.add('classification.type', 'blacklist')
            event.add('raw', line)
            yield event
BOT = BlutmagieParserBot