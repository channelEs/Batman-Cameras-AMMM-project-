/*****************************************************************************
 * Modello ILP per il progetto "Batman - Monitoring the Streets"
 * Versione per Copia-Incolla Manuale
 *****************************************************************************/

// --- PARAMETRI ---
int N = ...; 
int K = ...; 

range Crossings = 1..N;
range Models = 1..K;
range Days = 1..7; 

int P[Models] = ...; 
int R[Models] = ...; 
int A[Models] = ...; 
float C[Models] = ...; 

int M[Crossings][Crossings] = ...;

int Cover[i in Crossings][j in Crossings][k in Models] = (R[k] >= M[i][j]) ? 1 : 0;

// --- VARIABILI DECISIONALI ---
dvar boolean y[Crossings][Models];
dvar boolean x[Crossings][Models][Days];

// --- FUNZIONE OBIETTIVO ---
minimize 
  sum(i in Crossings, k in Models) P[k] * y[i][k] 
  + 
  sum(i in Crossings, k in Models, d in Days) C[k] * x[i][k][d];

// --- VINCOLI ---
subject to {
  forall(i in Crossings)
    sum(k in Models) y[i][k] <= 1;

  forall(i in Crossings, k in Models, d in Days)
    x[i][k][d] <= y[i][k];

  forall(j in Crossings, d in Days)
    sum(i in Crossings, k in Models) Cover[i][j][k] * x[i][k][d] >= 1;

  forall(i in Crossings, k in Models, d in Days) {
    x[i][k][d] - x[i][k][(d == 1 ? 7 : d-1)] <= x[i][k][(d == 7 ? 1 : d+1)];
  }

  forall(i in Crossings, k in Models, d in Days) {
    sum(offset in 0..A[k]) x[i][k][(d + offset - 1) % 7 + 1] <= A[k];
  }
}

// --- OUTPUT DATI PER PYTHON ---
execute {
  // Recuperiamo i valori
  var costo = cplex.getObjValue();
  var tempo = cplex.getCplexTime();
  
  writeln("");
  writeln("***************************************************");
  writeln("* COPIA LA RIGA QUI SOTTO NEL PROGRAMMA PYTHON   *");
  writeln("***************************************************");
  // Formato: N;K;Costo;Tempo
  writeln("DATA:" + N + ";" + K + ";" + costo + ";" + tempo);
  writeln("***************************************************");
  writeln("");
}