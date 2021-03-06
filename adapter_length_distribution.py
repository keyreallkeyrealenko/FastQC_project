#!/usr/bin/env python
# coding: utf-8

# In[1]:

# In[2]:


import matplotlib.pyplot as plt


def adapter_content(sequence, path_to_dir):
    # Illumina Universal Adapter—AGATCGGAAGAG
    # Illumina Small RNA 3' Adapter—TGGAATTCTCGG
    # Illumina Small RNA 5' Adapter—GATCGTCGGACT
    # Nextera Transposase Sequence—CTGTCTCTTATA
    universal = "AGATCGGAAGAG"
    small_3 = "TGGAATTCTCGG"
    small_5 = "GATCGTCGGACT"
    transposase = "CTGTCTCTTATA"
    plt.figure(figsize=(10, 8))
    adapters = [universal, small_3, small_5, transposase]
    max_len = max(len(r1) for r1 in sequence)
    for a in adapters:
        count_adapters = {}
        for i in range(max_len):
            count_adapters[int(i)] = 0
        for s in sequence:
            if a in s:
                for j in range(s.seq.index(a), max_len):
                    count_adapters[j] += 1
        keys = list(count_adapters.keys())
        values = [count_adapters[k]/len(sequence)*100 for k in keys]
        for x in values:
            if x >= 5:
                return "W"
            elif x >= 5:
                return "F"
        plt.plot(keys, values)
        count_adapters = [{i: 0} for i in range(max_len)]
    plt.legend(labels=["Illumina Universal Adapter", "Illumina Small RNA 3' Adapter",
                       "Illumina Small RNA 5' Adapter", "Nextera Transposase Sequence"])
    plt.xlabel("Position in read")
    plt.title('Adapter content')
    plt.ylim(0, 100)
    plt.grid()
    plt.savefig(path_to_dir + r'Adapter_content.png')


# In[7]:


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
# In[ ]:
