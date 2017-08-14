# -*- coding: utf-8 -*-
from intelmq.lib.bot import Bot
from intelmq.lib.message import Event

try:
    from elasticsearch import Elasticsearch
except ImportError:
    Elasticsearch = None


class ElasticDeduplicatorBot(Bot):

    def init(self):
        if Elasticsearch is None:
            raise ValueError('Missing elasticsearch module.')
        try:
            self.elastic_host = getattr(self.parameters, 'elastic_host')
            self.elastic_port = getattr(self.parameters, 'elastic_port', '9200')
            self.elastic_index = getattr(self.parameters, 'elastic_index', 'intelmq')
            self.elastic_doctype = getattr(self.parameters, 'elastic_doctype', 'events')
            self.ttl = getattr(self.parameters, 'ttl', 30)
            self.es = Elasticsearch([{'host': self.elastic_host, 'port': self.elastic_port}])
            if not self.es.indices.exists(self.elastic_index):
                self.es.indices.create(index=self.elastic_index, ignore=400)
        except Exception as e:
            self.logger.info(e)
            self.stop()
    
    def process(self):
        event = self.receive_message()
        try:
            mat = []
            q = '{"query":{"bool":{"must":[{ "match": { "raw":  "'+event.get("raw")+'"}}],"filter":[{"range":{"time.observation":{"gte":"now-'+str(self.ttl)+'d/d","lte":"now/d"}}}]}}}'
            res = self.es.search(index=self.elastic_index, body=q)
            if res['hits']['total'] == 0: 
                self.es.index(index=self.elastic_index,doc_type=self.elastic_doctype,body=event.to_json(hierarchical=False))
                self.send_message(event)
        except Exception as e:
            self.logger.info(e)

        self.acknowledge_message()

BOT = ElasticDeduplicatorBot
