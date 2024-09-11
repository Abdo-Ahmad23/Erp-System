# Copyright (C) Softhealer Technologies.

from odoo import api, SUPERUSER_ID
from . import models


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if env.ref('sh_pos_all_in_one_retail.sh_assets_js_frontend'):
        env.ref('sh_pos_all_in_one_retail.sh_assets_js_frontend').write({'active': False})
