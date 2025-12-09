import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

def global_heuristics_results():
    # 1. Load Data
    df_greedy = pd.read_csv('All_Executions_GREEDY.csv', delimiter=';')
    df_ls = pd.read_csv('All_Executions_LocalSearch.csv', delimiter=';')
    df_grasp = pd.read_csv('All_Executions_GRASP.csv', delimiter=';')

    # 2. Label Algorithms Explicitly
    df_greedy['Algorithm'] = 'Greedy'
    df_ls['Algorithm'] = 'Local Search'
    df_grasp['Algorithm'] = 'GRASP'

    # 3. Combine
    df_all = pd.concat([df_greedy, df_ls, df_grasp], ignore_index=True)

    # 4. Clean Instance Names for X-Axis (Remove 'batman_' and '.dat')
    df_all['Instance'] = df_all['in_filename'].str.replace('batman_', '').str.replace('.dat', '')

    # 5. Plot
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")

    # Create Bar Chart
    ax = sns.barplot(
        data=df_all, 
        x='Instance', 
        y='total_cost', 
        hue='Algorithm',
        palette='viridis',
        edgecolor='black' # Adds a border to bars for clarity
    )

    # Add Values on Top of Bars
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(f'{int(p.get_height())}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 8), 
                    textcoords = 'offset points',
                    fontsize=9, fontweight='bold')

    plt.title('Comparison of Solution Costs by Solver', fontsize=15)
    plt.ylabel('Total Cost (€)', fontsize=12)
    plt.xlabel('Instance', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Solver', bbox_to_anchor=(1.02, 1), loc='upper left')

    plt.tight_layout()
    plt.savefig('solvers_comparison_plot.png', dpi=300)
    plt.show()

global_heuristics_results()