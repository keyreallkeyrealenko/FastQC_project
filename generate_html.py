def generate_html(outdir, boxplot_test, per_quality_ps_test, dupl_test, overrepresented_test):
    html_output = f'''<!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8"/>
    <title>FASTQC report</title>
    </head>
    <body>
    <h2><img src={'./icons/' + boxplot_test + '.png'}>Per base sequence quality</h2>
    <img src={outdir + '/boxplot.png'}>
    <h2><img src={'./icons/' + per_quality_ps_test + '.png'}>Per sequence quality scores</h2>
    <img src={outdir + '/quality_scores.png'}>
    <h2>Per base sequence content</h2>
    <img src={outdir + '/Per_base_sequence_content.png'}>
    <h2>Per sequence GC content</h2>
    <img src={outdir + '/Per_sequence_GC_content.png'}>
    <h2>Per base N content</h2>
    <img src={outdir + '/Per_base_N_content.png'}>
    <h2><img src={'./icons/' + dupl_test + '.png'}>Sequence Duplication Levels</h2>
    <img src={outdir + '/duplications.png'}>
    <h2><img src={'./icons/' + overrepresented_test + '.png'}>Overrepresented sequences</h2>
    </body>
    </html>'''
    with open('fastqc_report.html', 'w') as out:
        out.write(html_output)
