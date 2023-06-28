# CircuitCrunchers

## Chips and Circuits

A chips consists of several gates that should be connected with eachother with wires. The less wire that have to be 
used for a chip the cheaper it is to make and the faster the chip is. You want to avoid that wires cross eachtoher 
and with a lot of wires this can get messy very fast. In chips and circuits a good way of connecting all the gates 
has to be found with the help of algoritms and heuristics. The chips consists of 8 layers where the wires can be put. 

## Algorithms ##
- **Random**: The random algorithm randomly lays wireparts into one direction and will stop when it has reached the end gate. The 2D option does the same in just two dimensions

- **Greedy**: The greedy algorithm looks for each step what direction is the most favourable. The algorithm oes this by comparing the current position of the end of the wire with the position of the gateB. First the algoritm will go into the x direction if it differs from the x coordinate of gateB then the y direction and after that the z direction.


- **Astar**: The a* algorithm uses nodes that all have an Fcost. The Fcost is the sum of the Gcost and the Hcost. The Gcost in this is the number of steps the node is away from the startNode. The Hcost is the heuristic value calculated by the distance from the node to the endNode that makes the algorithm find a solution faster. The algorithm calculates the Fcost for all adjacent nodes and chooses the node with the lowest Fcost to continue with. It does this until it finds the endNode and thus found a path. By further increasing the Fcost of certain nodes, you can control the algorithm because it will check these nodes later and will therefore possibly find another path sooner.

- **Hillclimber**: The hillclimber algotithm uses the greedy or astar algorithm as a basis and randomly takes one wire of that solution. This wire will then randomly be laid differently and if the cost is better, it will keep the change. The add-on of simulated annealing will keep a bit of randomness in the decision.

## Sorting Orders ##
- **Basic**: This sorting order just takes the unchanged netlist connections from top to bottom.
  
- **Reverse**: Reverse sorting order takes the basic order in the netlists and merely reverses it (essentially starting at the bottom).
  
- **Random**: Random sorting order sorts the netlist in a random way, every time it is run will give a different order of the netlist.
  
- **Short**: This sorting order sorts the netlists by the distance between the two gates that it is refering to. In this case starting with the shortest distances going to the longest.
 
- **Long**: This order is the complete reverse of the "Short" sorting order, ordering from longest to shortest distance between the two gates.
  
- **Least-connections**: Least connections orders the netlist based on how many connections one of the two gates has. So for example if we are talking about connection 1 from gate A to B. Where A has 3 different connections to other gates and gate B has 4 connections, this connection will be sorted based on the number "4" compared to other connections. They are sorted from least to most connections.
  
- **Most-connections**: This sorting order is the complete opposite of "least-connections", ordering the connections from most to least connections.
  
- **Sum-lowest**: Similar to the least- and most-connections, however in this sorting method it sorts based on the sum of both gates' connection count. In the case of the example given in "Least-connections" this would result in 4 + 3 = 7 connections. The connections will be sorted from lowest to highest sum.
  
- **Sum-highest**: This sorting order is the complete opposite of the "Sum-lowest" sorting order, in this case ordering the connections from highest to lowest sum.
  
- **Middle**: Sorts the connections based on their proximity to the middle of the chip. This is calculated by checking what the middle of the chip is and then for every connection, takes the closest gate of the two and calculates it's distance to the middle. Based on this distance , the connections will be sorted from shortest distance to longest.
  
- **Inter-quadrant**: Inter quadrant sorting method sorts on two factors. Before it can sort ,it divides the chip into 4 equal quadrants (dividing from the middle point). Then it sorts on the first factor, the position of the two gates. It divides all the connections based on whether the two gates are in the same quadrant or whether they are in different quadrants. These are then also sorted on their distance from shortest to longest.
  
- **Intra-quadrant**: Intra quadrant is the complete opposite of the "Inter-quadrant" sorting method, so starting with the longest connections between gates in different quadrants all the way to the shortest connections between gates in the same quadrant.
  
- **Manhattan**: Manhattan is mainly used in grid like objects, it calculates the distance slightly different than normally. It does this by taking the absolute distance between the x coordinate of both gates and the y coordinate for both gates and adding them together. the connections are ordered from shortest to longest manhattan distance.
  
- **X**: Sorts the connections based on their x coordinate (the lowest of the two gates) from lowest x to highest x.
  
- **Y**: Sorts the connections based on their y coordinate (the lowest of the two gates) from lowest y to highest y.
  
- **X-rev**:
- **Y-rev**:
- **Weighted**:
- **Weighted-rev**:


# Experiments

## Use
How to use the test function:
 
**If you want to test the algorithm:**
```shell
python3 main.py test algorithm
```

**If you want to test the order:**
```shell
python3 main.py test order
```

**In both cases you will be asked to input different things:**

**Netlist**: Here you have to choose a netlist, which is a number from 1 to 9 or all

**Algorithm:** Here you can choose between all algorithms:

- random
- random2D
- hillclimber
- (simulated annealing)
- astar

**For random/random2D or simulated annealing:** 
- Choose how often you want the algorithm to run

**For astar:** 
- Choose a **version** of astar like normal or optimal

**For algorithms**:
- It should start to run now

**For order**:
- Choose all will test all orders once
- Choose random will run random order n times 


## Output
**For tests that have to be runned more than once (e.g. random):**

- CSV output with the costs
- A histogram with the average 

**For tests that have to runned only once:**

- CSV output with the cost 
- Plot with the wires and the cost

## Auteurs

- Juri
- Anna
- Martijn

