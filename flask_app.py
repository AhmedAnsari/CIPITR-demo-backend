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
from demo import Environment

app = flask.Flask(__name__)
CORS(app)
port = int(os.getenv("PORT", 9099))

params_file = 'parameters/param_demo.json'
param = json.load(open(params_file))
env = Environment(param,'Train')

def step_message(func,arg1,arg2,arg3):
    if func=='gen_set':
        e = arg1
        r = arg2
        t = arg3
        return ("set object which consists of those entities of type \"%s\" that are related to entity \"%s\" by relation \"%s\"" % (t,e,r))
    if func=='gen_map_set':
        t1 = arg1
        r = arg2
        t2 = arg3
        return ("map (or dict) object with each entity of type \"%s\" as keys and the set of entities of type \"%s\" that is related to the key by \"%s\" as values" % (t1,t2,r))
    if func=='set_count':
        A = arg1
        return ("number of entities in set \"%s\"" % A)
    if func=='set_ints':
        A = arg1
        B = arg2
        return ("intersection of sets \"%s\", \"%s\"" % (A,B))
    if func=='set_diff':
        A = arg1
        B = arg2
        return ("difference of sets \"%s\", \"%s\"" % (A,B))
    if func=='set_union':
        A = arg1
        B = arg2
        return ("union of sets \"%s\", \"%s\"" % (A,B))
    if func=='map_count':
        A = arg1
        return ("for each entity in Map \"%s\", returns the count of the sets corresponding to that entity \"%s\". Output is a map_int object" % A)
    if func=='map_diff':
        A = arg1
        B = arg2
        return ("for each e in both Map \"%s\", \"%s\", returns the difference of the sets corresponding to that entity" % (A,B))
    if func=='map_ints':
        A = arg1
        B = arg2
        return ("for each e in both Map \"%s\", \"%s\", returns the intersection of the sets corresponding to that entity" % (A,B))
    if func=='map_union':
        A = arg1
        B = arg2
        return ("for each e in both Map \"%s\", \"%s\", returns the union of the sets corresponding to that entity" % (A,B))
    if func=='verify':
        return ('a boolean flag indicating if entities \"%s\", \"%s\" are related by relation \"%s\" in the KB.' %(arg1,arg3,arg2))
    if func=='terminate':
        return ('Terminate program')
    if func=='none':
        return ('No action')
    if func=='select_min':
        return ('for each entity e in \"%s\", selects that entity whose mapped int is the lowest among all the enitites in \"%s\"' %(arg1,arg1))
    if func=='select_max':
        return ('for each entity e in \"%s\", selects that entity whose mapped int is the highest among all the enitites in \"%s\"' %(arg1,arg1))
    if func=='select_more':
        return ('for each entity e in \"%s\", selects that entity whose mapped int > \"%s\" and returns a set of seleceted entities' %(arg1,arg2))
    if func=='select_less':
        return ('for each entity e in \"%s\", selects that entity whose mapped int < \"%s\" and returns a set of seleceted entities' %(arg1,arg2))
    if func=='select_equal':
        return ('for each entity e in A, selects that entity whose mapped int = B and returns a set of seleceted entities' %(arg1,arg2))
    if func=='select_almost':
        return ('for each entity e in \"%s\", selects that entity whose mapped int <= \"%s\" and returns a set of seleceted entities' %(arg1,arg2))
    if func=='select_atleast':
        return ('for each entity e in \"%s\", selects that entity whose mapped int >= \"%s\" and returns a set of seleceted entities' %(arg1,arg2))
    if func=='select_approx':
        return ('for each entity e in \"%s\", selects that entity whose mapped int ~ \"%s\" and returns a set of seleceted entities' %(arg1,arg2))


def convertTable(variables, headers):
    variablesTable=[]
    m= 0
    for i in range(len(headers)):
        if m<len(variables[i]):
            m=len(variables[i])
    for i in range(m):
        d = OrderedDict()
        for j in range(len(headers)):
            if i<len(variables[j]):
                d.update({headers[j]:variables[j][i]})
            else:
                d.update({headers[j]:""})
        variablesTable.append(d)
    return variablesTable

def prog_to_string(program, variable_sequence):
    prog_string = []
    for i in range(len(program['program_type'])):
        ptype = program['program_type'][i]
        aindex = program['argument_index'][i]
        line = chr(65+i) + " = " + id_to_operator[ptype] + "("
        f = False
        for j in range(len(aindex)):
            if variable_sequence[aindex[j]]!="":
                f=True
                line += variable_sequence[aindex[j]] + ", "
        if f:
            line = line[:-2]
        line += ")"
        prog_string.append(line)
    return prog_string

def addStepProg(program, variable_sequence, variableTable, opID, argsID):
    op = id_to_operator[opID]
    args = [ variable_sequence[int(a)] for a in argsID ]
    program['program_type'].append(operators[op])
    ttype = variable_types[op_output_type[op]]
    print(ttype, file=sys.stdout)
    program['target_type'].append(ttype)
    program['target_table_index'].append(len(variableTable[ttype]))
    program['target_index'].append(len(variable_sequence))
    variableTable[ttype].append(chr(64+len(program['target_type'])))
    variable_sequence.append(chr(64+len(program['target_type'])))
    obtainedArgsTypes = []
    argTableIndex = []
    argIndex = []
    for arg in args:
        if arg=="":
            obtainedArgsTypes.append(0)
            argTableIndex.append(0)
            argIndex.append(0)
            continue
        for i in range(9):
            for j in range(len(variableTable[i])):
                if variableTable[i][j]==arg:
                    obtainedArgsTypes.append(i)
                    argTableIndex.append(j)
                    break
        for i in range(len(variable_sequence)):
            if variable_sequence[i]==arg:
                argIndex.append(i)
    while len(obtainedArgsTypes)<3:
        argTableIndex.append(0)
        argIndex.append(0)
        obtainedArgsTypes.append(0)
    program['argument_type'].append(tuple(obtainedArgsTypes))
    program['argument_table_index'].append(tuple(argTableIndex))
    program['argument_index'].append(tuple(argIndex))
    print((program, variable_sequence, variableTable), file=sys.stdout)
    return (program, variable_sequence, variableTable)

def checkStep(variableTable, variable_sequence, opID, argsID):
    op = id_to_operator[opID]
    print(op, file=sys.stdout)
    args = [ variable_sequence[int(a)] for a in argsID ]
    print(args, file=sys.stdout)
    if op not in program_argument_type.keys():
        return False
    argsTypeID = [variable_types[t] for t in program_argument_type[op]]
    print(argsTypeID, file=sys.stdout)
    obtainedArgsTypes = []
    for arg in args:
        if arg=="":
            obtainedArgsTypes.append(0)
            continue
        for i in range(9):
            for j in range(len(variableTable[i])):
                if variableTable[i][j]==arg:
                    obtainedArgsTypes.append(i)
                    break
    print(obtainedArgsTypes, file=sys.stdout)
    if not len(argsTypeID)==len(obtainedArgsTypes):
        return False
    for i in range(len(argsTypeID)):
        if not argsTypeID[i]==obtainedArgsTypes[i]:
            return False
    print("here", file=sys.stdout)
    return True

def initialise_prog():
    program={}
    program['program_type'] = []
    program['target_type'] = []
    program['target_table_index'] = []
    program['target_index'] = []
    program['argument_type'] = []
    program['argument_table_index'] = []
    program['argument_index'] = []
    return program

def initialise_variables(entities, relations, types, ints):
    variables = [[] for i in range(9)]
    variables[0].append("")
    for e in entities:
        if e!=None:
            variables[1].append(e)
    for e in relations:
        if e!=None:
            variables[2].append(e)
    for e in types:
        f=True
        for r in relations:
            if r==e:
                f=False
        if e!=None:
            if f:
                variables[3].append(e)
            else:
                print('found duplicate', file=sys.stdout)
                variables[3].append(e+'\'')
    for e in ints:
        if e!=None:
            variables[4].append(e)
    return variables

@app.route('/getQuestion', methods=['POST'])
def getQuestion():
    print("here")
    state = json.loads(flask.request.form["json"])
    print(questionTypes[int(state["qtype"])], file=sys.stdout)
    ques = env.fetch_question(None, questionTypes[int(state["qtype"])])
    print(ques)
    question = ques[0][0]
    entities = ques[1][0]
    relations = ques[3][0]
    types = ques[2][0]
    ints = ques[4][0]
    if len(ques)<6:
        ques_id = 0
    else:
        ques_id = ques[5]
    cipitr_prog = ques[6]
    cipitr_reward = ques[7]
    variables = initialise_variables(entities, relations, types, ints)
    variables_table = convertTable(variables, var_types)
    operators_table = convertTable(operators_dict, operators_types)
    variables_list = [j for i in variables for j in i]
    response = {
            'question': question,
            'questionID': ques_id,
            'qtypes':questionTypes,
            'operators': [k for k,v in sorted(operators.items(), key=operator.itemgetter(1))],
            'operators_ids':operators,
            'operator_help':operator_help,
            'operators_types':operators_types,
            'operators_dict':operators_table,
            'operators_output_type': op_output_type,
            'variable_type_info':variable_type_info,
            'var_types':var_types,
            'variables':variables,
            'variables_table': variables_table,
            'variables_list': variables_list,
            'prog':initialise_prog(),
            'prog_string':[""],
            'program_arguments_string':program_arguments_string,
            'cipitr_prog':cipitr_prog,
            'cipitr_reward':cipitr_reward,
            'num_actions_rejected_per_timestep':ques[8],
            'num_actions_explored_per_timestep':ques[9],
            'feasible_action_space_size':ques[10]
            }
    print(response, file=sys.stdout)
    res = flask.jsonify(response)
    return res

@app.route('/getReward', methods=['POST'])
def getReward():
    print("here", file=sys.stdout)
    state = json.loads(flask.request.form["json"])
    print(state, file=sys.stdout)
    d = {}
    d['argument_type'] = state['prog']['argument_type']
    d['argument_table_index'] = state['prog']['argument_table_index']
    d['target_type'] = state['prog']['target_type']
    d['target_table_index'] = state['prog']['target_table_index']
    d['program_type'] = state['prog']['program_type']
    print(d, file=sys.stdout)
    reward = env.step(state["questionID"], questionTypes[int(state["qtype"])], d)
    print(reward[0][0], file=sys.stdout)
    response = {
            'reward':reward[0][0]
            }
    res = flask.jsonify(response)
    return res

@app.route('/addStep', methods=['POST'])
def addStep():
    print("here", file=sys.stdout)
    state = json.loads(flask.request.form["json"])
    print(state, file=sys.stdout)
    print(state["variables"], file=sys.stdout)
    print( state["selectedOpIndex"] , file=sys.stdout )
    print( [state["selectedArg1"],state["selectedArg2"],state["selectedArg3"]], file=sys.stdout )
    variable_sequence = state['variables_list']
    if checkStep(state["variables"], state["variables_list"], state["selectedOpIndex"], [state["selectedArg1"],state["selectedArg2"],state["selectedArg3"]]):
        print("True")
        (prog, variables_list, variables) = addStepProg(state['prog'], state['variables_list'], state['variables'], state["selectedOpIndex"], [state["selectedArg1"],state["selectedArg2"],state["selectedArg3"]])
        prog_string = prog_to_string(prog, variables_list)
        variables_table = convertTable(variables, var_types)
        response = {
                'variables':variables,
                'variables_table': variables_table,
                'variables_list': variables_list,
                'prog':prog,
                'prog_string':prog_string,
                'message':step_message(id_to_operator[state["selectedOpIndex"]], variable_sequence[int(state["selectedArg1"])], variable_sequence[int(state["selectedArg2"])], variable_sequence[int(state["selectedArg3"])])
                }
        print(response, file=sys.stdout)
    else:
        print("False")
        response = {
                'variables':state["variables"],
                'variables_table': state["variables_table"],
                'variables_list': state["variables_list"],
                'prog':state["prog"],
                'prog_string':state["prog_string"],
                'message':'Check step!'
                }
        print(response, file=sys.stdout)
    res = flask.jsonify(response)
    print(res, file=sys.stdout)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

