"""
"""

import os

from ping.scripts.brain import do_roygbiv


prefixes = dict(desikan=dict(area='MRI_cort_area.ctx.', thickness='MRI_cort_thick.ctx.'),
                destrieux=dict(area='Destrieux_area.', thickness='Destrieux_thickness.'))

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
