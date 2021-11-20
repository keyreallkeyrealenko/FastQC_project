import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def per_base_n_content(sequence_added, path_to_dir):
    # Сделаем список с процентами N на каждой позиции
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
    # Сделаем датафрейм
    np_list_of_n = np.array(list_of_n)
    df_of_n = pd.DataFrame(data=np_list_of_n, index=[i for i in range(1, len(np_list_of_n) + 1)], columns=["% N"])
    # Нарисуем график
    fig_dims = (10, 8)
    fig, ax = plt.subplots(figsize=fig_dims)
    aa = sns.lineplot(data=df_of_n, ax=ax)
    aa.set(xlabel='Position in read', ylabel='Frequency, %')
    aa.set_xlim(0, len(list_of_n))  # делаем плавающую границу
    aa.set_ylim(0, 20)  # граница 20%, т.к. более 20 уже некорректный образец
    plt.legend(labels=["N"])
    plt.xticks(np.arange(0, len(list_of_n), len(list_of_n) // 20))
    plt.grid()
    plt.title("N content across all bases")
    plt.savefig(path_to_dir + r'Per_base_N_content.png')


def per_base_sequence_content(sequence_added, path_to_dir):
    # Делаем список со списками количества нуклеотидов на каждой позиции
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
            pos[i] = (pos[i]*100)/curent_len
        list_of_base += [pos]
    # Сделаем датафрейм
    np_list_of_base_percentage = np.array(list_of_base).reshape(len(list_of_base), 4)
    df_list_of_base_percentage = pd.DataFrame(data=np_list_of_base_percentage,
                                              index=[i for i in range(1, len(np_list_of_base_percentage) + 1)],
                                              columns=["A", "T", "G", "C"])
    # Нарисуем график
    fig_dims = (10, 8)
    fig, ax = plt.subplots(figsize=fig_dims)
    plot = sns.lineplot(data=df_list_of_base_percentage, ax=ax)
    plot.set(xlabel='Position in read', ylabel='Frequency, %')
    plot.set_xlim(0, len(list_of_base))
    plot.set_ylim(0, 100)
    plt.legend(labels=["A", "T", "G", "C"])
    plt.xticks(np.arange(0, len(list_of_base), len(list_of_base) // 20))
    plt.grid()
    plt.title("Sequence content across all bases")
    plt.savefig(path_to_dir + r'Per_base_sequence_content.png')


def per_sequence_gc_content(sequence, path_to_dir):
    # Создадим список с процентом GC по каждому риду и посчитаем статистики по ним
    gc_content = []
    for i in sequence:
        gc_content += [round((i.count("G") + i.count("C")) * 100 / len(i), 1)]
    mean = np.mean(gc_content)
    sd = np.std(gc_content)
    lenght = len(gc_content)
    # Создадим датафрейм с нормальным распределением и распределением GC в образце
    value = np.random.normal(mean, sd, lenght)
    gc_content1 = np.array(gc_content)
    gc_array = np.array([gc_content1, value])
    gc_array = gc_array.transpose()
    gc_df = pd.DataFrame(data=gc_array, index=[i for i in range(1, len(value) + 1)],
                         columns=["GC count per read", "Theoretical distribution"])
    # Построим график
    ax1 = sns.displot(gc_df, kind="kde")
    ax1.set(xlabel='Mean GC content (%)', ylabel='Density')
    plt.xticks(np.arange(0, 100, 5))
    plt.grid()
    plt.title("GC distribution overall sequences")
    plt.savefig(path_to_dir + r'Per_sequence_GC_content.png')


def create_gc_base_n_graphs(sequence, path_to_dir):
    def get_new_string(seq):
        lenght_max = max(len(x) for x in seq)
        new_string = []
        for i in sequence:
            if len(i) < lenght_max:
                strok = i + "X" * (lenght_max - len(i))
                new_string += [strok]
            else:
                new_string += [i]
        return new_string

    sequence_added = get_new_string(sequence)
    per_base_n_content(sequence_added, path_to_dir)
    per_base_sequence_content(sequence_added, path_to_dir)
    per_sequence_gc_content(sequence, path_to_dir)
