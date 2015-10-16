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

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import JS_RESOURCES, CSS_RESOURCES
from bokeh.util.string import encode_utf8


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

    # Poster
    mkdirp('deploy')
    copytree('2014', 'deploy')

    # Brain
    mkdirp('deploy/brain')  # basedir
    copytree(roygbiv_web_path, 'deploy/brain')
    symlink('deploy/brain/two_hemis.html', 'deploy/brain/index.html')
    mkdirp('deploy/brain/data')
    symlink('data/fsaverage', 'deploy/brain/data/fsaverage')  # data

    # Manhattan
    mkdirp('deploy/gwas')
    copytree(osp.join(ping_viz_path, 'manhattan'), 'deploy/gwas')
    symlink('deploy/gwas/manhattan.html', 'deploy/gwas/index.html')
    mkdirp('deploy/gwas/data')
    for fil in glob.glob('data/*.json'):
        symlink(fil, os.path.join('deploy/gwas', fil))  # data

    # scatter / similarity plots
    mkdirp('deploy/scatter')
    symlink('plots/scatter.html', 'deploy/scatter/index.html')
    mkdirp('deploy/similarity')
    symlink('plots/similarity.html', 'deploy/similarity/index.html')

    def serve():
        @app.route('/')
        def serve_index():
            return """
                <a href='index.html.html'>Old poster</a>
                <a href='brain/index.html'>Two hemis</a>
                <a href='gwas/index.html'>Manhattan</a>
                <a href='scatter/index.html'>Scatter</a> (just one measure)
                <a href='similarity/index.html'>Similarity</a> (just one measure)
                """

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

    @app.route('/')
    def serve_poster():
        return ""

    @app.route('/brain/data/<path:path>')
    def serve_brain_data(path):
        data_dir = 'data'
        return flask.send_from_directory(data_dir, path)

    @app.route('/brain/<path:path>')
    def serve_brain_html(path):
        import roygbiv
        viz_dir = os.path.join(os.path.dirname(roygbiv.__file__), '..', 'web')
        return flask.send_from_directory(viz_dir, path)

    @app.route('/gwas/<path:foo>/data/<path:path>')
    def serve_gwas_data(foo, path):
        data_dir = 'data'
        return flask.send_from_directory(data_dir, path)

    @app.route('/gwas/<path:path>')
    def serve_gwas_html(path):
        import ping.viz
        viz_dir = os.path.dirname(ping.viz.__file__)
        return flask.send_from_directory(viz_dir, path)

    app.debug = True
    app.run()

if __name__ == "__main__":
    import threading
    import webbrowser

    # threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000/gwas/manhattan/manhattan.html')).start()
    deploy()
