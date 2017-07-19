# -*- coding: utf-8 -*-
import io

from intelmq.lib.bot import Bot
import json

class CSVOutputBot(Bot):

    def init(self):
        self.logger.debug("Opening %r file.", self.parameters.file)
        self.file = io.open(self.parameters.file, mode='at', encoding="utf-8")
        self.logger.info("File %r is open.", self.parameters.file)

    def process(self):
        event = self.receive_message()
        #event_data = event.to_json(hierarchical=self.parameters.hierarchical_output)
        event_data = event.to_json(hierarchical=False)
        data = json.loads(event_data)
        fields = self.parameters.fields.split(",")
        da = []
        for field in fields:
            if field in data:
                da.append(data[field])
            else:
            	da.append("")
        try:
            self.file.write(','.join(str(item) for item in da))
            self.file.write("\n")
            self.file.flush()
        except FileNotFoundError:
            self.init()
        else:
            self.acknowledge_message()


BOT = CSVOutputBot