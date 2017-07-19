# -*- coding: utf-8 -*-

import requests
from intelmq.lib.bot import Bot
from pymisp import PyMISP
import json

class MISPOutputBot(Bot):
    def init(self):
        try:
            self.MISP = PyMISP(self.parameters.server, self.parameters.key, ssl=False)
        except Exception as e:
            self.logger.exception(e)
            self.stop()

    def process(self):
        event = self.receive_message()
        attributes = []
        mapping = {"source.url":"url", "source.ip":"ip-src", "source.fqdn":"domain", "source.as_name":"AS", "malware.hash.md5":"md5"}
        mapping_category = {"source.url":"Network activity", "source.ip":"Network activity", "source.fqdn":"Network activity", "source.as_name":"Network activity", "malware.hash.md5":"Payload delivery"}
        # add attributes
        if event.get("source.reverse_dns"):
            res = self.MISP.add_named_attribute(self.parameters.event, 'domain|ip', "{}|{}".format(event.get("source.reverse_dns"), event.get("source.ip"), category="External analysis"))
            if res.get("Attribute"):
                attributes.append(res)
        else :
            for field in mapping:
                val = event.get(field)
                if val:
                    res = self.MISP.add_named_attribute(self.parameters.event, mapping[field], val, category=mapping_category[field], comment=event.get("event_description.text"))
                    if res.get("Attribute"):
                        attributes.append(res)
        # add tags
        for attribute in attributes:
            try:
                for tag in json.loads(event.get("extra"))["tags"]:
                    self.MISP.new_tag(tag["tag"])
                    self.MISP.add_tag(attribute["Attribute"], tag["tag"], attribute=True)
            except:
                pass
        self.acknowledge_message()
        
BOT = MISPOutputBot