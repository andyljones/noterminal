Sometimes you want a transient notebook. This extension adds a `/noterminal` endpoint to Jupyter that creates a new, empty notebook in a temporary directory, then deletes it when you close the tab. 

Once in a notebook, you can create a new noterminal with `noterminal:create` entry in the command palette, or the `T,T` shortcut.

### Dev Install
Install the server extension:
```sh
pip install -e noterminal
```
then add it to your `.jupyter/jupyter_notebook_config.json` file, a la
```json
{
  "NotebookApp": {
    "nbserver_extensions": {
      "jupyter_nbextensions_configurator": true,
      "noterminal": true
    }
  }
}
```
Now install the frontend:
```
jupyter nbextension install noterminal/noterminal
jupyter nbextension enable noterminal
```
You might have to then run `jupyter nbextension list` and edit the `.jupyter/nbconfig/notebook.json` file to replace `noterminal` with `noterminal/main`. I think the yaml file should be doing this automatically, I'm not sure why it currently isn't.