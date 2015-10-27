from coopr.pyomo import *

model = AbstractModel()

model.I = Set()
model.J = Set()

model.y = Var(model.J, within=Boolean)
model.x = Var(model.I, model.J, within=Boolean)
model.c = Param(model.I, model.J)
model.k = Param()

def con1_rule(model, i):
    return sum(model.x[i,j] for j in model.J) == 1

model.con1 = Constraint(model.I, rule=con1_rule)

def con2_rule(model, i, j):
    return model.x[i,j] <= model.y[j]

model.con2 = Constraint(model.I, model.J, rule=con2_rule)

def con3_rule(model):
    return sum(model.y[j] for j in model.J) == model.k

model.con3 = Constraint(rule=con3_rule)

def obj_rule(model):
    return sum(model.c[i,j]*model.x[i,j] for i in model.I for j in model.J)

model.obj = Objective(rule=obj_rule, sense=minimize)

