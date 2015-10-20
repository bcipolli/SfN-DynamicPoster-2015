var app = angular.module('navigator', []);
app.controller('NavigateController', ['$scope', function($scope) {
    // Object bound to the form. We "watch" this object below.
    $scope.metadata = {
        subject: 'fsaverage',
        atlas: 'destrieux',
        surf_type: 'pial',
        prefix: 'Destrieux_area.',
        measure: 'area'
    };
    $scope.manifest_url = build_manifest_url('data', $scope.metadata);
    $scope.data_url = build_data_url('data', $scope.metadata);

    // Create the right hemi brain
    $scope.plotter = new HemiPlotter({
        divIDs: ["master-brain", "slave-brain"],
        manifest_url: $scope.manifest_url,
        data_url: $scope.data_url,
        value_keys: value_keys || null,
        callback: function(mesh) {
            // Show the mesh info
            $scope.mesh = mesh;
            $scope.$apply();
        }
    });

    // Use the relatively new watchCollection().
    $scope.$watchCollection("metadata", function( newValue, oldValue ) {
        $scope.metadata.prefix = measure2prefix(newValue.measure, newValue.atlas);

        manifest_url = build_manifest_url('data', $scope.metadata);
        data_url = build_data_url('data', $scope.metadata);
        if (manifest_url != $scope.manifest_url) {
            $scope.manifest_url = manifest_url;
            if (data_url != $scope.data_url)
                $scope.data_url = data_url;
            $scope.plotter.loadBrains({
                manifest_url: $scope.manifest_url,
                data_url: $scope.data_url
            });
        }
    });
}]);