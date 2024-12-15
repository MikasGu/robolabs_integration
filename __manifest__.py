{
    "name": "RoboLabs Integration",
    "version": "17.0.0.0.1",
    "license": "Other proprietary",
    "author": "Mikas Gudzinevičius",
    "contributors": [
        "Mikas Gudzinevičius <gudzineviciusm@gmail.com>",
    ],
    "category": "Accounting",
    "depends": [
        "base",
    ],

    "data": [
        "security/ir.model.access.csv",
        "data/robo_filters.xml",
        "views/res_config_settings_views.xml",
        "views/robolabs_views.xml",
        "wizard/robo_wizards_views.xml",
    ],

    "installable": True,
    "application": True,

}
