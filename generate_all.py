"""
master script to generate all data.
"""

import os.path as op


def generate_all_brains(data_dir=op.join('generated', 'data'),
                        output_dir=op.join('generated', 'data')):
    """ Generate all VTK files used by roygbiv (2D surface plot)"""
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
                                      sample_rate=0.1, force=False,
                                      data_dir=data_dir,
                                      output_dir=output_dir)
                        do_roygbiv(**kwargs)


def generate_manhattan(data_dir=op.join('generated', 'data'),
                        output_dir=op.join('generated', 'data')):
    """ Generate genetic metadata and JSON for manhattan plot."""
    from ping.scripts.gwas import do_gwas

    do_gwas(action='display', measures='MRI_cort_area_ctx_frontalpole_AI',
            covariates=['Age_At_IMGExam'], data_dir=data_dir,
            output_dir=output_dir, output_format='json')


def generate_scatter_bokeh(data_dir=op.join('generated', 'data'),
                           output_dir=op.join('generated', 'plots')):
    """ Various scatter plots"""
    import os

    from ping.ping.data import prefixes
    from ping.scripts.scatter import do_scatter
    from ping.scripts.similarity import do_similarity

    for atlas, measures in prefixes.items():
        # Generate area vs. thickness plots
        if atlas.lower() == 'destrieux':
            continue

        # Thickness vs. area
        do_scatter(atlas=atlas, prefixes=[os.path.commonprefix(measures.values())],
                   x_key='%s:AI:mean' % measures['area'],
                   y_key='%s:AI:mean' % measures['thickness'],
                   title="Area vs. thickness",
                   data_dir=data_dir,
                   output_dir=output_dir,
                   output_format='bokeh')

        for measure, prefix in measures.items():
            # Generate scatter plot for given dataset / data point
            do_scatter(atlas=atlas, prefixes=[prefix], x_key='AI:mean',
                       y_key='AI:std', size_key='LH_PLUS_RH:mean',
                       data_dir=data_dir,
                       output_dir=output_dir,
                       output_format='bokeh')


def generate_similarity_bokeh(data_dir=op.join('generated', 'data'),
                              output_dir=op.join('generated', 'plots', 'similarity')):
    """ Asymmetry partial correlation matrix"""
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
                          data_dir=data_dir,
                          output_dir=output_dir, output_format='bokeh')


def generate_similarity_json(data_dir=op.join('generated', 'data'),
                             output_dir=op.join('generated', 'data')):
    """ Asymmetry partial correlation data as json overlay for roygbiv"""
    from ping.ping.data import prefixes
    from ping.scripts.similarity import do_similarity

    for atlas, measures in prefixes.items():
        if atlas == 'destrieux':  # skip destrieux
            continue
        for measure, prefix in measures.items():
            do_similarity(atlas=atlas, prefixes=[prefix],
                          metric='partial-correlation', measures=['Asymmetry Index'],
                          data_dir=data_dir,
                          output_dir=op.join(output_dir, 'fsaverage', atlas),
                          output_format='json')


def generate_multivariate(data_dir=op.join('generated', 'data'),
                          output_dir=op.join('generated', 'data')):
    """ PCA overlay for roygbiv"""
    from ping.ping.data import prefixes
    from ping.scripts.multivariate import do_multivariate

    for atlas, measures in prefixes.items():
        if atlas == 'destrieux':  # skip destrieux
            continue
        for measure, prefix in measures.items():
            do_multivariate(prefixes=[prefix], atlas=atlas,
                            data_dir=data_dir,
                            output_dir=op.join(output_dir, 'fsaverage', atlas),
                            output_format='json',
                            verbose=0, pc_thresh=0.05)


def generate_regressions(data_dir=op.join('generated', 'data'),
                         output_dir=op.join('generated', 'plots', 'regression')):
    """ Regression between age and value, grouped by gender/handedness"""
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
                            data_dir=data_dir,
                            output_dir=output_dir,
                            output_type='matplotlib')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('command', default=None)
    parser.add_argument('--data-dir', nargs='?', default=op.join('generated', 'data'))
    parser.add_argument('--output-dir', nargs='?', default=op.join('generated'))
    args = parser.parse_args()

    args_dict = vars(args)
    command = args.command
    del args_dict['command']

    if command is None or command == 'brain':
        args_dict['output_dir'] = op.join(args.output_dir, 'data')
        generate_all_brains(**args_dict)

    if command is None or command == 'manhattan':
        args_dict['output_dir'] = op.join(args.output_dir, 'data')
        generate_manhattan(**args_dict)

    if command is None or command == 'scatter':
        args_dict['output_dir'] = op.join(args.output_dir, 'plots', command)
        generate_scatter_bokeh(**args_dict)

    if command is None or command == 'similarity':
        args_dict['output_dir'] = op.join(args.output_dir, 'plots', command)
        generate_similarity_bokeh(**args_dict)
        args_dict['output_dir'] = op.join(args.output_dir, 'data')
        generate_similarity_json(**args_dict)

    if command is None or command == 'multivariate':
        args_dict['output_dir'] = op.join(args.output_dir, 'data')
        generate_multivariate(**args_dict)

    if command is None or command == 'regression':
        args_dict['output_dir'] = op.join(args.output_dir, 'plots', command)
        generate_regressions(**args_dict)
