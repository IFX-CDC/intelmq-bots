# -*- coding: utf-8 -*-
"""
VirusshareParserBot parses data from https://virusshare.com/hashes/VirusShare_XXXXX.md5.

"""
from intelmq.lib.bot import ParserBot

class VirusshareParserBot(ParserBot):
    def parse_line(self, line, report):
        if not line.startswith('#') and not len(line) == 0:
            event = self.new_event(report)
            event.add('malware.hash.md5', line)
            event.add('classification.type', 'malware')
            event.add('raw', line)
            yield event

BOT = VirusshareParserBot