import sys
from frontend.forms import IRForm, ResForm
sys.path.append("..")
from backend.backend import Backend

back = Backend('tf-idf', 1000000)


def query(form, result, lim = 50):
    key = form.keywords.data
    attr = form.attributes.data
    l = form.length.data
    merge = form.merge.data

    if not merge and attr == '':
        attr = 'all'

    if l == None:
        l = -1
    if l <= 0:
        l = -1

    res = back.query(key, attr, l)
    result.data = []
    for i, d in enumerate(res):
        if i > lim:
            break
        result.data.append({'index': i, 'name': d[0], 'attr': d[1], 'score': round(d[2], 2), 'length': d[3]})

