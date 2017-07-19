# -*- coding: utf-8 -*-
"""
HaleysParserBot parses data from http://charles.the-haleys.org/ssh_dico_attack_hdeny_format.php/hostsdeny.txt.

"""
from intelmq.lib.bot import ParserBot
class HaleysParserBot(ParserBot):
    def parse_line(self, line, report):
        if not line.startswith("#"):
            event = self.new_event(report)
            event.add('source.ip', str(line[6:]))
            event.add('classification.type', 'blacklist')
            event.add('raw', line)
            yield event
BOT = HaleysParserBot