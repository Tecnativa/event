# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    seats_available_total = fields.Char(
        string="Events (seats)",
        compute="_compute_event_totals",
        help="Upcoming/running events of this type (and available seats).",
    )
    seats_wanted_total = fields.Char(
        string="Opportunities (seats)",
        compute="_compute_opportunities_totals",
        help="Open opportunities for events of this type (and wanted seats).",
    )

    def _compute_event_totals(self):
        """Get how many open events and available seats exist."""
        domain = [
            ("event_type_id", "in", self.ids),
            # The following domain is the same as upstream's "Upcoming/Running"
            # filter, which is the default when opening events view. It'd be
            # more correct to filter for `date_end >= fields.Datetime.now()`,
            # to exclude events that finished earlier today. However, that
            # would make the smart button display a different count than the
            # events when clicking on it, so it seems more user-friendly to
            # include these events, even if they finished earlier today.
            ("date_end", ">=", fields.Date.today()),
            ("state", "!=", "cancel"),
        ]
        types_with_unlimited_seats = (
            self.env["event.event"]
            .search(
                domain + [("seats_availability", "=", "unlimited")],
            )
            .mapped("event_type_id")
        )
        results = self.env["event.event"].read_group(
            domain=domain,
            fields=["seats_available"],
            groupby=["event_type_id"],
        )
        translated_unlimited = dict(
            self.env["event.event"].fields_get(["seats_availability"])[
                "seats_availability"
            ]["selection"]
        )["unlimited"]
        totals = {group["event_type_id"][0]: group for group in results}
        for one in self:
            totals_item = totals.get(one.id, {})
            event_count = totals_item.get("event_type_id_count", 0)
            seats_sum = (
                translated_unlimited
                if one in types_with_unlimited_seats
                else totals_item.get("seats_available", "0")
            )
            one.seats_available_total = "%d (%s)" % (event_count, seats_sum)

    def _compute_opportunities_totals(self):
        """Get how many open opportunities and wanted seats exist."""
        results = self.env["crm.lead"].read_group(
            domain=[
                ("event_type_id", "in", self.ids),
                ("type", "=", "opportunity"),
                # Ignore won opportunities
                ("probability", "<", "100"),
            ],
            fields=["seats_wanted"],
            groupby="event_type_id",
            orderby="id",
        )
        totals = {group["event_type_id"][0]: group for group in results}
        for one in self:
            totals_item = totals.get(one.id, {})
            oppt_count = totals_item.get("event_type_id_count", 0)
            seats_sum = totals_item.get("seats_wanted", 0)
            one.seats_wanted_total = "%d (%d)" % (oppt_count, seats_sum)
