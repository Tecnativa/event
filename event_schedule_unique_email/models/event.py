# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models

class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.multi
    def mail_attendees(self, template_id, force_send=False):
        self.ensure_one()
        l = []
        for attendee in self.registration_ids:
            if attendee.email not in l:
                self.env['mail.template'].browse(
                    template_id).send_mail(attendee.id,force_send=force_send)
                l.append(attendee.email)