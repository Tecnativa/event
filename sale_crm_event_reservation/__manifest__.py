# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Create event quotations from opportunities",
    "summary": "Combine event reservations, opportunities and quotations",
    "version": "12.0.1.0.0",
    "development_status": "Production/Stable",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Yajo"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": ["crm_event", "event_sale_reservation", "sale_crm"],
    "data": [
        # "security/some_model_security.xml",
        # "security/ir.model.access.csv",
        # "templates/assets.xml",
        # "views/report_name.xml",
        # "views/res_partner_view.xml",
        "wizards/crm_lead_event_sale_wizard_views.xml",
        "views/crm_lead_views.xml",
    ],
    "demo": [
        # "demo/assets.xml",
        # "demo/res_partner_demo.xml",
    ],
    "qweb": [
        # "static/src/xml/module_name.xml",
    ],
}
