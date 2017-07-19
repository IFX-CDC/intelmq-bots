# -*- coding: utf-8 -*-
from intelmq.lib.bot import ParserBot
class EmergingThreatsParserBot(ParserBot):
    def parse_line(self, line, report):
        if not line.startswith('#') and not len(line) == 0:
            event = self.new_event(report)
            event.add('source.ip', line)
            event.add('classification.type', 'blacklist')
            event.add('raw', line)
            yield event
BOT = EmergingThreatsParserBot