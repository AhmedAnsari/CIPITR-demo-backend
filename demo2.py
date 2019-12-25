import pickle as pkl
import numpy as np
d=pkl.load(open('../../../../data/test_data2.pkl'))
def get_batch(size):
    indices = np.random.choice(len(d),size)
    out = []
    for index in indices:
        question = d[index][0].split('\t')[0]
        entities = d[index][3]
        types = d[index][4]
        rels = d[index][5]
        ints = d[index][6]
        program = d[index][-1]['results']['per_step_programs']
        reward = d[index][-1]['results']['reward']
        out.append([question,entities, types, rels, ints, program, reward])
    return out

