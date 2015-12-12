"""
master script to generate all data.
"""


def generate_all_brains():
    import os

    from ping.ping.data import prefixes
    from ping.scripts.brain import do_roygbiv

    for measure in ['area', 'thickness']:
        for atlas in ['desikan']:  # skip destrieux
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


def generate_scatter_bokeh():
    import os

    from ping.ping.data import prefixes
    from ping.scripts.scatter import do_scatter
    from ping.scripts.similarity import do_similarity

    for atlas, measures in prefixes.items():
        # Generate area vs. thickness plots
        if atlas.lower() == 'destrieux':
            continue
        do_scatter(atlas=atlas, prefixes=[os.path.commonprefix(measures.values())],
                   x_key='%s:_AI:mean' % measures['area'],
                   y_key='%s:_AI:mean' % measures['thickness'],
                   data_dir='generated/data',
                   output_dir='generated/plots',
                   output_format='bokeh')

        for measure, prefix in measures.items():
            # Generate scatter plot for given dataset / data point
            do_scatter(atlas=atlas, prefixes=[prefix], x_key='_AI:mean',
                       y_key='_AI:std', size_key='_LH_PLUS_RH:mean',
                       data_dir='generated/data',
                       output_dir='generated/plots', output_format='bokeh')


def generate_similarity_bokeh():
    import os

    from ping.ping.data import prefixes
    from ping.scripts.scatter import do_scatter
    from ping.scripts.similarity import do_similarity

    for atlas, measures in prefixes.items():
        if atlas == 'destrieux':  # skip destrieux
            continue
        for measure, prefix in measures.items():
            # Generate similarity matrix for given dataset / data point
            do_similarity(atlas=atlas, prefixes=[prefix],
                          metric='partial-correlation', measures=['Asymmetry Index'],
                          data_dir='generated/data',
                          output_dir='generated/plots', output_format='bokeh')


def generate_similarity_json():
    from ping.ping.data import prefixes
    from ping.scripts.similarity import do_similarity
    for atlas, measures in prefixes.items():
        if atlas == 'destrieux':  # skip destrieux
            continue
        for measure, prefix in measures.items():
            do_similarity(atlas=atlas, prefixes=[prefix],
                          metric='partial-correlation', measures=['Asymmetry Index'],
                          data_dir='generated/data',
                          output_dir='generated/data/fsaverage/' + atlas,
                          output_format='json')


def generate_multivariate():
    from ping.ping.data import prefixes
    from ping.scripts.multivariate import do_multivariate

    for atlas, measures in prefixes.items():
        if atlas == 'destrieux':  # skip destrieux
            continue
        for measure, prefix in measures.items():
            do_multivariate(prefixes=[prefix], atlas=atlas,
                            data_dir='generated/data',
                            output_dir='generated/data/fsaverage/' + atlas,
                            output_format='json',
                            verbose=0, pc_thresh=0.05)


def generate_regressions():
    from ping.ping.data import prefixes
    from ping.scripts.grouping import do_grouping
    for atlas, measures in prefixes.items():
        if atlas == 'destrieux':  # skip destrieux
            continue
        for measure, prefix in measures.items():
            for grouping_key in ['Gender', 'FDH_23_Handedness_Prtcpnt']:
                do_grouping(prefixes=[prefix], grouping_keys=[grouping_key],
                            xaxis_key='Age_At_IMGExam',
                            plots='regressions', atlas='desikan',
                            data_dir='generated/data',
                            output_dir='generated/plots/regression/',
                            output_type='matplotlib')


if __name__ == '__main__':
    # generate_all_brains()
    # generate_manhattan()
    # generate_scatter_bokeh()
    # generate_similarity_bokeh()
    # generate_similarity_json()
    # generate_multivariate()
    generate_regressions()
