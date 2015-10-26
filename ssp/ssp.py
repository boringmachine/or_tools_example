from coopr.pyomo import *

model = AbstractModel()

model.V = Set()
model.E = Set(within=model.V*model.V)

model.x = Var(model.V, within=Boolean)

def con_rule(model,i,j):
    return model.x[i]+model.x[j]<=1

model.con = Constraint(model.E, rule=con_rule)

def obj_rule(model):
    return sum(model.x[i] for i in model.V)

model.obj = Objective(rule=obj_rule, sense=maximize)
