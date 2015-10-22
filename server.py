"""
Create a website with all plots available. Url schema is as follows:

/brain/
/brain/data/fsaverage/desikan/pial/Desikan_area_lh_files_to_load.json
/gwas/(index.html)
/gwas/data/
/scatter/(plot).html
/similarity/(plot).html


"""

import glob
import os
import os.path as osp
import shutil

import flask
import simplejson

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import JS_RESOURCES, CSS_RESOURCES
from bokeh.util.string import encode_utf8


def serve_index():
    return """
        <html><head><meta http-equiv="refresh" content="0;2015/index.html"></head></html>
        """


def deploy():
    """ Take all the disparate apps, and create a directory structure that works
    on a static webserver with no urlconf."""
    def mkdirp(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def copytree(f1, f2):
        if osp.exists(f2):
            shutil.rmtree(f2)
        shutil.copytree(f1, f2)

    def symlink(p1, p2):
        if osp.exists(p2):
            try:
                os.remove(p2)
            except:
                shutil.rmtree(p2)
        os.symlink(osp.abspath(p1), p2)

    def pathof(modpath):
        mod = __import__(modpath)
        path = os.path.dirname(mod.__file__)
        print(mod.__file__)
        return path

    app = flask.Flask(__name__, static_url_path='/static')
    ping_viz_path = osp.join(pathof('ping'), 'viz')
    roygbiv_web_path = osp.join(pathof('roygbiv'), 'web')

    try:

        # Poster
        mkdirp('deploy')
        copytree('2015', 'deploy/2015')

        # Brain
        copytree(roygbiv_web_path, 'deploy/brain')
        for fil in glob.glob('brain/*.html'):
            shutil.copy(fil, 'deploy/' + fil)
        shutil.copy('brain/two_hemis.html', 'deploy/brain/index.html')
        for fil in glob.glob('brain/css/*') + glob.glob('brain/js/*'):
            shutil.copy(fil, 'deploy/' + fil)
        mkdirp('deploy/brain/data')
        copytree('generated/data/fsaverage', 'deploy/brain/data/fsaverage')  # data

        # Manhattan
        mkdirp('deploy/gwas')
        copytree(osp.join(ping_viz_path, 'manhattan'), 'deploy/gwas')
        shutil.copyfile('deploy/gwas/manhattan.html', 'deploy/gwas/index.html')
        mkdirp('deploy/gwas/data')
        for fil in glob.glob('generated/data/*.json'):
            shutil.copyfile(fil, os.path.join('deploy/gwas/data', os.path.basename(fil)))

        # scatter / similarity plots
        copytree('generated/plots', 'deploy/plots')

        # Create the default page.
        with open('deploy/index.html', 'w') as fp:
            fp.write(serve_index())

        # Finally, try and reduce snp file size.
        with open('deploy/gwas/data/SNPS_all.json', 'r') as fp:
            snps = simplejson.load(fp)
        with open('deploy/gwas/data/GWAS_MRI_cort_area_ctx_frontalpole_AI__Age_At_IMGExam.json', 'r') as fp:
            gwas = simplejson.load(fp)
        snps = dict([(k, v) for k, v in snps.items()
                     if k in gwas[gwas.keys()[0]]])
        with open('deploy/gwas/data/snps_all.json', 'w') as fp:
            simplejson.dump(snps, fp)

    except Exception as e:
        print("Error deploying: %s" % e)

    def serve():
        app.route('/')(serve_index)

        @app.route('/<path:path>')
        def serve_brain_data(path):
            return flask.send_from_directory('deploy', path)
        app.run()
    serve()


def server_it():
    """ Take the mess, and create a flask webserver that knows how to route things
    to make them work.
    """

    app = flask.Flask(__name__, static_url_path='/static')

    app.route('/')(serve_index)


    @app.route('/brain/data/<path:path>')
    def serve_brain_data(path):
        data_dir = 'generated/data'
        return flask.send_from_directory(data_dir, path)

    @app.route('/brain/<path:path>')
    def serve_roygbiv_html(path):
        try:
            return flask.send_from_directory('brain', path)
        except Exception as e:
            import roygbiv
            viz_dir = os.path.join(os.path.dirname(roygbiv.__file__), 'web')
            print viz_dir, path
            return flask.send_from_directory(viz_dir, path)

    # GWAS app
    @app.route('/gwas/data/<path:path>')
    def serve_gwas_data(path):
        data_dir = 'generated/data'
        return flask.send_from_directory(data_dir, path)

    @app.route('/gwas/')
    @app.route('/gwas/index.html')
    def serve_default():
        import ping.viz
        viz_dir = os.path.dirname(ping.viz.__file__)
        man_dir = os.path.join(viz_dir, 'manhattan')
        return flask.send_from_directory(man_dir, 'manhattan.html')

    @app.route('/gwas/<path:path>')
    def serve_gwas_html(path):
        import ping.viz
        viz_dir = os.path.dirname(ping.viz.__file__)
        man_dir = os.path.join(viz_dir, 'manhattan')
        return flask.send_from_directory(man_dir, path)

    # Scatter app
    @app.route('/plots/<path:path>')
    def serve_plot(path):
        return flask.send_from_directory('generated/plots', path)
    @app.route('/2015/<path:path>')
    def serve_old(path):
        return flask.send_from_directory('2015', path)
    app.debug = True
    app.run()

if __name__ == "__main__":
    import threading
    import webbrowser

    # threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000/gwas/manhattan/manhattan.html')).start()
    # deploy()
    server_it()
