function load_index() {
    // Bring us back to the original page; clear all divs.
    window.location.href = "#";
    if ($('#poster-footer').is(":visible")) {
        window.location.reload();
    }
}

/* Builds the poster cover-page elements */
$(function() {

    $('.poster-title').each(function() {
        // Add the left logo, center area, right QR code.
        //  data-logo="logo.png"
        //  data-qrcode="qrcode.png"
        //  data-title="Blah"
        //  data-authors="Ben Cipollini, Garrison Cottrell"
        //  data-affiliations="UC San Diego, Department of Computer Science"
        //  data-author-affiliations="1,1">

        var title_div = $(this);
        var d = title_div.data();
        title_div.append("<div class='spacer logo'><a href='javascript:load_index()'><img src='" + d["logo"] + "' /></a></div>");
        title_div.append("<div class='content'>"
            + "<div class='title'><a href='javascript:load_index()' style='font-weight: normal; text-decoration: none; color: black'>" + d["title"] + "</a></div>"
            + "<div class='authors'>" + d["authors"] + "</div>"
            + "<div class='affiliations'>" + d["affiliations"] + "</div>"
            + "</div>");
        // Generate at http://www.qr-code-generator.com/
        title_div.append("<div class='spacer qrcode'>"
            + "<div class='download-text'>Scan to access online now,</div>"
            + "<div><img src='" + d["qrcode"] + "' /></div>"
            + "<div class='download-text'>or visit <a href='http://tinyurl.com/sfn15-asymmetry'>tinyurl.com/sfn15-asymmetry</a>!</div>");
    });

    $('.section').each(function(idx) {

        //data-number
        //data-title="Are human brains lateralized because they are large?"
        //data-image=""
        //data-blurb="The human brain is highly lateralized and somehat large.  Are the to connected?"
        var section_div = $(this);
        var d = section_div.data();
        section_div.attr("id", "section" + (idx+1));

        // Move children to the main content.
        var main_div = $('#main-content');
        var children = section_div.children();
        var details_div_id = "details" + idx;

        section_div.data["details_div_id"] = details_div_id
        main_div.append("<div id='" + details_div_id + "' class='section-details'></div>");
        var details_div = main_div.find('#' + details_div_id);
        details_div.append(children);
        //section_div.remove(children);

        // Add the data to the actual div
        section_div.append("<div class='number'>" + d["number"] + "</div>");
        section_div.append("<div class='title'>" + d["title"] + "&nbsp;</div>");
        if (d["image"]) {
            section_div.append("<div class='image'><img src='" + d["image"] + "' /></div>");
        }
        section_div.append("<div class='blurb short-blurb'>" + (d["shortBlurb"] ? d["shortBlurb"] : d["blurb"]) + "</div>");
        section_div.append("<div class='blurb'>" + d["blurb"] + "</div>");


        // Show the relevant details, and make the buttons active.
        $(this).on('click', function() {
            var div = $("#" + details_div_id)
            if (!div.is(":visible")) {
                $('.section-details').hide();
                div.show(500);
                location.hash = "#b" + d['number'];
            }
        });
    });

});


/* Builds the poster main section elements */
