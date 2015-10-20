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


def serve_index():
    return """
        <a href='2015/index.html'>Old poster</a>
        <a href='brain/two_hemis.html'>Two hemis</a>
        <a href='gwas/manhattan/manhattan.html'>Manhattan</a>
        <a href='scatter/index.html'>Scatter</a> (just one measure)
        <a href='similarity/index.html'>Similarity</a> (just one measure)
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

    # Poster
    mkdirp('deploy')
    copytree('2015', 'deploy')

    # Brain
    mkdirp('deploy/brain')  # basedir
    copytree(roygbiv_web_path, 'deploy/brain')
    shutil.copy('brain/two_hemis.html', 'deploy/brain/index.html')
    copytree('brain/css/', 'deploy/brain/css/')
    copytree('brain/js/', 'deploy/brain/js/')
    mkdirp('deploy/brain/data')
    symlink('generated/data/fsaverage', 'deploy/brain/data/fsaverage')  # data

    # Manhattan
    mkdirp('deploy/gwas')
    copytree(osp.join(ping_viz_path, 'manhattan'), 'deploy/gwas')
    symlink('deploy/gwas/manhattan.html', 'deploy/gwas/index.html')
    mkdirp('deploy/gwas/data')
    for fil in glob.glob('generated/data/*.json'):
        symlink(fil, os.path.join('deploy/gwas/data', os.path.basename(fil)))

    # scatter / similarity plots
    mkdirp('deploy/scatter')
    symlink('plots/scatter.html', 'deploy/scatter/index.html')
    mkdirp('deploy/similarity')
    symlink('plots/similarity.html', 'deploy/similarity/index.html')

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
