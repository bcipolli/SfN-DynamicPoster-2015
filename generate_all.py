"""
master script to generate all data.
"""

# Brains
# import generate_all_brains

# Add more GWAS if possible
# from ping.scripts.gwas import do_gwas
# do_gwas(action='display', measures='MRI_cort_area_ctx_frontalpole_AI',
#         covariates=['Age_At_IMGExam'], data_dir='generated/data',
#         output_dir='generated/data', output_format='json')

# Make scatter and similarity plots
from ping.ping.data import prefixes
for atlas, measures in prefixes.items():
    for measure, prefix in measures.items():

        from ping.scripts.scatter import do_scatter
        do_scatter(prefixes=['MRI_cort_area.ctx.'], x_key='AI:mean',
                   y_key='AI:std', size_key='LH_PLUS_RH:mean',
                   data_dir='generated/data',
                   output_dir='generated/plots', output_format='bokeh-silent')

        from ping.scripts.similarity import do_similarity
        do_similarity(prefixes=['MRI_cort_area.ctx.'],
                      metric='partial-correlation', measures=['Asymmetry Index'],
                      data_dir='generated/data',
                      output_dir='generated/plots', output_format='bokeh-silent')
