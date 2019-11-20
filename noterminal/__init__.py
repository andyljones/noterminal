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

DEFAULT = """{"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 2}"""

IMMORTALS = set()

class NoterminalHandler(IPythonHandler):

    @web.authenticated
    def get(self):
        api_path = f'.{aljpy.humanhash(n=2)}.ipynb'
        os_path = Path(self.contents_manager._get_os_path(api_path))
        self.log.info(f'Creating noterminal at {api_path}')
        #TODO: Do this via the contents_manager
        os_path.write_text(DEFAULT)
        self.redirect(f'/notebooks/{api_path}')

class ImmortalizeHandler(IPythonHandler):

    @web.authenticated
    def get(self):
        api_path = self.get_argument('path', '')
        self.log.info(f'Immortalizing {api_path}')
        #TODO: Carry this across restarts
        IMMORTALS.add(api_path)

class ExitHandler(IPythonHandler):

    @web.authenticated
    def get(self):
        api_path = self.get_argument('path', '')
        kernel = self.get_argument('kernel', '')
        if api_path.startswith('.'):
            if api_path in IMMORTALS:
                self.log.info(f'Tried to exit immortal {api_path}; ignoring')
            else:
                self.log.info(f'Removing noterminal at {api_path}')
                self.kernel_manager.shutdown_kernel(kernel)
                os_path = Path(self.contents_manager._get_os_path(api_path))
                os_path.unlink() 

def load_jupyter_server_extension(nb_server_app):
    app = nb_server_app.web_app

    route = url_path_join(app.settings['base_url'], '/noterminal')
    app.add_handlers('.*$', [(route, NoterminalHandler)])

    route = url_path_join(app.settings['base_url'], '/noterminal/immortalize')
    app.add_handlers('.*$', [(route, ImmortalizeHandler)])

    route = url_path_join(app.settings['base_url'], '/noterminal/exit')
    app.add_handlers('.*$', [(route, ExitHandler)])
