# -*- coding: utf-8 -*-
import requests
from intelmq.lib.bot import CollectorBot

class VirusshareCollectorBot(CollectorBot):

    def init(self):
        self.set_request_parameters()
        self.last_fetched = 1
        self.parameters.feed = "virusshare"

    def process(self):
        for i in range(self.last_fetched - 1, 99999):
            u = "https://virusshare.com/hashes/VirusShare_"+str(i).zfill(5) +".md5"
            resp = requests.get(url=u, verify=False)
            if resp.status_code // 100 != 2:
                break
            else:
                report = self.new_report()
                report.add("raw", resp.text)
                report.add("feed.url", u)
                self.send_message(report)
                self.last_fetched = i

BOT = VirusshareCollectorBot