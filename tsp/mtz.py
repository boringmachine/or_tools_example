from coopr.pyomo import *

model = AbstractModel()

model.I = Set()
model.J = Set()

model.x = Var(model.I, model.I, within=Boolean)
model.u = Var(model.I, within=NonNegativeReals)

model.n = Param()
model.c = Param(model.I, model.I)

def con1_rule(model, i):
    return sum(model.x[i,j] for j in model.I if j != i) == 1

def con2_rule(model, i):
    return sum(model.x[j,i] for j in model.I if j != i) == 1

model.con1 = Constraint(model.I, rule=con1_rule)
model.con2 = Constraint(model.I, rule=con2_rule)

def con3_rule(model, i, j):
    if i == j:
        return Constraint.Skip
    else:
        return model.u[i]-model.u[j]+(model.n-1)*model.x[i,j]+(model.n-3)*model.x[j,i] <= model.n -2

model.con3 = Constraint(model.I, model.J, rule=con3_rule)

def con4_rule(model, i):
    return -model.x[1,i]-model.u[i]+(model.n-3)*model.x[i,1]<=-2

def con5_rule(model, i):
    return -model.x[i,1]+model.u[i]+(model.n-3)*model.x[1,i]<=model.n-2

model.con4 = Constraint(model.J, rule=con4_rule)
model.con5 = Constraint(model.J, rule=con5_rule)

def obj_rule(model):
    return sum(model.c[i,j]*model.x[i,j] for i in model.I for j in model.J)

model.obj = Objective(rule=obj_rule, sense=minimize)
