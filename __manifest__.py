# -*- coding: utf-8 -*-
{
    'name': "shopify_mint",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [

        'security/ir.model.access.csv',
# 'security/security_group.xml',
        'views/res_config_settings_views.xml',

        'views/shopify_app.xml',
        'views/templates.xml',
        'views/instagram_data.xml',
        'views/media.xml',
        'views/product.xml',
        'views/widget.xml',
        'views/media_comments.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
