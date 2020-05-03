// The outline for this code is largely lifted from [this extension](https://github.com/ipython-contrib/jupyter_contrib_nbextensions/blob/6af8e5e84e4746476c5b476b7e38f63d7abb2064/src/jupyter_contrib_nbextensions/nbextensions/runtools/main.js)

define([
    'jquery',
    'base/js/events',
    'base/js/namespace'
], function($, events, Jupyter) {
    "use strict";

    function add_delete_action() {
        var handler = function () {
            var path = Jupyter.notebook.notebook_path;
            var kernel = Jupyter.notebook.kernel.id;
            $.get('/noterminal/delete', {'path': path, 'kernel': kernel});
        };

        var action = {
            icon: 'fa-comment-plus-square', // a font-awesome class used on buttons, etc
            help    : 'Delete a noterminal notebook',
            help_index : 'zz',
            handler : handler
        };

        Jupyter.actions.register(action, 'delete', 'noterminal');
        Jupyter.keyboard_manager.command_shortcuts.add_shortcut('d,d', 'noterminal:delete');
    }

    function add_open_action() {
        var handler = function () {
            window.open('/noterminal', '_blank');
        };

        var action = {
            icon: 'fa-comment-plus-square', // a font-awesome class used on buttons, etc
            help    : 'Create a new noterminal notebook',
            help_index : 'zz',
            handler : handler
        };

        Jupyter.actions.register(action, 'create', 'noterminal');
        Jupyter.keyboard_manager.command_shortcuts.add_shortcut('t,t', 'noterminal:create');
    }

    function init() {
        add_exit_event();
        add_open_action();
        add_delete_action();
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
