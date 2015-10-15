=== Poster Design: ===

* create jinja2 template for poster.
* create some static javascript functions
* import all needed files (brain.js, bokeh.js, etc.)
* create python code to generate plots as needed
    => AS A SERVER.
* Listen to events from all the different plots.
    => Update data source for regression.
    => Update selections for others.
* All plots have a CustomJS to update the brain, using library
    functions in brain.js.

EASY.


=== What's done: ===
* manhattan plot (ish) - running from poster!
    `python gwas.py display MRI_cort_area_ctx_frontalpole_AI --output-format flask`
* Brain navigator with stats
    `python brain.py MRI_cort_area.ctx. AI:mean --output-format flask`
* Scatter plot
    `python scatter.py MRI_cort_area.ctx. AI:mean AI:std LH_PLUS_RH:mean --output-format bokeh`
* Similarity matrix
    `python similarity.py MRI_cort_area.ctx partial-correlation "Asymmetry Index" --output-format bokeh` (note the funky missing dot on the prefix)

=== To do:===
* move selector code OUT of roygbiv and into SfN2015
* make bokeh plots output to data or plots dir.
* combine flask server into one uber-server, from all the apps.
    * use urls like /[app]/[plot]/...
* deployment script - to copy files to a structure that will work for non-flask servers (no url re-routing)

* Regression plots - multiple per area, based on what you want to see (age, gender, both). Plot both when brain is clicked.
* Export / import of data
* Correlation between thickness and area
* GWAS on frontal pole
* Brain map for PCA components
* interactions between plots

Must:
* Make a poster
* put things on the poster!
