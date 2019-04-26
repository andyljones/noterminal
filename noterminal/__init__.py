"""Following https://jupyter-notebook.readthedocs.io/en/stable/extending/handlers.html

Test it with
```
jupyter notebook --NotebookApp.nbserver_extensions="{'noterminal':True}"  
```
"""

from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler

class NoterminalHandler(IPythonHandler):

    def get(self):
        self.finish('Hello, world!')


def load_jupyter_server_extension(nb_server_app):
    app = nb_server_app.web_app

    route = url_path_join(app.settings['base_url'], '/noterminal')
    app.add_handlers('.*$', [(route, NoterminalHandler)])