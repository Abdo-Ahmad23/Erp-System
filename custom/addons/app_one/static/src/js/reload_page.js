odoo.define('your_module.reload_page', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var ReloadPage = Widget.extend({
        events: {
            'click .o_reload_button': '_onReloadClick',
        },

        _onReloadClick: function () {
            location.reload();
        },
    });

    core.action_registry.add('reload_page_action', ReloadPage);
});
