Sometimes you want a transient notebook. This extension adds a `t,t` shortcut to create a new, temporary notebook, and a `q,q` shortcut to destroy it.

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


### TODO
Together with stripcommon, this is most of the way to a terminal-esque experience. The final step would be to add  i-search-esque functionality to search back through previous cells