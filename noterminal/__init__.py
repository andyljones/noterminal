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
        # Create a new notebook in a temp dir
        # Set its working directory?
        # Redirect the requester to it
        # Need a frontend extension to put in a 'im leaving' request on `onbeforeunload`
        # Leaving request ends the session and deletes the notebook
        self.finish('Hello, world!')


def load_jupyter_server_extension(nb_server_app):
    app = nb_server_app.web_app

    route = url_path_join(app.settings['base_url'], '/noterminal')
    app.add_handlers('.*$', [(route, NoterminalHandler)])