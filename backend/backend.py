from elasticsearch import Elasticsearch
import math


class Backend():
    def __init__(self, strategy = 'dummy', doc_size = 1000):
        self.es = Elasticsearch()
        self.strategy = strategy
        self.doc_size = doc_size

    
    def find_nearest(self, text, cw, w, pos):
        if cw == w:
            return 0
        i = pos - 1
        l1 = len(text) + 1
        while i >=0:
            if text[i] == cw:
                l1 = pos - i
                break
            i -= 1
        
        i = pos + 1
        l2 = len(text) + 1
        while i < len(text):
            if text[i] == cw:
                l2 = i - pos
                break
            i += 1
        return min(l1, l2)


    def query(self, q, aim_attr='', length=-1):
        
        # Step 1. Construct the original query
        body = {}
        body['query'] = {}
        body['query']['bool'] = {}
        body['query']['bool']['must'] = []
        words = q.split(' ')
        if len(words) == 0:
            return []
        for word in words:
            body['query']['bool']['must'].append({'term': {'text.keyword': word}})
        hits = self.es.search(index='ir', body=body)['hits']['hits'] 
        if len(hits) == 0:
            return []
         
        # Step 2. Find potential results

        res0 = {}
        for hit in hits:
            src = hit['_source']
            text = src['text']
            attr = src['attr']
            cw = words[0]   # Choose the first query word as center word
            for i in range(len(text)):
                w = text[i]
                a = attr[i]
                if w in words:
                    continue
                l = self.find_nearest(text, cw, w, i)
                if l == 0:
                    continue
                if w not in res0:
                    res0[w] = {}
                if a not in res0[w]:
                    res0[w][a] = {'tf': 0, 'l': -1}
                res0[w][a]['tf'] += 1
                if res0[w][a]['l'] == -1 or res0[w][a]['l'] > l:
                    res0[w][a]['l'] = l
        # Step 3. Filter 1 : Based on attr of the word
        
        filter1 = set(['t', 'm', 'q', 'mq', 'r', 'c', 'p', 'u', 'y', 'e', 'o', 'g', 'w', 'x'])       # By default ignore words with such attrs
        res1 = {}
        for w in res0:
            for a in res0[w]:
                if a in filter1:
                    continue
                if aim_attr == '':
                    if w not in res1:
                        res1[w] = {}
                    if 'all' not in res1[w]:
                        res1[w]['all'] = res0[w][a]
                        continue
                    res1[w]['all']['tf'] += res0[w][a]['tf']
                    res1[w]['all']['l'] = min(res0[w][a]['l'], res1[w]['all']['l'])
                else:
                    if a != aim_attr and aim_attr != 'all':
                        continue
                    if w not in res1:
                        res1[w] = {}
                    res1[w][a] = res0[w][a]

        # Step 4. Filter 2 : Based on distance constrain

        res2 = {}
        if length == -1:
            res2 = res1
        else:
            for w in res1:
                for a in res1[w]:
                    if res1[w][a]['l'] > length:
                        continue
                    if w not in res2:
                        res2[w] = {}
                    res2[w][a] = res1[w][a]


        # Step 5. Rank by user defined strategy
        
        res3 = {}
        for w in res2:
            for a in res2[w]:
                if w not in res3:
                    res3[w] = {}
                res3[w][a] = {'l': res2[w][a]['l'], 's': -1, 'tf': res2[w][a]['tf']}
        if self.strategy == 'dummy':
            for w in res3:
                for a in res3[w]:
                    res3[w][a]['s'] = 233
        elif self.strategy == 'tf-idf':
            for w in res3:
                for a in res3[w]:
                    if a == 'all':
                        body = {'query': {'match':{'text.keyword':w}}}
                        hits = self.es.search(index='ir', body=body)['hits']['hits']
                        df = len(hits)
                    else:
                        body = {'query': {'match':{'text.keyword':'{}/{}'.format(w, a)}}}
                        hits = self.es.search(index='ir-raw', body=body)['hits']['hits']
                        df = len(hits)
                    if df == 0:
                        s = -1
                    else:
                        s = res3[w][a]['tf'] * math.log(self.doc_size / df) 
                    res3[w][a]['s'] = s
                    
        elif self.strategy == 'bm25':
            None
        
        res4 = []
        for w in res3:
            for a in res3[w]:
                res4.append([w, a, res3[w][a]['s'], res3[w][a]['l']])
        res4 = list(sorted(res4, key = lambda x: x[2], reverse=True))
        return res4


if __name__ == '__main__':
    backend = Backend('tf-idf')
    res = backend.query('空气', 'a', 5)
    for d in res:
        print("word {}, attr {}, score {}, length {}".format(d[0], d[1], d[2], d[3]))
