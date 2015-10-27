from coopr.pyomo import *

model = AbstractModel()

model.I = Set()
model.J = Set()

model.y = Var(model.J, within=Boolean)
model.x = Var(model.I, model.J, within=NonNegativeReals)
model.d = Param(model.I)
model.M = Param(model.J)
model.f = Param(model.J)
model.c = Param(model.I, model.J)

def con1_rule(model, i):
    return sum(model.x[i,j] for j in model.J) == model.d[i]

model.con1 = Constraint(model.I, rule=con1_rule)

def con2_rule(model, j):
    return sum(model.x[i,j] for i in model.I) <= model.M[j]*model.y[j]

model.con2 = Constraint(model.J, rule=con2_rule)

def con3_rule(model, i, j):
    return model.x[i,j] <= model.d[i]*model.y[j]

model.con3 = Constraint(model.I, model.J, rule=con3_rule)

def obj_rule(model):
    return sum(model.f[j]*model.y[j] for j in model.J) + sum(model.c[i,j]*model.x[i,j] for i in model.I for j in model.J)

model.obj = Objective(rule=obj_rule, sense=minimize)
