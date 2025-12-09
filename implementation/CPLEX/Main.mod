/*********************************************
 * OPL 22.1.1.0 Model
 * Author: roger
 * Creation Date: Dec 9, 2025 at 2:30:36 PM
 *********************************************/

main {
	// Store initial time
  var start = new Date();
  var startTime = start.getTime();
	
	    
	var src = new IloOplModelSource("progetto amm.mod"); // load model
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	var model = new IloOplModel(def, cplex);
	
	var data = new IloOplDataSource("batman_N40_K20.dat"); // load instance
	model.addDataSource(data);
	model.generate();
	
	cplex.tilim=600; // 30 mins
	cplex.epgap = 0.01; // GAP 1%
	
	if (cplex.solve()) {
		writeln ( "Max load " + cplex.getObjValue() + "%" );
		writeln("DATA:" + model.N + ";" + model.K + ";" + cplex.getObjValue() + ";" + cplex.getCplexTime());
	}
	else {
		writeln("No solution found");
	}
	
	model.end();
	data.end();
	def.end();
	cplex.end();
	src.end();
	
	// Write execution time
  var end = new Date();
  var endTime = end.getTime();
  writeln("Execution time: " + (endTime - startTime) + "ms");
};