from coopr.pyomo import *

model = AbstractModel()

model.I = Set()
model.J = Set()

model.s = Param(model.I)
model.B = Param()

model.x = Var(model.I, model.J, within=Boolean)
model.y = Var(model.J, within=Boolean)

def con1_rule(model, i):
    return sum(model.x[i,j] for j in model.J) == 1

def con2_rule(model, j):
    return sum(model.s[i]*model.x[i,j] for i in model.I) <= model.B * model.y[j]

def con3_rule(model, i, j):
    return model.x[i,j] <= model.y[j]

model.con1 = Constraint(model.I, rule=con1_rule)
model.con2 = Constraint(model.J, rule=con2_rule)
model.con3 = Constraint(model.I, model.J, rule=con3_rule)

def obj_rule(model):
    return sum(model.y[j] for j in model.J)

model.obj = Objective(rule=obj_rule, sense=minimize)
