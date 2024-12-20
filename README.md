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
![image](https://github.com/user-attachments/assets/226dc2e4-778c-4583-9baa-6f6cff77317a)


2) By applying Nearest Neighbour Heuristic
![image](https://github.com/user-attachments/assets/a3a7773a-7e98-4b94-b1c7-403d02eba197)


3) By applying Genetic Algorithm
