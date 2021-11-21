import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def per_base_n_content(sequence, path_to_dir):
    lenght_max = max(len(x) for x in sequence)
    sequence_added = []
    for i in sequence:
        if len(i) < lenght_max:
            strok = i + "X" * (lenght_max - len(i))
            sequence_added += [strok]
        else:
            sequence_added += [i]
    # Make a list with percent N at each position
    list_of_n = []  # base-content for each position
    lenth_of_string = len(sequence_added[0])
    lenth_of_list = len(sequence_added)
    for j in range(lenth_of_string):
        n = 0
        curent_len = 0
        for i in range(lenth_of_list):
            a = sequence_added[i][j]
            if a != "X":
                curent_len += 1
            if a == "N":
                n += 1
            else:
                continue
        list_of_n += [n * 100 / curent_len]
    # Let's make a dataframe
    np_list_of_n = np.array(list_of_n)
    df_of_n = pd.DataFrame(data=np_list_of_n, index=[i for i in range(1, len(np_list_of_n) + 1)], columns=["% N"])
    # Draw a graph
    fig, ax = plt.subplots(figsize=(10, 8))
    aa = sns.lineplot(data=df_of_n, ax=ax)
    aa.set(xlabel='Position in read', ylabel='Frequency, %')
    aa.set_xlim(0, len(list_of_n))  # make a floating border
    aa.set_ylim(0, 50)  # border 50%
    plt.legend(labels=["N"])
    plt.xticks(np.arange(0, len(list_of_n), len(list_of_n) // 20))
    plt.grid()
    plt.title("N content across all bases")
    if any(df_of_n['% N'] > 20):
        plt.suptitle("Results are not correct! There are positions with N>20%)", color="red")
        result = 'F'
    elif any(df_of_n['% N'] > 5):
        plt.suptitle("Results are not entirely correct. There are positions with N>5%)", color="yellow")
        result = 'W'
    else:
        plt.suptitle("Results are correct", color="green")
        result = 'P'
    plt.savefig(path_to_dir + r'Per_base_N_content.png')
    return result


def per_base_sequence_content(sequence, path_to_dir):
    lenght_max = max(len(x) for x in sequence)
    sequence_added = []
    for i in sequence:
        if len(i) < lenght_max:
            strok = i + "X" * (lenght_max - len(i))
            sequence_added += [strok]
        else:
            sequence_added += [i]
    # Making a list with lists of the number of nucleotides at each position
    lenth_of_string = len(sequence_added[0])
    lenth_of_list = len(sequence_added)
    list_of_base = []  # base-content for each position
    for j in range(lenth_of_string):
        #      A0 T1 G2 C3
        pos = [0, 0, 0, 0]
        curent_len = 0
        for i in range(lenth_of_list):
            a = sequence_added[i][j]
            if a != "X":
                curent_len += 1
            if a == "A":
                pos[0] += 1
            elif a == "T":
                pos[1] += 1
            elif a == "G":
                pos[2] += 1
            elif a == "C":
                pos[3] += 1
            else:
                continue
        for i in range(4):
            pos[i] = (pos[i] * 100) / curent_len
        list_of_base += [pos]
    # Let's make a dataframe
    np_list_of_base_percentage = np.array(list_of_base).reshape(len(list_of_base), 4)
    df_list_of_base_percentage = pd.DataFrame(data=np_list_of_base_percentage,
                                              index=[i for i in range(1, len(np_list_of_base_percentage) + 1)],
                                              columns=["A", "T", "G", "C"])
    # Draw a graph
    fig, ax = plt.subplots(figsize=(10, 8))
    plot = sns.lineplot(data=df_list_of_base_percentage, ax=ax, dashes=False)
    plot.set(xlabel='Position in read', ylabel='Frequency, %')
    plot.set_xlim(0, len(list_of_base))
    plot.set_ylim(0, 100)
    plt.legend(labels=["%A", "%T", "%G", "%C"])
    plt.xticks(np.arange(0, len(list_of_base), len(list_of_base) // 20))
    plt.grid()
    plt.title("Sequence content across all bases")
    if any(((df_list_of_base_percentage['G'] - df_list_of_base_percentage['C']) ** 2) ** 0.5 > 20) or any(
            ((df_list_of_base_percentage['A'] - df_list_of_base_percentage['T']) ** 2) ** 0.5 > 20):
        plt.suptitle("Results are not correct! There are positions with a difference between A and T or G and C> 20%",
                     color="red")
        result = 'F'
    elif any(((df_list_of_base_percentage['G'] - df_list_of_base_percentage['C']) ** 2) ** 0.5 > 10) or any(
            ((df_list_of_base_percentage['A'] - df_list_of_base_percentage['T']) ** 2) ** 0.5 > 10):
        plt.suptitle(
            "Results are not entirely correct. There are positions with a difference between A and T or G and C> 10%",
            color="yellow")
        result = 'W'
    else:
        plt.suptitle("Results are correct", color="green")
        result = 'P'
    plt.savefig(path_to_dir + r'Per_base_sequence_content.png')
    return result


def per_sequence_gc_content(sequence, path_to_dir):
    # Create a list with the percentage of GC for each read and calculate statistics for them
    gc_content = []
    for i in sequence:
        gc_content += [round((i.count("G") + i.count("C")) * 100 / len(i), 1)]
    mean = np.mean(gc_content)
    sd = np.std(gc_content)
    lenght = len(gc_content)
    # Create a dataframe with normal distribution and GC distribution in the sample
    value = np.random.normal(mean, sd, lenght)
    gc_content1 = np.array(gc_content)
    gc_array = np.array([gc_content1, value])
    gc_array = gc_array.transpose()
    gc_df = pd.DataFrame(data=gc_array, index=[i for i in range(1, len(value) + 1)],
                         columns=["GC count per read", "Theoretical distribution"])
    # check for normality
    upper_then_normal_value = sum(gc_df['GC count per read'] > (np.mean(value) + (np.std(value) * 1.96)))
    lower_then_normal_value = sum(gc_df['GC count per read'] < (np.mean(value) - (np.std(value) * 1.96)))
    percentage_of_unnormal_reads = (upper_then_normal_value + lower_then_normal_value) * 100 / np.size(value)

    # Build a graph
    plt.subplots(figsize=(10, 8))
    sns.kdeplot(data=gc_df)
    plt.xlabel('Mean GC content (%)')
    plt.ylabel('Density')
    plt.xticks(np.arange(0, 100, 5))
    plt.grid()
    plt.title("GC distribution overall sequences")
    if percentage_of_unnormal_reads > 10:
        plt.suptitle("Results are not correct! More than 10% of reads deviate from the normal distribution",
                     color="red")
        result = 'F'
    elif percentage_of_unnormal_reads > 5:
        plt.suptitle("Results are not entirely correct. More than 5% of reads deviate from the normal distribution",
                     color="yellow")
        result = 'W'
    else:
        plt.suptitle("Results are correct", color="green")
        result = 'P'
    plt.savefig(path_to_dir + 'Per_sequence_GC_content.png')
    return result
