var prefixes = {
    desikan: { area: 'MRI_cort_area.ctx.', thickness: 'MRI_cort_thick.ctx.', volume: 'MRI_cort_vol.ctx.'},
    destrieux: { area: 'Destrieux_area.', thickness: 'Destrieux_thickness.'}
}

function prefix2measure(prefix) {
    for (var ai in prefixes) {
        for (var mi in prefixes[ai]) {
            if (prefixes[ai][mi] == prefix)
                return mi
        }
    }
}

function measure2prefix(measure, atlas) {
    return prefixes[atlas][measure]
}

function click_partner_function(partner_brain) {
    return function(mesh) {
        if (mesh) {
            // On click, select the same mesh in the "stats" brain.
            var other_mesh = partner_brain.selectMeshByName(mesh.name);
            partner_brain.objectPick(other_mesh);
        }
    }
}

function build_manifest_url(base_url, metadata) {
    return base_url + '/' + metadata.subject + '/'
                    + metadata.atlas + '/' + metadata.surf_type + '/'
                    + metadata.prefix + 'lh_files_to_load.json';
}
