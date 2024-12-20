#importing dependencies
from gurobipy import GRB, Model, quicksum
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from color import Color


#parameters of the problem
n = 10 #number of customers (Update for larger instances)
d = [i for i in range(n+1) if i != 0] #List of customers excluding depots
nodes = [0] + d + [n+1] #list of all nodes including depots
arcs = [(i,j) for i in nodes for j in nodes if i!=j] #every possible arcs
v = 5 #number of vehicles (Update for larger instances)

#Times Windows {a;b}:
a = {0:0,   1:70,  2:70,  3:50,  4:50,  5:70,  6:50,  7:50,  8:50,  9:35,  10:40,  11:0}                #begin of Starting the service times for each node                                  
b = {0:300, 1:140, 2:190, 3:180, 4:180, 5:190, 6:180, 7:180, 8:180, 9:260, 10:280, 11:300}              #end of Starting the Service times for each node

#Service Times (S): 
s = {0:0, 1:10, 2:20, 3:30, 4:20, 5:30, 6:30, 7:50 ,8:60 ,9:20 ,10:40, 11:0}                            #Service Times for each VP

import random
'''
#Let's type in time windows {a:b}
#where "a" is the starting of starting of service time for each node
#where "b" is the ending of starting of service time for each node

seed = 0
# a
list_cust = []
for i in range(0,n + 2):
    add = list_cust.append(i)
list_cust

start_tw = [random.randint(1, 10) * 5 for _ in range(n)]
start_tw = [0] + start_tw + [0]

a = dict(zip(list_cust, start_tw))
print(a)

# b

end_tw = [random.randint(10, 50) * 5 for _ in range(n)]
end_tw = [0] + end_tw + [0]

b = dict(zip(list_cust, end_tw))
print(b)

#service time (s) at each customer

seed = 0
service_time = [random.randint(0, 20)*5 for _ in range(n)]
service_time = [0] + service_time + [0]

s = dict(zip(list_cust, service_time))
'''

#List of vehicles/number of vehicles
vehicles = []
for i in range(v+1):
    veh = vehicles.append(i)
vehicles = vehicles[1:]
vehicles

#Let's Randomize Coordinates of customers we need to deliver to!
seed = 1
#X-coordinates
# X = [random.randint(1, 200) for i in range(n) ] 
# X = [100] + X + [100]

#Y-Coordinates
# Y = [random.randint(1, 200) for i in range(n) ] 
# Y = [100] + Y + [100]

# X = [55, 10, 80, 85, 65, 5 , 80 ,50, 55, 145,140, 55]                                                   #Fixed X Coordinates
# Y = [70, 35, 5 , 105,95, 100,60 ,85, 25, 80, 115, 70]  
# we have 0 in starting and ending to depict depots (or we can add any value if we need)
X = [100, 55, 50, 24, 141, 128, 99, 21, 69, 132, 161, 100]
Y =  [100, 152, 59, 36, 29, 71, 79, 165, 163, 163, 77, 100]
# Cust  D   1   2   3   4   5   6    7    8   9   10   D

#Travelling time - , 
distance_matirx = {(i, j): np.hypot(X[i] - X[j], Y[i] - Y[j]) for i in nodes for j in nodes if i != j}
cost_per_dist = 0.4
cost_matrix = {(i, j): distance_matirx[i,j]*cost_per_dist for i in nodes for j in nodes if i != j}
#initiating a model
model = Model("CVRPTW")
model.ModelSense  = GRB.MINIMIZE #redundant but looks cool

arc_var = [(i, j, k) for i in nodes for j in nodes for k in vehicles if i!=j]
arc_time = [(i, k) for i in nodes for k in vehicles]

#adding our Decision Variables
x = model.addVars(arc_var, vtype=GRB.BINARY, name='x')
t = model.addVars(arc_time, vtype=GRB.CONTINUOUS, name='t')
w = model.addVar(vtype=GRB.CONTINUOUS, name='w')

#adding our Objection Function
#Multi-Objective Optimization

#1st Objective - Reduce the distance being truth to time windows
model.setObjectiveN(quicksum(distance_matirx[i,j]* x[i,j,k] for i, j, k in arc_var), 0, priority = 2)
#2nd Objective - Reduce the total cost while being truth to time windows
model.setObjectiveN(quicksum(cost_matrix[i, j]*x[i,j,k] for i, j, k in arc_var), 1, priority = 1)


#adding our Constraints
#1 - Visiting each node only once by one vehicle
model.addConstrs(quicksum(x[i, j, k]for j in nodes for k in vehicles if i!=j and j!=0) == 1 for i in d)

#2 - Each Vehicle starts at depot (0) & ends at depot (n+1)
model.addConstrs(quicksum(x[0, j, k] for j in nodes if j != 0) == 1 for k in vehicles)
model.addConstrs(quicksum(x[j, (n+1), k] for j in nodes if j != (n+1)) == 1 for k in vehicles)

#3 - Flow conservation at each node
model.addConstrs(quicksum(x[i,j,k] for j in nodes if j != i) - quicksum(x[j,i,k] for j in nodes if j != i) == 0 for i in d for k in vehicles)

#4 - Time windows
model.addConstrs((t[i, k] + (distance_matirx[i, j] + s[i])*x[i, j, k]) <= (t[j, k] + b[i]*(1 - x[i, j, k])) for i in nodes for j in nodes for k in vehicles if i!=j)

#5 - Arrival time within time windows
model.addConstrs((a[i]*quicksum(x[i,j,k] for j in nodes if i != j)) <= t[i,k] for i in d for k in vehicles)
model.addConstrs(t[i,k] <= b[i]*quicksum(x[i,j,k] for j in nodes if i != j) for k in vehicles for i in d)


#6 - Depot Arrival within time windows
model.addConstrs(a[i] <= t[i,k] for k in vehicles for i in nodes if i == 0 or i == (n+1))
model.addConstrs(t[i,k] <= b[i] for k in vehicles for i in nodes if i == 0 or i == (n+1))

#7 - Workload balancing across vehicles
model.addConstrs(quicksum(s[i]*x[i,j,k] for i in nodes for j in nodes if i != j) - quicksum(s[i]*x[i,j,l] for i in nodes for j in nodes if i != j) <= w \
    for k in vehicles for l in vehicles if k != l)

#8 - Non-negative workload
model.addConstr(w >= 0)

model.optimize()

# model.computeIIS()
# model.write("model.ilp")

#Printing the Variables
print("Objective Value: " ,str(round(model.ObjVal, 2)))
for v in model.getVars():
    if v.x > 0.9: 
        print(str(v.VarName)+"="+str(v.x))


#Routes for the Graphic Illustration
routes = [ ]
truck = [ ]
K = vehicles
N = nodes
for k in vehicles: 
    for i in nodes: 
        if i != 0 and x[0,i,k].x>0.9:
            aux = [0,i]
            while i != n+1: 
                j = i
                for h in nodes:
                    if j != h and x[j,h,k].x>0.9:
                        aux.append(h)
                        i = h
            routes.append(aux)
            truck.append(k)


#Times for the Graphical Illustration
times = list()
for k in range(len(routes)):
    help = []
    for j in range(len(routes[k])):
        l = k + 1
        #print(k, routes[k][j], ": ", t[routes[k][j],l].x)
        help.append(t[routes[k][j],l].x)
    times.append(help)



#Graphic Illustration (Matplotlib)
plt.figure(figsize=(12,5))
plt.scatter(X,Y, color="blue")
plt.scatter(X[0], Y[0], color='red', marker='D')
plt.scatter(X[11], Y[11], color='red', marker='D') 

#Routes: 
for r in range(len(routes)):
    for n in range(len(routes[r]) - 1):
        i = routes[r][n]
        j = routes[r][n+1]
        plt.plot([X[i], X[j]],[Y[i], Y[j]], color=Color[r], alpha = 0.3)

#Time when the Vehicle starts the Serivce at each Visit-Point
for r in range(len(times)):
    for n in range(len(times[r])):
        i = routes[r][n]
        if i == 11 or i == 0:
            continue
        else: 
            plt.annotate('$t_{%d}=%d$\n'%(i,times[r][n]),(X[i]+1,Y[i]))

#Legend
patch = [mpatches.Patch(color=Color[n], label="Vehicle " + str(truck[n])) for n in range(len(truck))]
plt.legend(handles=patch,loc='best')

#Time Windows for each Visit-Point
plt.annotate("\nDC|$t_{%d}$ = (%d$,%d$)" %(0, a[0], b[0]), (X[0]-1,Y[0]-5.5))
for i in d: 
    plt.annotate('\n$t_{%d}$ = (%d$,%d$)' %(i, a[i], b[i]), (X[i]+1, Y[i]))

plt.xlabel("Distance X")
plt.ylabel("Distance Y")
plt.title("VRPTW ", fontsize=15)
plt.show()

#Lets focus on Heuristics now!
''' 
we will try the following heuristics:
1) Greedy Search
2)

'''
