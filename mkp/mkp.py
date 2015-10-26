from coopr.pyomo import *

model = AbstractModel()

model.I = Set()
model.J = Set()
model.a = Param(model.I, model.J)
model.b = Param(model.I)
model.v = Param(model.J)
model.x = Var(model.J, within=Boolean)

def con_rule(model, i):
    return sum(model.a[i,j]*model.x[j] for j in model.J) <= model.b[i]

model.con = Constraint(model.I, rule=con_rule)

def obj_rule(model):
    return sum(model.v[j]*model.x[j] for j in model.J)

model.obj = Objective(rule=obj_rule, sense=maximize)
