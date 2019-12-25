from __future__ import print_function # In python 2.7
import sys
import pickle
import flask
import os
import json
import operator
import random

from flask_cors import CORS, cross_origin
from collections import OrderedDict

from helper_dicts import *
# from demo import Environment
from demo2 import *

app = flask.Flask(__name__)
CORS(app)
port = int(os.getenv("PORT", 8099))

# params_file = 'parameters/param_demo.json'
# param = json.load(open(params_file))
# env = Environment(param,'Train')

def join(l):
    f=False
    s=""
    for e in l:
        s+="\""+e+"\", "
        f=True
    if f:
        s=s[:-2]
    return s

def join2(l):
    f=False
    s=""
    for e in l:
        s+=e+", "
        f=True
    if f:
        s=s[:-2]
    return s

def correct(prog):
    prog_ret = []
    for p in prog:
        p2 = []
        for q in p:
            if q[:4]=="none":
		p2.append("none()")
            elif q[:9]=="terminate":
                p2.append("terminate()")
            else:
                p2.append(q)
        prog_ret.append(p2)
    return prog_ret

@app.route('/getQuestions', methods=['GET'])
def getQuestions():
    ques = get_batch(10)
    print(ques)
    question = [ a[0] for a in ques ]
    entities = [join(a[1]) for a in ques]
    types = [join(a[2]) for a in ques]
    rels = [join(a[3]) for a in ques]
    ints = [join2(a[4]) for a in ques]
    prog = [a[5] for a in ques]
    prog = correct(prog)
    rewards = [str(a[6]) for a in ques]
    response = {
            'questions': question,
            'entities': entities,
            'rels': rels,
            'types':types,
            'ints':ints,
            'progs': prog,
            'rewards':rewards
            }
    print(response, file=sys.stdout)
    res = flask.jsonify(response)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

