# -*- coding: utf-8 -*-
{
    'name': "Garden Planner",

    'summary': """
        Tools for Micro Farms
        """,

    'description': """
        Tools for Micro Farms
    """,
    'license': 'OPL-1',
    'author': "mytime.click",
    'website': "https://www.mytime.click",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website, Instagram, Content,social-marketing,marketing-automation,blog,website,ecommerce',
    'version': '1.0',

    "price": 49.99,
    "currency": "EUR",
    'images': ['static/images/main_screenshot.png'],

    # any module necessary for this one to work correctly
    'depends': ["web", 'base',
                "website_blog",
                "website",
                "website_sale",
                "web_editor",
                "mass_mailing",
                ],

    # always loaded
    'data': [
        # "wizard/get_insta_posts.xml",
        'security/ir.model.access.csv',
        "views/crops_tab.xml"

    ],


    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'assets': {
    }
}
