# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime
from .. import misc
from odoo.exceptions import ValidationError


class crops(models.Model):
    #_name = "gardenplanner.blogtester"
    _description = 'crops'
    _inherit = "product.template"

    name_latein = fields.Char(string='Name Latein',
                              compute="_name_latein_neu", store=False)

    tag_ids = fields.Many2many(
        comodel_name="lisigruen.tags",
    )

    name_common = fields.Char(string='Vulgo')
    dtm = fields.Integer(string='DTM', compute="_dtm_from", store=False)
    generation = fields.Char(string='generation')
    image = fields.Binary(string="Image")

    # muss nur in Tagen und Monat angegeben werden
    aussaat = fields.Char(string='Aussaat', default="25.3")
    start_harvest = fields.Char(string='START OF HARVEST', default="25.3")
    end_harvest = fields.Char(string='END OF HARVEST', default="25.3")

    kw = fields.Char(string='KW')
    meter_aussat = fields.Char(string='Meter / Aussaat')
    reihen_beet = fields.Char(string='Reihen / Beet')
    abstand = fields.Char(string='Abstand in Reihe')
    platten = fields.Char(string='# Platten pro Aussaatmeter')

    # Platten pro Aussaatmeter * meter_aussat
    ges_platten = fields.Char(string='Gesamtanzahl Platten',
                              compute="_compute_ges_platten", store=False)

    anzahl_platten = fields.Char(string='Anzahl Platten')
    anzahl_zellen = fields.Char(string='Anzahl Zellen',
                                compute="_compute_anzahl_zellen", store=False)

    plattengr = fields.Char(string='Plattengröße')
    t_platte = fields.Integer(string='Tage in der Platte')
    pikieren = fields.Char(string='Pikieren',
                           compute="_compute_pikieren", store=False)  # wird nur in Tag und Monat ausgegeben
    abhaerten = fields.Char(string='Abhärten',
                            compute="_compute_aushaerten", store=False)  # wird nur in Tag und Monat ausgegeben
    auspflanzen = fields.Char(string='Auspflanzen',
                              compute="_compute_auspflanzen", store=False)  # wird nur in Tag und Monat ausgegeben
    erntefenster = fields.Integer(string='Erntefenster')
    erntebeginn = fields.Char(string='Erntebeginn',  # compute="_compute_erntebeginn",  # wird nur in Tag und Monat ausgegeben
                              store=False)
    # wird nur in Tag und Monat ausgegeben
    abernten = fields.Char(string='Abernten')
    active = fields.Boolean(string="Active", default=True)

    is_plant = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Plant'),
    ], default='0', index=True, string="Starred", tracking=True)

    # current_user = fields.Many2one('res.users','Current User', #default=lambda self: self.env.user    )
    #create_uid2=fields.Many2one('res.users',default=lambda self: self.env.user and self.env.user.id or False)

    additional_info = fields.Char(string='additional_info',
                                  # required=True
                                  )

    @api.depends('name')
    def _compute_visible_expense_policy(self):
        visibility = self.user_has_groups('analytic.group_analytic_accounting')
        for product_template in self:
            product_template.visible_expense_policy = visibility

    product_variant_ids = fields.One2many(
        'product.product', 'product_tmpl_id', 'Products', required=True)
    # performance: product_variant_id provides prefetching on the first product variant only
    product_variant_id = fields.Many2one(
        'product.product', 'Product', compute='_compute_product_variant_id')

    @api.depends('product_variant_ids')
    def _compute_product_variant_id(self):
        for p in self:
            p.product_variant_id = p.product_variant_ids[:1].id

    # after
    def _name_latein_neu(self):
        print("button clicked on button Nik")

        try:
            name_latein = self.env['lisigruen.sorten'].search(
                [('id', '=', int(self.hauptsorte_id.id))], limit=1).name_latein
            self.name_latein = name_latein
        except Exception as e:
            print(e)
            self.name_latein = "Error"

    def _dtm_from(self):

        try:
            dtm = self.env['lisigruen.sorten'].search(
                [('id', '=', int(self.hauptsorte_id.id))], limit=1).dtm
            self.dtm = dtm
        except Exception as e:
            print(e)
            self.dtm = 0  # "Error"

    def action_open_something(self):
        print("Testibus")
        return {
            "type": "ir.actions.act_window",
            "name": "Imported Mapping",
            "res_model": "lisigruen.crops",
            "view_mode": "tree,form",
            "target": "current",
        }

    def action_url(self):

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://apps.odoo.com/apps/modules/14.0/om_account_accountant',
        }

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        return super(Crops, self).copy(default)

    def print_report(self):
        return self.env.ref('nik_anbauplan.report_sorten_nik').report_action(self)

    @api.depends("ges_platten", "plattengr")
    def _compute_anzahl_zellen(self):
        for record in self:
            try:
                record.ges_platten = record.ges_platten.replace(",", ".")
                record.plattengr = record.plattengr.replace(",", ".")

                record.anzahl_zellen = str(
                    float(record.ges_platten) * float(record.plattengr))
            except Exception as e:
                print(e)
                print("Error with:" + str(record.ges_platten) +
                      " or " + str(record.plattengr))
                record.anzahl_zellen = str(99)

    @api.depends("meter_aussat", "platten")
    def _compute_ges_platten(self):
        for record in self:
            try:
                record.meter_aussat = record.meter_aussat.replace(",", ".")
                record.platten = record.platten.replace(",", ".")

                record.ges_platten = str(
                    float(record.meter_aussat) * float(record.platten))
            except Exception as e:
                print(e)
                print("Error with:" + str(record.meter_aussat) +
                      " or " + str(record.platten))
                record.ges_platten = str(99)

    @api.depends("aussaat", "t_platte")
    def _compute_auspflanzen(self):
        for record in self:
            date = misc.nikhelper.get_date_from_day_and_month(
                record.aussaat) + datetime.timedelta(days=record.t_platte)
            string = date.strftime("%d.%m")
            record.auspflanzen = date

    @api.depends("auspflanzen")
    def _compute_aushaerten(self):
        for record in self:
            date = misc.nikhelper.get_date_from_day_and_month(
                record.auspflanzen) + datetime.timedelta(days=-7)
            string = date.strftime("%d.%m")
            record.abhaerten = date

    @api.depends("abhaerten")
    def _compute_pikieren(self):
        for record in self:
            date = misc.nikhelper.get_date_from_day_and_month(
                record.abhaerten) + datetime.timedelta(days=-7)
            string = date.strftime("%d.%m")
            record.pikieren = date

    state = fields.Selection(
        [
            ("open", "Confirmed"),
            ("cancel", "Cancelled"),
            ("pending", "Pending"),
            ("done", "Held"),
        ],
        string="Status",
        tracking=3,
        default="open",
        help="The status is set to Confirmed, when a case is created.\n"
        "When the call is over, the status is set to Held.\n"
        "If the callis not applicable anymore, the status can be set "
        "to Cancelled.",
    )

    def action_confirm(self):
        print("button clicked on button Nik")
        self.state = "pending"

    def action_open(self):
        print("button clicked on button Nik")
        self.state = "open"

    @api.constrains("name")
    def check_name(self):
        for rec in self:
            patients = self.env["lisigruen.sorten"].search(
                [("name", "=", rec.name), ('id', "!=", rec.id)])
            if patients:
                raise ValidationError("Name %s Already Exists" % rec.name)


class Sorten(models.Model):
    _name = "lisigruen.sorten"
    _description = "Sorten"
    _sql_constraints = [
        ('name', 'unique (name)', 'The field  must be unique  !')
    ]

    name = fields.Char(string='Name Deutsch / S',
                       # required=True
                       unique=True
                       )
    name_latein = fields.Char(string='Name Latein / S')
    dtm = fields.Integer(string='DTM')

    #sorten_id = fields.One2many(   'product.template', 'hauptsorte_id', string="Sorten")

    @api.model
    def create(self, vals):
        #name = self.env['lisigruen.sorten'].search([('name', '=', record.name)], limit=2).name

        # default value für Sorte wenn keine Eingegeben wurde:

        sortenlist = []
        if vals.get("sorten_id", False):
            for id, sorten in enumerate(vals.get("sorten_id", [])):
                if sorten[2]["name"] == "" or sorten[2]["name"] == False:
                    vals["sorten_id"][id][2]["name"] = "Default_Code"
        else:
            vals["sorten_id"] = [[0, 0, {"name": "Default_Code"}]]
            print("tesT")

        anzahl = self.env['lisigruen.sorten'].search_count(
            [('name', '=', vals["name"])])
        # wenn nur ein Model mit dem Namen gefunden wird, dann wird ein nues angelegt -> ansonsten wird das bestehnde zurückgegeben.
        if anzahl < 1:
            rec = super().create(vals)
            return rec
        else:
            x = 1
            rec = self.env['lisigruen.sorten'].search(
                [('name', '=', vals["name"])], limit=1)
            rec.write({"name_latein": "Rudi"})
            if vals["name"] == "Skabiosen":
                print("Test")

            sortenlist = []
            if vals.get("sorten_id", True):
                for sorten in vals.get("sorten_id", []):
                    sortendict = sorten[2]
                    sortenlist.append(sortendict)
            #added_sorten = rec.sorten_id
            #new = self.env['lisigruen.crops'].create()

            # rec.write({"sorten_id":rec.sorten_id})
            # create a new Link:
            for new in sortenlist:
                anzahl = self.env['lisigruen.crops'].search_count(
                    [('name', '=', new["name"])])
                # wenn es noch keine Sorte gibt dann erstelle eine
                if anzahl == 0:
                    if new["name"] == "":
                        new["name"] = "Default_Code"
                    rec.write({"sorten_id": [(0, 0, {"name": new["name"]})]})
                # wenn es die sorte schon gibt dann verlinke darauf 4er
                if anzahl == 1:
                    if new["name"] == "":
                        new["name"] = "Default_Code"
                    obj = self.env['lisigruen.crops'].search(
                        [('name', '=', new["name"])], limit=1)
                    rec.write({"sorten_id": [(4, obj.id)]})
            return rec
