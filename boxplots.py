import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
from basic_statistics import type_check


def create_boxplot(dataframe, output, encoding):
    max_val = max(dataframe.max())
    if dataframe.shape[1] > 50:
        dataframe = dataframe.iloc[:, np.r_[:10, np.arange(11, dataframe.shape[1],
                                                           step=(dataframe.shape[1] - 10) / 40)]]
    quartile_25 = dataframe.quantile([0.25]).iloc[0]
    median_val = dataframe.median()
    plt.figure(figsize=(16, 10), dpi=150)
    sns.boxplot(data=dataframe, showfliers=False, color="#FFFB02", medianprops=dict(color="red"), zorder=10)
    ax = sns.pointplot(data=dataframe, errwidth=0.01, scale=0.4, zorder=3)
    sns.set_theme(style="white")
    plt.axhspan(0, 20.1, facecolor='#F77A61', alpha=0.5, zorder=-1)
    plt.axhspan(20, 28.1, facecolor='#DEDD7C', alpha=0.5, zorder=-2)
    plt.axhspan(28, max_val + 0.2, facecolor='#84D56C', alpha=0.5, zorder=-3)
    ax.set(ylim=(0, max_val + 0.2))
    plt.yticks(np.arange(0, max_val, step=2), fontsize=12)
    if (quartile_25 < 5).any() or (median_val < 20).any():
        ax.axes.set_title(f'Quality score across all bases ({encoding})\n(FAILURE!)', fontsize=20, pad=4)
    elif (quartile_25 < 10).any() or (median_val < 25).any():
        ax.axes.set_title(f'Quality score across all bases ({encoding})\n(WARNING!)', fontsize=20, pad=4)
    else:
        ax.axes.set_title(f'Quality score across all bases ({encoding})\n(Everything is OK!)', fontsize=20, pad=4)
    for i in range(0, len(dataframe.columns), 2):
        plt.axvspan(i, i + 1, color='#E1E1DB', alpha=0.4, zorder=0)
    plt.xlabel('Position in read (bp)', fontsize=16, labelpad=12)
    if dataframe.shape[1] < 50:
        plt.xticks(np.arange(0, dataframe.shape[1], step=2), fontsize=12)
    else:
        n = len(dataframe.columns)
        idx = np.zeros(n // 2, dtype=bool)
        idx[:5] = True
        idx[4:None:3] = True
        indexes = np.arange(n).reshape(-1, 2)[idx].ravel()
        plt.xticks(indexes, fontsize=12)
    return plt.savefig(f'{output}/boxplot.png')


def create_quality_plot(dataframe, output):
    dict_df = pd.DataFrame.from_dict(dataframe, orient='index')
    dict_df = dict_df.sort_index()
    dict_df.reset_index(level=0, inplace=True)
    dict_df.columns = [''] * len(dict_df.columns)
    max_yvalue = max(dict_df.iloc[:, 1])
    max_xvalue = dict_df.iloc[dict_df.index[dict_df.iloc[:, 1] == max_yvalue].tolist()[0], 0]
    plt.figure(figsize=(16, 10), dpi=150)
    sns.lineplot(data=dict_df, x=dict_df.iloc[:, 0], y=dict_df.iloc[:, 1], color='red', linewidth=4)
    sns.set(rc={'figure.figsize': (15, 10)})
    sns.set_style("white")
    sns.despine()
    plt.xticks(np.arange(min(dict_df.iloc[:, 0]), max(dict_df.iloc[:, 0])), size=14)
    plt.xlabel('Mean Sequence Quality (Phred Score)', size=14)
    plt.yticks(size=20)
    plt.grid(axis='y')
    plt.ylim(ymin=0)
    if max_xvalue < 20:
        plt.title('Quality score distribution over all sequences\n(FAILURE!)', size=18)
    elif max_xvalue < 27:
        plt.title('Quality score distribution over all sequences\n(WARNING!)', size=18)
    else:
        plt.title('Quality score distribution over all sequences\n(Everything is OK!)', size=18)
    for i in range(min(dict_df.iloc[:, 0]), max(dict_df.iloc[:, 0]) + 1, 2):
        plt.axvspan(i, i + 1, color='#E1E1DB', alpha=0.4, zorder=0)
    plt.text(max_xvalue - 2, max_yvalue, 'Average Quality per read', color='red', size=14,
             bbox=dict(facecolor='white', edgecolor='grey'))

    return plt.savefig(f'{output}/quality_scores.png')


def compile_quality(file, output):
    d_boxplot = {}
    dict_df = {}
    for record in range(len(file)):
        if record % 4 == 3:
            quality = file[record].strip()
            quality_value = 0
            for symbol in range(len(quality)):
                if symbol + 1 not in d_boxplot:
                    d_boxplot[symbol + 1] = [ord(quality[symbol]) - 33]
                else:
                    d_boxplot[symbol + 1].append(ord(quality[symbol]) - 33)
                quality_value += ord(quality[symbol]) - 33
            if round(quality_value / len(quality)) not in dict_df:
                dict_df[round(quality_value / len(quality))] = 1
            else:
                dict_df[round(quality_value / len(quality))] += 1

    create_quality_plot(dict_df, output)
    dataframe = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in d_boxplot.items()]))
    encoding = type_check(file)
    create_boxplot(dataframe, output, encoding)
