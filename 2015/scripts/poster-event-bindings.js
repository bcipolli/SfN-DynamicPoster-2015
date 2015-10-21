
/* Connects events to poster elements */
$(function() {
    var ad_fast = 200;
    var ad_slow = 500;

    $('.section-buttons-expanded .section').on('click', function(e){
        //e.preventDefault();

        // Expand the main content, shrink the summaries
        $('#main-content').toggleClass('main-content-collapsed', false, ad_slow);
        $('.section-buttons').toggleClass('section-buttons-expanded', false, ad_slow);
        $('.section').toggleClass('section-button', true, ad_slow);
        $('.section').find(".blurb").hide();
        $('.section').find(".short-blurb").show();
        $('#poster-footer').show(ad_slow, 'linear');
    });

    $('.section').on('click', function(e) {
        // e.preventDefault();

        // Turn off all but one of the summaries
        $('.section').toggleClass('section-summary-on', false, ad_slow);
        $(this).toggleClass('section-summary-on', true, ad_slow);
        $('#main-content').toggleClass('main-content-on', true, ad_slow);
    });

    // Set rounded corners on the right sides of left summaries
    $('#section-summary-left .section-summary').on('click', function(e) {
        $('.section-summary').toggleClass('section-summary-left-on', false);
        $('.section-summary').toggleClass('section-summary-right-on', false);
        $(this).toggleClass('section-summary-left-on'); });

    // Set rounded corners on the left sides of right summaries
    $('#section-summary-right .section-summary').on('click', function(e) {
        $('.section-summary').toggleClass('section-summary-left-on', false);
        $('.section-summary').toggleClass('section-summary-right-on', false);
        $(this).toggleClass('section-summary-right-on');
    });
});


/* content pane 1: model with demo activation */
$(function() {
    var ii = 0;
    $('#ringo-model').on('click', function(e, k) {
        ii = (ii < 25) ? ii + 1 : 0;
        $(this).find('img').attr('src', 'figs/cc/' + ii + '.png');
    });
});


/* content pane 2: animations */
$(function() {
    $('#animate-ringo').on('click', function(e) {
        e.preventDefault();
        $('#ringo-results-moving').animate({left: "171px"}, 1000, 'linear', function() { $('#no-diff').show();} );
    });
    $('#unanimate-ringo').on('click', function(e) {
        e.preventDefault();
        $('#ringo-results-moving').animate({left: "116px"}, 1000);
    });

    var ii = 1;
    $('#ringo-compare-movie').on('click', function(e) {
        ii = (ii < 25) ? ii + 1 : 1;
        $(this).find('#ringo-cc-movie img').attr('src', 'figs/cc/' + ii + '.png');
        $(this).find('#ringo-cc-no-movie img').attr('src', 'figs/cc-no/' + ii + '.png');
    });
});


function goto(res_id) {
    $scope = window.scope;
    $scope.resources.push(res_id);
    $scope.cur_resource = res_id;
    $scope.$apply();
    console.log(res_id);
    window.location.hash = '#' + res_id;
}


/* Now, parse out the bookmark */
$(function() {
    if (window.location.hash && window.location.hash.length > 1) {
        if (window.location.hash.substr(0,2) == "#b") {
            var sectionID = "#section" + window.location.hash.substr(2);
            console.log(sectionID);
            $(sectionID).trigger('click');
        } else {
            goto(window.location.hash.substr(1));
        }
    }
});
