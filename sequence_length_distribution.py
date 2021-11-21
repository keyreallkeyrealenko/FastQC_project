#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt


def sequence_length_distribution(sequence, path_to_dir):
    lengths = [len(r) for r in sequence]
    min_len = min(len(r2) for r2 in sequence)
    if min_len == 0:
        return "F"
    distributions = []
    count_distributions = {}
    for i in lengths:
        if i not in distributions:
            distributions.append(i)
            count_distributions[i] = 1
        else:
            count_distributions[i] += 1
    if len(count_distributions) == 1:
        count_distributions[max(count_distributions) + 1] = 0
        count_distributions[min(count_distributions) - 1] = 0
    else:
        return "W"
    keys = sorted(list(count_distributions.keys()))
    values = [count_distributions[k] for k in keys]
    plt.figure(figsize=(10, 8))
    plt.plot(keys, values)
    plt.xlabel("Sequence length")
    plt.title('Sequence length distribution')
    plt.grid()
    plt.savefig(path_to_dir + r'Sequence_length_distribution.png')
