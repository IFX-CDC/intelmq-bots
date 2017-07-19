# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

class AddKeyExpertBot(Bot):
    def init(self):
        self.key = self.parameters.key
        self.value = self.parameters.value

    def process(self):
        event = self.receive_message()
        event.add(self.key, self.value, overwrite=True)
        self.send_message(event)
        self.acknowledge_message()

BOT = AddKeyExpertBot