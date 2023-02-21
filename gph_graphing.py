"""gph_graphing.py
File containing pyplot code that's used in several places.
"""

from matplotlib import pyplot as plt


def make_graph(graph_data, update_list, units, plotname, plotfile_name):
    # Set up Pyplot to customize the appearance of the graph
    text_color = '#99AAB5'
    bg_color = '#333333'
    plot_markers = ['o', '^', 's', 'X', 'D', 'v', '*', 'p']

    with plt.rc_context({'axes.spines.right': False, 'axes.spines.top': False, 'axes.facecolor': bg_color,
                         'axes.edgecolor': text_color, 'axes.labelcolor': text_color, 'axes.titlecolor': text_color,
                         'xtick.color': text_color, 'ytick.color': text_color, 'legend.edgecolor': text_color,
                         'legend.fancybox': True, 'figure.facecolor': bg_color, 'figure.edgecolor': text_color,
                         'figure.titlesize': 'large'}):
        # Add lines for each of the top_n to the graph
        for i in range(len(graph_data[0])):
            plt.plot(update_list, graph_data[i + 1], label=graph_data[0][i], marker=plot_markers[i])

        # More plot setup
        plt.xticks(update_list)
        plt.xlabel('Update number')
        plt.ylabel(f'{units} gained')
        plt.title(plotname)
        plt.legend(facecolor='#36393F', labelcolor='#99AAB5')

        # Save plot to a file so it can be sent to Discord
        plt.tight_layout()
        plt.savefig(plotfile_name)
