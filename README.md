# MS5570_Heuristics_VRPTW

### Steps Involved in this Project

Steps Involved in this Project:

START
- Define Parameters
- Initiating a model
- Adding our Decision Variables
- Adding our Objection Function
- Optimizing our model through Gurobi
- Printing results
- Making a visualization
- Noting computational speed at larger instances
- Making Construction Heuristics 	
- Solving the Model using simple construction Heuristics
- Solving the above model using Meta-Heuristics like Genetic algorithm
- Comparing all the results together & generate observations in the form of report considering larger instances of the problem

END

### Data
"final.py" file can be implemented in 2 ways,
1) Fixed: This is the way we used in this project, here the data have been put manually to understand how our VRPTW model works.
2) Random: There are some sections in the "final.py" file which is commented out, those can be used to help you generate random values for the VRPTW study.

Now, Let's get to Mixed Interger Linear Programming Modelling of the case:

### MILP Model

- $N = [0,1,2....n]$; 0 - Depot, (1 to n) - Customers
- $K = [1,2,....k]$;  Set of Vehicles

Parameters:

- $d_i$ - Demand at customer i
- $C_k$ - Capacity of Vehicle
- $[e_i,~l_i]$ - Time window for customer i ($e_i$ - earliest time, $l_i$ - latest time)
- $s_i$ - Service time at customer i
- $t_{ij}$ - Travel time from node i to j
- $C_{ij}$ - Travel cost from node i to j(Proportional to distance)

Decision Variables:

- $x^k_{ij}\in\{0,1\}$; [1 - Vehicle k travels from i to j | 0 - otherwise]
- $u^k_i  \geq  0$; Load of vehicle k after visiting node i
- $k^k_i  \geq  0$; Arrival time of vehicle k after visiting node i

Objective Function:

Minimize Total Travel Cost = 
- $min \Sigma^k_{k=1}\Sigma^i_{i=0}\Sigma^j_{j=1}~C_{ij}X^k_{ij}~~~\forall j\neq i$

Constraints:

1) Each Customer is Visited Exactly Once

- $\Sigma_k\Sigma_iX^k_{ij}=1 \forall j \in N, j\neq0$

2) Flow Conservation

- $\Sigma_jX^k_{ij} = \Sigma_jX^k_{ji}, \forall i \in N, \forall k \in K$

3) Vehicle Starts & Ends at Depot

- $\Sigma^n_{j=1}X^k_{0j}=1, \forall k \in K$
- $\Sigma^n_{i=0}X^k_{jo}=1, \forall k \in K$ 

4) Vehicle Capacity Constraint

- $u^k_j\geq u^k_i + d_j - C_k(1-x^k_{ij})$
- $0 \leq u^k_i \leq C_k$ - Ensures Load is within Vehicle Capacity at all times

5) Time Window Constraint

- $t^k_j\geq t^k_i + s_i + t_{ij} - M(1-x^k_{ij})$
- $e_i \leq t^k_i \leq l_i$ - Time window bounds

### Results:

Here are some results with given data:
1) Traditional MILP using Gurobi

Multi-objectives: solved in 1.98 seconds (2.81 work units), solution count 1

Objective Value:  360.27
x[0,1,2]=1.0
x[0,3,4]=1.0
x[0,4,3]=1.0
x[0,6,1]=1.0
x[0,9,5]=1.0
x[1,7,2]=1.0
x[2,11,4]=1.0
x[3,2,4]=1.0
x[4,10,3]=1.0
x[5,11,1]=1.0
x[6,5,1]=1.0
x[7,11,2]=1.0
x[8,11,5]=1.0
x[9,8,5]=1.0
x[10,11,3]=1.0
t[1,2]=70.0
t[2,4]=164.07104870241284
t[3,4]=99.35793878699377
t[4,3]=81.9878039710785
t[5,1]=110.08321791298157
t[6,1]=50.0
t[7,2]=116.40054944640235
t[8,5]=153.6611633077174
t[9,5]=70.66116330771808
t[10,3]=153.9878039710785
t[11,1]=180.3945066544728
t[11,2]=268.70401957327516
t[11,3]=259.17982802310496
t[11,4]=248.7317013437202
t[11,5]=283.8751220338848
w=30.0
![VRPTW_MILP_figure](https://github.com/user-attachments/assets/c22722d0-859a-48ea-a108-62ff80c23da1)



3) By applying Nearest Neighbour Heuristic

I have used “Nearest Neighbor” Approach in Heuristics for the problem to get feasible solution, which is not optimal of course.
Solution we get in this approach is following:
Vehicle 1 route: [0, 10, 5, 11]
Distance: 73.85
Vehicle 2 route: [0, 8, 7, 11]
Distance: 150.35
Vehicle 3 route: [0, 9, 11]
Distance: 70.66
Vehicle 4 route: [0, 4, 6, 11]
Distance: 86.32
Vehicle 5 route: [0, 3, 2, 11]
Distance: 99.37
Total Distance: 480.56

Here, 0 and 11 are same Depot, it has been put that way to easily understand the code .

![image](https://github.com/user-attachments/assets/a3a7773a-7e98-4b94-b1c7-403d02eba197)


4) By applying Genetic Algorithm
