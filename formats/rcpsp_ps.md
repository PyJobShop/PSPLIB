Note: taken from https://data.4tu.nl/articles/dataset/Instances_and_file_format_for_the_Resource_Constrained_Project_Scheduling_Problem_with_a_flexible_Project_Structure/21106768 

----

The input file format is as following (# of means number of)
Counting starts at 0

	[# of activities] [# of renewable resources] [#number of nonrewable resources]
	[resource availabilities]

	[duration] [resource requirements per resource type]
	[# of selection-groups] [[# of or selection successors] [selection group successor1] [selection group successor2]...] (repeat)
	[# of time precedence successors] [successor1] [successor2] ...




To give a small example:

	5 1 0
	10
	
	0 0
	2 2 1 2 1 3
	3 1 2 3
	
	2 5
	1 1 4
	1 4
	
	2 6
	1 1 4
	1 4
	
	3 10
	1 1 4
	1 4
	
	4 0
	0
	0
	
This means:

	5 1 0
	10 6 8 2
	1.05 1.06
	
In total 5 activities, with 1 renewable resource (with availability 10), and 0 nonrenewable resources

	0 0
	2 2 1 2 1 4
	3 1 2 3
	
First line: Activity 0 with a duration of 0 and no resource requirements
Second line: Two selection-groups. The first one has two successor nodes 
Third line: Three time successors: Activities 1 2 and 3
