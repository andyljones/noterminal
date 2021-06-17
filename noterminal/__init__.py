"""Following https://jupyter-notebook.readthedocs.io/en/stable/extending/handlers.html

Test it with
```
jupyter notebook --NotebookApp.nbserver_extensions="{'noterminal':True}"  
```
"""

from tornado import web
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from pathlib import Path
import uuid
import aljpy
from urllib.parse import unquote

DEFAULT = """{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 2}"""

class NoterminalHandler(IPythonHandler):

    @web.authenticated
    def get(self):
        path = Path(self.request.path)
        # If the frontend's sent us a full ipynb path, then get the parent
        if path.suffix != '':
            path = path.parent

        dir = path.relative_to('/noterminal-create')

        api_path = dir / f'.{aljpy.humanhash(n=2)}.ipynb'
        os_path = Path(self.contents_manager._get_os_path(str(api_path)))
        if os_path.parent.exists():
            self.log.info(f'Creating noterminal at {api_path}')
            #TODO: Do this via the contents_manager
            os_path.write_text(DEFAULT)
            self.redirect(f'/notebooks/{api_path}')
        else:
            self.send_error(400)


class DeleteHandler(IPythonHandler):

    @web.authenticated
    def get(self):
        api_path = unquote(self.get_argument('path', ''))
        kernel = self.get_argument('kernel', '')
        if Path(api_path).name.startswith('.'):
            self.log.info(f'Removing noterminal at {api_path}')
            self.kernel_manager.shutdown_kernel(kernel)
            os_path = Path(self.contents_manager._get_os_path(api_path))
            os_path.unlink() 
        else:
            self.log.info('No noterminal notebook at {api_path} to remove')

def load_jupyter_server_extension(nb_server_app):
    app = nb_server_app.web_app

    route = url_path_join(app.settings['base_url'], '/noterminal-create/?.*')
    app.add_handlers('.*$', [(route, NoterminalHandler)])

    route = url_path_join(app.settings['base_url'], '/noterminal-delete.*')
    app.add_handlers('.*$', [(route, DeleteHandler)])
