# Instructions of each part
## INSTANCE GENERATION
Inside the DATA/ directory there is the script to generate random instances of the problem. It is a [Jupyter Notebook](https://jupyter.org/) divided in two part, the first cell is to generate the instances, the second is to save the results of the CPLEX log into a CSV file.

The first part asks for two inputs, first the N value, then the M value. Once both values are inserted correctly, it will generate a file as **batman_NXX_KYY.dat**. This is a random instance of the problem.

The second part asks for the result line from the log console of CPLEX, the one that starts with 'DATA;..;...;...'. This part insterts a new row of values into the results CSV file.

## CPLEX EXECUTION
To execute the CPLEX modules, there is a Main.mod prepared to read input instances and generate a CSV file with the results.

It can read more than one .dat file as entrance and it will execute them sequentialy. The time limit it is also setted for each execution of the problem.

In the Main.mod script, just add a new element in the **datFiles** var, such as:
````shell 
var datFiles = new Array();
datFiles[0] = "file_to_instance_01.dat"
datFiles[1] = "file_to_instance_02.dat"
datFiles[2] = "file_to_instance_03.dat"
...
````
This will execute sequentally the instances 01, 02, 03,... And save the results in the outfile variable named "results.csv". This CSV file can also be modified just by changes the parameter in the IloOplOutputFile("csv_file_result_can_be_modified.csv");

## HEURISTICS
To solve instances using heuristics, first open a terminal inside the Heuristics/ directory.

Once in the heuristics root directory, just execute the commad:
```shell
python3 Main.py
```
And it will solve the instance with the configuration setted in the config/ subdirectory. In the config file is where the input is setted. Modify the file with the following parameters:
- inputFileName [the filename of the instance to be solved]
- solutionFile [output filename]
- solver [solver used]
- local_search [True -> used, False -> not used]
- maxExecTime [maximum execution time in minutes]

