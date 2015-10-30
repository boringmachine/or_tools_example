from coopr.pyomo import *

model = AbstractModel()

model.I = Set()
model.J = Set()

model.x = Var(model.I, model.I, within=Boolean)
model.f = Var(model.I, model.I, within=NonNegativeReals)

model.n = Param()
model.c = Param(model.I, model.I)

def con1_rule(model, i):
    return sum(model.x[i,j] for j in model.I if j != i) == 1

def con2_rule(model, i):
    return sum(model.x[j,i] for j in model.I if j != i) == 1

model.con1 = Constraint(model.I, rule=con1_rule)
model.con2 = Constraint(model.I, rule=con2_rule)

def con3_rule(model):
    return sum(model.f[1, j] for j in model.J) == model.n-1

model.con3 = Constraint(rule=con3_rule)

def con4_rule(model, i):
    return sum(model.f[j,i] for j in model.I if j != i) - sum(model.f[i,j] for j in model.I if j != 1) == 1

model.con4 = Constraint(model.J, rule=con4_rule)

def con5_rule(model, j):
    return model.f[1,j] <= (model.n-1)*model.x[1,j]

model.con5 = Constraint(model.J, rule=con5_rule)

def con6_rule(model, i, j):
    if i==j:
        return Constraint.Skip
    else:
        return (model.f[i,j] <= (model.n-2)*model.x[i,j])

model.con6 = Constraint(model.J, model.J, rule=con6_rule)

def obj_rule(model):
    return sum(model.c[i,j]*model.x[i,j] for i in model.I for j in model.I)


model.obj = Objective(rule=obj_rule, sense=minimize)
