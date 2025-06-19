# IDLEE - Case Study on Optimizing Vehicle Routing Problem with Time Windows

## What is Idlee & Co? 

Welcome to Idlee & Co, the South Indian breakfast franchise redefining your mornings, one plate at a time. At Idlee, our menu celebrates the rich variety of South Indian breakfast classics, but there’s one star that keeps our customers coming back—our legendary idli.

What sets Idlee apart? According to our customers, it’s the unbeatable freshness, soft texture, and mouthwatering taste of our idlis that make us the go-to destination for early morning breakfasts. The secret behind our irresistibly fresh idlis lies in our unique supply chain: every Idlee franchise receives freshly prepared batter each morning, ensuring that every idli served is as fresh as it gets and to maintain consistancy among all the franchises.

So, whether you’re a breakfast enthusiast or simply seeking the perfect start to your day, Idlee & Co promises a truly authentic and fresh South Indian breakfast experience—where “fresh” isn’t just a word, it’s our way of life.


### Scope of this Case Study:

Every food business sacrifices their food quality over reducing cost, which interm will increase their profit. 
What happens when a restaurant chain comes in & preaces for good and consistent food quality? where reducing cost may not be their first priority!?
This is where our case study comes in, This supply chain is designed for specific need presented by the stakeholders of the company.

What are the demands of the stakeholders? (This can be treated as direct (or) indirect constraints for our study)
1) Every Franchise should have same (consistent) idle batter
   - They tackle this by making the idli batter at one place & then distribute it to the franchises.
   - This is a verticle integretion for them as they sell idli batters in a manufactured packs in supermarkets as well. (Stakeholders wish to make use of their less utilized idly batter manufacturing plants)

2) Having all these constraint, keep the costs at minimum.
   (They 2nd Priority is to Reduce cost & make the whole supply chains's cost to the minimum)

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

We can also change the number of customers (or) the number of vehicles used for VRPTW to understand how the model works with larger instances.

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

\n
TSP is a NP-Hard problem, If the number of Variable increases, it will become infeasible to run this model. For this case, if the number of franchises increase by large, this code will become useless!\n

Now, for that not to happen, our only hope is to get a solution which is near optimal, hence we will take help of heuristics & meta heuristics. For heuristics, for now, I have designed it via Nearest Neighbor. For Meta-Heuristics, we are using Genetic algorithm.

### Results:

Here are some results with given data:
1) Traditional MILP using Gurobi

Multi-objectives: solved in 1.98 seconds (2.81 work units), solution count 1

This is the Gurobi Solution:
Objective Value:  360.27

![VRPTW_MILP_figure](https://github.com/user-attachments/assets/c22722d0-859a-48ea-a108-62ff80c23da1)



2) By applying Nearest Neighbour Heuristic

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


3) By applying Genetic Algorithm
   (will be updated soon)

#### Future Course of Work:
1) To refine this model & inject many more Objective functions to determine more stuff about VRPTW.
2) Input More number of various Heuristic solutions
3) Input More number of various Meta-Heuristic solutions
4) Try to input new constraints & visualize how each model reacts.


This Case Study was created & thought in accordance of:
##### MS5570_Heuristics_VRPTW

at last I would like to thank,
1) Prof. C.Rajendran (Course Instructor)

with regards,
Vivek Karna

