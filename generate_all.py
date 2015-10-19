"""
master script to generate all data.
"""


def generate_all_brains():
    import os

    from ping.ping.data import prefixes
    from ping.scripts.brain import do_roygbiv

    for measure in ['area', 'thickness']:
        for atlas in ['desikan', 'destrieux']:
            for surface_type in ['pial', 'inflated']:
                for subject in ['fsaverage']:
                    for hemi in ['lh', 'rh']:
                        kwargs = dict(prefix=prefixes[atlas][measure],
                                      surface_type=surface_type, hemi=hemi,
                                      atlas=atlas, subject=subject,
                                      key='AI:mean',
                                      output_format='json',
                                      sample_rate=0.1, force=True,
                                      output_dir=os.path.join(os.getcwd(), 'data'))
                        print("args to call: ", kwargs)
                        do_roygbiv(**kwargs)


def generate_manhattan():
    from ping.scripts.gwas import do_gwas
    do_gwas(action='display', measures='MRI_cort_area_ctx_frontalpole_AI',
            covariates=['Age_At_IMGExam'], data_dir='generated/data',
            output_dir='generated/data', output_format='json')


def generate_bokeh():
    from ping.ping.data import prefixes
    from ping.scripts.scatter import do_scatter
    from ping.scripts.similarity import do_similarity

    for atlas, measures in prefixes.items():
        # Generate area vs. thickness plots
        do_scatter(atlas=atlas, prefixes=[os.path.commonprefix(measures.values())],
                   x_key='%s:AI:mean' % measures['area'],
                   y_key='%s:AI:mean' % measures['thickness'],
                   data_dir='generated/data',
                   output_dir='generated/plots',
                   output_format='bokeh')

        for measure, prefix in measures.items():
            # Generate scatter plot for given dataset / data point
            do_scatter(atlas=atlas, prefixes=[prefix], x_key='AI:mean',
                       y_key='AI:std', size_key='LH_PLUS_RH:mean',
                       data_dir='generated/data',
                       output_dir='generated/plots', output_format='bokeh')

            # Generate similarity matrix for given dataset / data point
            do_similarity(atlas=atlas, prefixes=[prefix],
                          metric='partial-correlation', measures=['Asymmetry Index'],
                          data_dir='generated/data',
                          output_dir='generated/plots', output_format='bokeh')


if __name__ == '__main__':
    generate_all_brains()
    generate_manhattan()
    generate_bokeh()
