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

