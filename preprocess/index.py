from elasticsearch import Elasticsearch
import argparse

def Args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", type=str, default="../data/docs")
    return parser.parse_args()

def count_lines(filename):
    count = 0
    with open(filename, 'rb') as f:
        last_data = '\n'
        while True:
            data = f.read(0x400000)
            if not data:
                break
            count += data.count(b'\n')
            last_data = data
        if last_data[-1:] != b'\n':
            count += 1
    return count


if __name__ == '__main__':
    es = Elasticsearch()
    args = Args()
    es.indices.delete(index='ir', ignore=[400, 404])
    es.indices.delete(index='ir-raw', ignore=[400, 404])
    count = count_lines(args.docs)
    with open(args.docs, 'r') as f:
        p = 0
        pp = -1
        index = 0
        body = {"text": [], "attr": []}
        body_raw = {"text": []}
        for line in f:
            text = []
            attr = []
            text_raw = []
            line = line.strip().split()
            for pair in line:
                text_raw.append(pair)
                pair = pair.split('/')
                text.append(pair[0])
                attr.append(pair[1])
            body['text'] = text
            body['attr'] = attr
            body_raw['text'] = text_raw
            
            es.index(index='ir', doc_type='doc', id=index, body=body)
            es.index(index='ir-raw', doc_type='doc', id=index, body=body_raw)
            
            index += 1
            p = int(index / count * 100)
            if p != pp:
                pp = p
                print("lines = {}, {}% now".format(index, p))

    print(index)

