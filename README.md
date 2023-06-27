# CircuitCrunchers

## Chips and Circuits

## Experiments

## Use
How to use the test function:

**if you want to test the algorithm:**
1. run "python3 main.py test order"

**if you want to test the order:**
1. run "python3 main.py test order"

**both:**

2. You will be asked to input different things: 

**Netlist**: Here you have to choose a netlist, which is a number from 1 to 9 or all

**Algorithm:** Here you can choose between all algorithms:

random
random2D
hillclimber
(simulated annealing)
astar

if you choose random/random2D or simulated annealing you have to choose how often you want it to run

if you choose astar you have to choose a **version** of astar like:

normal 
...

**for algorithms**:
It should start to run now

**for order**:
after that you have to choose **all or random:** either you test all the orders, or just the random n times 

then it should start to run

## Output
If you have tested something that requires more than once to run (e.g. random)
for the netlists that you entered you will get:

1. CSV output with the costs
2. A histogram with the average 

if you have run something that only needs to run one time you will get:

1. CSV output with the cost 
2. Plot with the wires and the cost

