import plotly.graph_objects as go


def type_check(file):
    """Function guesses the encoding type"""
    length = 0
    pulled_ascii = []
    for qs_number in range(3, len(file), 4):
        length += len(file[qs_number])
        for ascii_symbol in file[qs_number].strip():
            pulled_ascii.append(int(ord(ascii_symbol)))
        if qs_number >= 4000:
            break

    if min(pulled_ascii) >= 33 and 105 in pulled_ascii:
        return 'Illumina-1.3'
    elif min(pulled_ascii) >= 66 and max(pulled_ascii) > 100:
        return 'Illumina-1.5'
    elif min(pulled_ascii) >= 50 and max(pulled_ascii) > 100:
        return 'Solexa/Illumina 1.0'

    return 'Sanger/Illumina 1.9'


def handler(file):
    """This functions performs basic statistics operations for a "basic statistics" table """
    GC = 0
    length = []
    poor_quality = 0
    for i in range(len(file)):
        if i % 4 == 1:
            sequence = file[i].strip()
            GC += sequence.count('G') + sequence.count('C')
            length.append(len(sequence))
        if i % 4 == 3:
            quality = file[i].strip()
            quality_length = len(quality)
            bad_quality = 0
            for symbol in quality:
                if ord(symbol) - 33 < 10:
                    bad_quality += 1
            if bad_quality/quality_length > 0.9:
                poor_quality += 1
    total_seq = len(length)
    GC = round(GC * 100 / sum(length))
    length_range = set(length)
    return GC, length_range, total_seq, poor_quality


def basic_statistics(file, filename, output):
    if '\\' in filename:
        filename = filename.split('\\')[-1]
    elif '/' in filename:
        filename = filename.split('/')[-1]
    Filename = filename
    File_type = 'Conventional base calls'
    Encoding = type_check(file)
    Total_Sequences = handler(file)[2]
    poor_quality = handler(file)[3]
    GC_percent = handler(file)[0]
    Sequence_length = handler(file)[1]
    if len(Sequence_length) > 1:
        Sequence_length = f'{min(Sequence_length)} - {max(Sequence_length)}'
    else:
        Sequence_length = max(Sequence_length)
    layout = go.Layout(
        autosize=False,
        width=700,
        height=400
    )
    fig = go.Figure(data=[go.Table(header=dict(values=['Measure', 'Value'], fill_color='darkblue',
                                               font=dict(color='white', size=18)),
                                   cells=dict(values=[['Filename', 'File type', 'Encoding', 'Total Sequences',
                                                       'Sequences flagged as poor quality', 'Sequence length',
                                                       '%GC'], [Filename, File_type, Encoding, Total_Sequences,
                                                                poor_quality,
                                                                Sequence_length,
                                                                GC_percent]], font=dict(color='black', size=12),
                                              align='left', fill_color='lightgrey'))],layout=layout)

    return fig.write_image(f'{output}/basic_statistics.pdf')
