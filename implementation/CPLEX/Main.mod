/*********************************************
 * OPL 22.1.1.0 Model
 * Author: roger
 * Creation Date: Dec 9, 2025 at 2:30:36 PM
 *********************************************/

main {
  // 1. Define your model source and definition ONCE (more efficient)
  var src = new IloOplModelSource("progetto_ammm.mod");
  var def = new IloOplModelDefinition(src);

  var datFiles = new Array();
  /*
  datFiles[0] = "batman_N10_K2.dat";
  datFiles[1] = "batman_N10_K3.dat";
  datFiles[2] = "batman_N10_K6.dat";
  datFiles[3] = "batman_N15_K10.dat";
  datFiles[4] = "batman_N20_K3.dat";
  datFiles[5] = "batman_N30_K5.dat";
  datFiles[6] = "batman_N30_K10.dat";
  datFiles[7] = "batman_N40_K20.dat";
  datFiles[8] = "batman_N40_K25.dat";
  datFiles[0] = "batman_N45_K20.dat";
  datFiles[1] = "batman_N50_K30.dat";
  */
  datFiles[0] = "batman_N60_K30.dat";
  datFiles[1] = "batman_N60_K40.dat";
  datFiles[2] = "batman_N70_K50.dat";
  datFiles[3] = "batman_N90_K50.dat";
  datFiles[4] = "batman_N130_K5.dat";
  datFiles[5] = "batman_N260_K5.dat";
  datFiles[6] = "batman_N300_K5.dat";

  // Add more lines here as needed: datFiles[2] = "..."
  // --- CHANGED SECTION END ---

	var outfile = new IloOplOutputFile("results_ALL_INSTANCES.csv");
	outfile.writeln("Type;Filename;N;K;Objective;Time(s)");
  var globalStart = new Date();

  // Iterate using the array length
  for (var i = 0; i < datFiles.length; i++) {
    var fileName = datFiles[i];
    writeln("--------------------------------------------------");
    writeln("Solving instance: " + fileName);

    var instanceStart = new Date();
 	var cplex = new IloCplex();
	var model = new IloOplModel(def, cplex);
    var data = new IloOplDataSource(fileName);
    model.addDataSource(data);
    
    model.generate();
	cplex.tilim = 1800; // Note: 600s is 10 mins. Use 1800 for 30 mins.
    cplex.epgap = 0.01; 

    // Solve
    if (cplex.solve()) {
      var outputString = "DATA;" + fileName + ";" + model.N + ";" + model.K + ";" + cplex.getObjValue() + ";" + cplex.getCplexTime();
      writeln("Max load " + cplex.getObjValue() + "%");
      writeln(outputString);
      outfile.writeln(outputString);
    } else {
      writeln("No solution found for " + fileName);
    }

    // 4. IMPORTANT: Clean up memory for this iteration
    model.end();
    data.end();
    cplex.end();
    
    // Calculate time for this instance
    var instanceEnd = new Date();
    writeln("Instance Time: " + (instanceEnd.getTime() - instanceStart.getTime()) + "ms");
  }

  // Clean up global objects
  def.end();
  src.end();

  var globalEnd = new Date();
  writeln("--------------------------------------------------");
  writeln("Total Execution time: " + (globalEnd.getTime() - globalStart.getTime()) + "ms");
}