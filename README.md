# Structural Outline

We want to optimize a small and simple train transportation system by minimizing delays. First, we just want to have a 
minimal working prototype that can then be extended to a more complex description (e.g., larger system, more trains, 
higher realism and fidelity, etc.). 

We have timetables and track segments with different capacities (parallel tracks), connecting the different train 
stations. Due to the track selection, this problem is a Mixed-Integer Programs (MIP). We should strongly try to 
formulate linear constraints, as Mixed-Integer Linear Programs (MILP) are much easier to solve. A good (commercial, 
check usage license) solver with a free academic license should be Gurobi. 

## Step 1: Implementing an MILP

To get started with the concept of MILPs, we could first simply have a straight line connecting two train stations, 
where the first half has two tracks and the second one only one. For this, we can probably set (basically) arbitrary 
times for departure and arrival that overlap in the single-track segment and don't need any intermediate train stations 
(stops). We use two trains going in the same direction and set a time horizon that is large enough to allow both trains 
to once make their way to the destination. Also, they should only travel once. 

### Thoughts on the Formulation
- The track system (in our current case just a line with two segments of different capacities (1 and 2)) should have 
- arrival and departure times for each train at the boundary of the segments. 
- For time, probably use integers for now...

## Step 2: Making the Formulation more general

**Just some thoughts to incorporate:**
- Use at least three track segments (of different capacities) to make the implementation easier to formulate for $n$.
- Add a safety distance between trains as this is crucial to depict reality and contributes to the complexity of the 
problem.
- Have at least one train going in the opposite direction (with colliding schedules).


## Step 3: 

**Just some thoughts to incorporate:**
- Maybe add (or think about adding) junctions. 
