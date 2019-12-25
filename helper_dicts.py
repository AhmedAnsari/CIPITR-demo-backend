operator_help = {}
operator_help['gen_map_set'] = "gen_map_set(t1, r, t2) creates a map (or dict) object with each entity of type 't1' as keys and the set of entities of type t2 that is related to the key by 'r' as values.\n e.g: gen_map_set(river, flows through, country): for each river in the KB, it stores the set of countries that the river flows through"
operator_help['gen_set'] = "gen_set(e, r, t) creates a set object which consists of those entities of type t that are related to entity e by relation r. \n eg: gen_set(ganga, flows through, country): set of countries that ganga flows through"
operator_help['set_count'] = "set_count(set A) returns the number of entities in the set A"
operator_help['set_ints'] = "set_ints(set A, set B) returns the intersection the sets A, B"
operator_help['set_diff'] = "set_diffs(set A, set B) returns the difference of the sets A, B"
operator_help['set_union'] = "set_union(set A, set B) returns the union of the sets A, B"
operator_help['map_count'] = "map_count(Map_set A) for each entity in Map A, returns the count of the sets corresponding to that entity. eg: map_count({india:(ganga, brahmaputra), pakistan:(sindhu, ravi)}) returns {india:2, pakistan:2}"
operator_help['map_diff'] = "map_diff(Map_set A, Map_set B) for each e in both Map A,B, returns the difference of the sets corresponding to that entity"
operator_help['map_ints'] = "map_ints(Map_set A, Map_set B) for each e in both Map A,B, returns the intersection of the sets corresponding to that entity"
operator_help['map_union'] = "map_union(Map_set A, Map_set B) for each e in both Map A,B, returns the union of the sets corresponding to that entity"
operator_help['select_approx'] = "select_approx(Map_int A, int B) for each entity e in A, selects that entity whose mapped int ~ B and returns a set of seleceted entities"
operator_help['select_atleast'] = "select_atleast(Map_int A, int B) for each entity e in A, selects that entity whose mapped int >= B and returns a set of seleceted entities"
operator_help['select_atmost'] = "select_atmost(Map_int A, int B) for each entity e in A, selects that entity whose mapped int <= B and returns a set of seleceted entities"
operator_help['select_equal'] = "select_equal(Map_int A, int B) for each entity e in A, selects that entity whose mapped int = B and returns a set of seleceted entities"
operator_help['select_less'] = "select_less(Map_int A, int B) for each entity e in A, selects that entity whose mapped int < B and returns a set of seleceted entities"
operator_help['select_more'] = "select_more(Map_int A, int B) for each entity e in A, selects that entity whose mapped int > B and returns a set of seleceted entities"
operator_help['select_max'] = "select_max(Map_int A) for each entity e in A, selects that entity whose mapped int is the highest among all the enitites in A"
operator_help['select_min'] = "select_min(Map_int A) for each entity e in A, selects that entity whose mapped int is the lowest among all the enitites in A"
operator_help["none"] = "No action"
operator_help["terminate"] = "Terminate program"
operator_help["verify"] = "verify(e1, r, e2) returns a boolean flag indicating if entities e1, e2 are related by relation r in the KB. eg: verify(Donald Trump, president_of, america) returns a boolean flag True after checking that Donald Trump is president_of america"


variable_type_info = {}
variable_type_info['entity'] = 'Variable of type KB-entity'
variable_type_info['relation'] = 'Variable of type KB-relation'
variable_type_info['type'] = 'Variable of type KB-type'
variable_type_info['none'] = 'None type variable'
variable_type_info['int'] = 'Variable of type integer'
variable_type_info['bool'] = 'Variable of type boolean'
variable_type_info['set'] = "Variable of type set. A set(e, r, t) is a set object which consists of those entities of type 't' that are related to entity 'e' by relation 'r'"
variable_type_info['map_set'] = "Variable of type map_set. A map_set(t1, r, t2) is a dict object with each entity of type 't1' as keys and the set of entities of type 't2' that is related to the key by 'r' as values"
variable_type_info['map_int'] = "Variable of type map_int. It is a dict object with entities as keys and integers as values."


var_types = ["none", "entity", "relation", "type", "int", "bool", "set", "map_set", "map_int"]

questionTypes = ["simple", "verify", "quantitative count", "quantitative", "comparative count", "comparative", "logical"]

variable_types ={
    'bool': 5,
    'entity': 1,
    'int': 4,
    'map_set': 7,
    'map_int': 8,
    'none': 0,
    'relation': 2,
    'set': 6,
    'type': 3}

program_argument_type = {
    'gen_map_set': ['type', 'relation', 'type'],
    'gen_set': ['entity', 'relation', 'type'],
    'map_count': ['map_set'],
    'map_diff': ['map_set', 'map_set'],
    'map_ints': ['map_set', 'map_set'],
    'map_union': ['map_set', 'map_set'],
    'select_approx': ['map_int', 'int'],
    'select_atleast': ['map_int', 'int'],
    'select_atmost': ['map_int', 'int'],
    'select_equal': ['map_int', 'int'],
    'select_less': ['map_int', 'int'],
    'select_max': ['map_int'],
    'select_min': ['map_int'],
    'select_more': ['map_int', 'int'],
    'set_count': ['set'],
    'set_diff': ['set', 'set'],
    'set_ints': ['set', 'set'],
    'set_union': ['set', 'set'],
    'verify': ['entity', 'relation', 'entity'],
    'terminate': [],
    'none':[]}

operators_types = ["set", "map_set", "select", "bool", "others"]

operators_dict = [
    ['gen_set', 'set_count', 'set_diff', 'set_ints', 'set_union'],
    ['gen_map_set','map_count','map_diff','map_ints','map_union'],
    ['select_approx','select_atleast','select_atmost','select_equal','select_less','select_max','select_min','select_more'],
    ['verify'],
    ['none','terminate']
    ]

operators = {
    'gen_map_set': 2,
    'gen_set': 1,
    'map_count': 8,
    'map_diff': 11,
    'map_ints': 10,
    'map_union': 9,
    'none': 0,
    'select_approx': 19,
    'select_atleast': 14,
    'select_atmost': 15,
    'select_equal': 18,
    'select_less': 17,
    'select_max': 12,
    'select_min': 13,
    'select_more': 16,
    'set_count': 4,
    'set_diff': 7,
    'set_ints': 6,
    'set_union': 5,
    'terminate': 20,
    'verify': 3}

outputType = {
    'bool': ['verify'],
    'entity': ['select_max', 'select_min'],
    'int': ['set_count'],
    'map_set': ['gen_map_set', 'map_union', 'map_ints', 'map_diff'],
    'map_int': ['map_count'],
    'set': ['gen_set',
        'set_union',
        'set_ints',
        'set_diff',
        'select_atleast',
        'select_atmost',
        'select_more',
        'select_less',
        'select_equal',
        'select_approx'],
    'none': ['none', 'terminate']}

id_to_operator = {v: k for k, v in operators.iteritems()}

id_to_variable_type = {v: k for k, v in variable_types.iteritems()}

op_output_type = {o: k for k, v in outputType.iteritems() for o in v}

program_arguments_string = []
for i in range(21):
    x = program_argument_type[id_to_operator[i]]
    while len(x)<3:
        x.append('none')
    op = id_to_operator[i]
    program_arguments_string.append(op+"("+', '.join(x)+") -> " + op_output_type[op])

