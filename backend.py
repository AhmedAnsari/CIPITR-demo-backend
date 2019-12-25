from demo import Environment
import json
params_file = 'parameters/param_demo.json'
param = json.load(open(params_file))
env = Environment(param,'Train')

