#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt


def sequence_length_distribution(sequence, path_to_dir):
    f = 0
    w = 0
    lengths = [len(r) for r in sequence]
    min_len = min(len(r2) for r2 in sequence)
    if min_len == 0:
        f += 1
    distributions = []
    count_distributions = {}
    for i in lengths:
        if i not in distributions:
            distributions.append(i)
            count_distributions[i] = 1
        else:
            count_distributions[i] += 1
    if len(count_distributions) <= 5:
        # it does not seem to work well in such cases
        count_distributions[max(count_distributions) + 1] = 0
        count_distributions[min(count_distributions) - 1] = 0
    else:
        w += 1
    keys = sorted(list(count_distributions.keys()))
    values = [count_distributions[k] for k in keys]
    plt.figure(figsize=(10, 8))
    plt.plot(keys, values)
    plt.xlabel("Sequence length")
    plt.title('Sequence length distribution')
    plt.grid()
    plt.savefig(path_to_dir + r'Sequence_length_distribution.png')
    
    # Alternatively from Stack Overflow
    # from scipy.signal import find_peaks
    # hist, bin_edges = np.histogram(lengths)
    # bin_edges = bin_edges[1:]
    # plt.plot(bin_edges, hist)
    # lengths, _ = find_peaks(hist)
    # plt.plot(bin_edges[lengths], hist[lengths], "x")
