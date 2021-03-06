from coopr.pyomo import *

model = AbstractModel()

model.I = Set()
model.J = Set()

model.x = Var(model.I, model.I, within=Boolean)
model.f = Var(model.I, model.I, model.J, within=NonNegativeReals)

model.c = Param(model.I, model.I)
model.n = Param()

def con1_rule(model, i):
    return sum(model.x[i,j] for j in model.I if j != i) == 1

def con2_rule(model, i):
    return sum(model.x[j,i] for j in model.I if j != i) == 1

model.con1 = Constraint(model.I, rule=con1_rule)
model.con2 = Constraint(model.I, rule=con2_rule)

def con3_rule(model, k):
    return sum(model.f[1,i,k] for i in model.J if (1,i,k) in model.f) == 1

def con4_rule(model, k):
    return sum(model.f[i,k,k] for i in model.I if (i,k,k) in model.f) == 1

model.con3 = Constraint(model.J, rule=con3_rule)
model.con4 = Constraint(model.J, rule=con4_rule)


def con5_rule(model, k, i):
    if i == k:
        return Constraint.Skip
    else:
        return sum(model.f[j,i,k] for j in model.I if (j,i,k) in model.f) == sum(model.f[i,j,k] for j in model.I if (i,j,k) in model.f)

model.con5 = Constraint(model.J, model.J, rule=con5_rule)

def con6_rule(model, i, j, k):
    return model.f[i,j,k] <= model.x[i,j]

model.con6 = Constraint(model.I, model.I, model.J, rule=con6_rule)

def obj_rule(model):
    return sum(model.c[i,j]*model.x[i,j] for i in model.I for j in model.I)

model.obj = Objective(rule=obj_rule, sense=minimize)
