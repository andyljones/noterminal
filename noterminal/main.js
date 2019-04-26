// The outline for this code is largely lifted from [this extension](https://github.com/ipython-contrib/jupyter_contrib_nbextensions/blob/6af8e5e84e4746476c5b476b7e38f63d7abb2064/src/jupyter_contrib_nbextensions/nbextensions/runtools/main.js)

define([
    'jquery',
    'base/js/events',
    'base/js/namespace'
], function($, events, Jupyter) {
    "use strict";

    function init() {
        $(window).on('beforeunload', function () { 
            var path = Jupyter.notebook.notebook_path
            $.get('exit', {'path': path});
        });
        return null;
    }

    function load_extension() {
        if (Jupyter.notebook._fully_loaded) {
            init();
        } else {
            events.one('notebook_loaded.Notebook', init);
        }
    }

    return {
        load_ipython_extension: load_extension,
        load_jupyter_extension: load_extension
    };
});
