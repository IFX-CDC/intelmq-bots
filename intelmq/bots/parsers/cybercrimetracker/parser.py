# -*- coding: utf-8 -*-
"""
CyberCrimeTrackerParserBot parses data from http://cybercrime-tracker.net/all.php.

"""
from intelmq.lib.bot import ParserBot
class CyberCrimeTrackerParserBot(ParserBot):
    def parse_line(self, line, report):
        if not line.startswith('#') and not len(line) == 0:
            event = self.new_event(report)
            event.add('source.url', line)
            event.add('raw', line)
            yield event
BOT = CyberCrimeTrackerParserBot