from TICC_solver import TICC
import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import Patch
import ipdb

def plot_results(input_file, output_file):
    # plot
    fig, ax = plt.subplots(figsize=(24, 6))
    Data = np.loadtxt(input_file, delimiter=",")
    results = np.loadtxt(output_file, delimiter=",")
    ax.plot(Data)
    
    df = pd.DataFrame(results.astype(int), columns=['color'])
    df['index'] = range(results.shape[0])
    cmap = matplotlib.cm.get_cmap('Set3')
    for c in df['color'].unique():
        bounds = df[['index', 'color']].groupby('color').agg(['min', 'max']).loc[c]
        ax.axvspan(bounds.min(), bounds.max()+1, alpha=0.5, color=cmap.colors[c])
    legend = [Patch(facecolor=cmap.colors[c], label=c) for c in df['color'].unique()]
    ax.legend(handles=legend)
    
    fig.savefig('example_data.png')
    plt.close(fig)
    print("raw_signals plotted and saved, check!")
    sys.exit()

    
fname = "example_data.txt"
ticc = TICC(window_size=1, number_of_clusters=8, lambda_parameter=11e-2, beta=600, maxIters=100, threshold=2e-5,
            write_out_file=False, prefix_string="output_folder/", num_proc=1)
(cluster_assignment, cluster_MRFs) = ticc.fit(input_file=fname)
print(cluster_assignment)
np.savetxt('Results.txt', cluster_assignment, fmt='%d', delimiter=',')

plot_results(input_file = 'example_data.txt', output_file = 'Results.txt')
