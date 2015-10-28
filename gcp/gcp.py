from coopr.pyomo import *

model = AbstractModel()

model.V = Set()
model.E = Set(within=model.V*model.V)
model.K = Set()
model.x = Var(model.V, model.K, within=Boolean)
model.y = Var(model.K, within=Boolean)

def con1_rule(model, i):
    return sum(model.x[i,k] for k in model.K) == 1

model.con1 = Constraint(model.V, rule=con1_rule)

def con2_rule(model,i,j,k):
    return model.x[i,k] + model.x[j,k] <= model.y[k]

model.con2 = Constraint(model.E, model.K, rule=con2_rule)

def con3_rule(model, k):
    return model.y[k] >= model.y[k+1]

model.con3 = Constraint(model.K)

def obj_rule(model):
    return sum(model.y[k] for k in model.K)

model.obj = Objective(rule=obj_rule, sense=minimize)
