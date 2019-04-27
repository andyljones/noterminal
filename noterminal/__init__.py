"""Following https://jupyter-notebook.readthedocs.io/en/stable/extending/handlers.html

Test it with
```
jupyter notebook --NotebookApp.nbserver_extensions="{'noterminal':True}"  
```
"""

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from pathlib import Path
import uuid
import aljpy

CACHE = Path('.cache')
DEFAULT = """{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 2}"""

class NoterminalHandler(IPythonHandler):

    def get(self):
        path = CACHE / 'noterminal' / f'{aljpy.humanhash(n=2)}.ipynb'
        self.log.info(f'Creating noterminal at {path}')
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(DEFAULT)
        self.redirect(f'/notebooks/{path}')

class ExitHandler(IPythonHandler):

    def get(self):
        path = Path(self.get_argument('path', ''))
        kernel = self.get_argument('kernel', '')
        if path and (CACHE in path.parents):
            self.log.info(f'Removing noterminal at {path}')
            self.kernel_manager.shutdown_kernel(kernel)
            path.unlink() 



def load_jupyter_server_extension(nb_server_app):
    app = nb_server_app.web_app

    route = url_path_join(app.settings['base_url'], '/noterminal')
    app.add_handlers('.*$', [(route, NoterminalHandler)])

    route = url_path_join(app.settings['base_url'], '/exit')
    app.add_handlers('.*$', [(route, ExitHandler)])
