import pandas as pd
import matplotlib.pyplot as plt

def GRASP_alpha_plot():
    # 1. Load Data
    file_path = 'batman_N30_K10_GRASP_alpha.csv'
    df = pd.read_csv(file_path, delimiter=';')

    # 2. Setup the Plot (Dual Axis)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Cost (Red Line, Left Axis)
    color_cost = 'tab:red'
    ax1.set_xlabel(r'GRASP Parameter $\alpha$')
    ax1.set_ylabel('Total Cost (€)', color=color_cost, fontsize=12)
    ax1.plot(df['alpha'], df['total_cost'], color=color_cost, marker='o', linewidth=2, label='Best Cost Found')
    ax1.tick_params(axis='y', labelcolor=color_cost)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Plot Time (Blue Dashed Line, Right Axis)
    ax2 = ax1.twinx()
    color_time = 'tab:blue'
    ax2.set_ylabel('Execution Time (s)', color=color_time, fontsize=12)
    ax2.plot(df['alpha'], df['time'], color=color_time, marker='x', linestyle='--', linewidth=2, label='Execution Time')
    ax2.tick_params(axis='y', labelcolor=color_time)

    # 3. Titles and Legends
    plt.title(r'Sensitivity Analysis of GRASP Parameter $\alpha$', fontsize=14)
    fig.legend(loc="upper center", bbox_to_anchor=(0.5, 0.9), ncol=2, frameon=True)

    # 4. Save and Show
    plt.tight_layout()
    plt.savefig('grasp_analysis.png', dpi=300)
    plt.show()

def general_result():
    # Load data
    df = pd.read_csv("batman_results.csv")

    # Create a boxplot to compare algorithms
    plt.figure(figsize=(8, 6))
    df.boxplot(column='Total_Cost', by='Algorithm', grid=False)

    plt.title('Comparison of Optimization Algorithms')
    plt.suptitle('') # Removes the default 'Boxplot grouped by...' title
    plt.ylabel('Total Cost')
    plt.xlabel('Algorithm')
    plt.show()

