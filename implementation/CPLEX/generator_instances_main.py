import random
import sys
import os

def generate_instance(N, K, filename=None):
    """
    Genera un'istanza del problema Batman in formato OPL .dat
    e la salva direttamente su un file.
    """
    
    # Se non specificato, crea un nome file automatico es: batman_N10_K3.dat
    if filename is None:
        filename = f"batman_N{N}_K{K}.dat"
    
    print(f"\nGenerazione istanza con N={N}, K={K}...")
    
    # --- 1. Generazione Dati ---
    P = [random.randint(10, 100) for _ in range(K)]
    R = [random.randint(1, 49) for _ in range(K)]
    A = [random.randint(2, 6) for _ in range(K)]
    C = [round(random.uniform(1.0, 10.0), 2) for _ in range(K)]

    M = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            is_reachable = random.random() > 0.3
            if is_reachable:
                dist = random.randint(1, 49)
            else:
                dist = random.randint(50, 100)
            M[i][j] = dist
            M[j][i] = dist

    # --- 2. Scrittura su File ---
    try:
        with open(filename, 'w') as f:
            f.write("/*************************************************\n")
            f.write(f" * Istanza Generata Random\n")
            f.write(f" * N (Incroci) = {N}\n")
            f.write(f" * K (Modelli) = {K}\n")
            f.write(" *************************************************/\n\n")
            
            f.write(f"N = {N};\n")
            f.write(f"K = {K};\n\n")
            
            f.write(f"P = {P};\n")
            f.write(f"R = {R};\n")
            f.write(f"A = {A};\n")
            f.write(f"C = {C};\n\n")
            
            f.write("M = [\n")
            for row in M:
                f.write(f"  {row},\n")
            f.write("];\n")
            
        print(f"[SUCCESSO] File creato correttamente: {filename}")
        print(f"Trovi il file nella stessa cartella di questo script.")
        
    except Exception as e:
        print(f"\n[ERRORE] Impossibile scrivere il file: {e}")

if __name__ == "__main__":
    # Se lanciato senza argomenti (es. da IDE o doppio click), chiede input all'utente
    if len(sys.argv) != 3:
        print("--- Generatore Istanze Batman (OPL .dat) ---")
        try:
            val_n = input("Inserisci il numero di Incroci (N): ")
            val_k = input("Inserisci il numero di Modelli (K): ")
            
            n_input = int(val_n)
            k_input = int(val_k)
            
            generate_instance(n_input, k_input)
        except ValueError:
            print("Errore: Devi inserire numeri interi validi.")
        
        # Pausa finale per non far chiudere la finestra subito su Windows
        input("\nPremi INVIO per chiudere...")
        
    else:
        # Modalità terminale (se volessi ancora usarla): python generator.py 10 3
        try:
            n_input = int(sys.argv[1])
            k_input = int(sys.argv[2])
            generate_instance(n_input, k_input)
        except ValueError:
            print("// Errore: N e K devono essere numeri interi.")