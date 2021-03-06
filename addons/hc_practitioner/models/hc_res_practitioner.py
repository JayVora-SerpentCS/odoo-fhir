# -*- coding: utf-8 -*-

from openerp import models, fields, api

class Practitioner(models.Model):
    _name = "hc.res.practitioner"
    _description = "Practitioner"
    _inherits = {"hc.res.person": "person_id"}
    _rec_name = "person_id"

    person_id = fields.Many2one(
        comodel_name="hc.res.person",
        string="Person",
        required="True",
        ondelete="restrict",
        help="Person who is this practitioner.")
    type = fields.Selection(
        string="Type",
        selection=[
            ("human", "Human"),
            ("animal", "Animal")],
        default="human",
        help="Practitioner is human or animal.")
    identifier_ids = fields.One2many(
        related="person_id.identifier_ids",
        string="Identifiers",
        help="A human identifier for this practitioner.")
    # identifier_ids = fields.One2many(
    #     comodel_name="hc.practitioner.identifier",
    #     inverse_name="practitioner_id",
    #     string="Identifiers",
    #     help="A human identifier for this practitioner.")
    is_active = fields.Boolean(
        string="Active Practitioner",
        default="True",
        help="Whether this practitioner's record is in active use.")
    name_ids = fields.One2many(
        related="person_id.name_ids",
        string="Names",
        help="A name associated with this practitioner.")
    # name_ids = fields.One2many(
    #     comodel_name="hc.practitioner.name",
    #     inverse_name="practitioner_id",
    #     string="Names",
    #     help="A name associated with this practitioner.")
    telecom_ids = fields.One2many(
        related="person_id.telecom_ids",
        string="Telecoms",
        help="A contact detail for this practitioner.")
    # telecom_ids = fields.One2many(
    #     comodel_name="hc.practitioner.telecom",
    #     inverse_name="practitioner_id",
    #     string="Telecoms",
    #     help="A contact detail for this practitioner.")
    address_ids = fields.One2many(
        related="person_id.address_ids",
        string="Addresses",
        help="One or more addresses for this practitioner.")
    # address_ids = fields.One2many(
    #     comodel_name="hc.practitioner.address",
    #     inverse_name="practitioner_id",
    #     string="Addresses",
    #     help="One or more addresses for this practitioner.")
    gender = fields.Selection(
        related="person_id.gender",
        readonly=True,
        help="The gender of a practitioner used for administrative purposes.")
    birth_date = fields.Date(
        related="person_id.birth_date",
        readonly=True,
        help="The birth date for the practitioner.")
    photo_ids = fields.One2many(
        related="person_id.photo_ids",
        string="Photos",
        help="Image of the practitioner.")
    # photo_ids = fields.One2many(
    #     comodel_name="hc.practitioner.photo",
    #     inverse_name="practitioner_id",
    #     string="Photos",
    #     help="Image of the Practitioner.")
    communication_ids = fields.One2many(
        comodel_name="hc.practitioner.communication",
        inverse_name="practitioner_id",
        string="Languages",
        help="A language the practitioner is able to use in patient communication.")
    specialty_id = fields.Many2one(
        comodel_name="hc.vs.practitioner.specialty",
        string="Primary Specialty",
        help="Primary specialty of the practitioner.")
    qualification_ids = fields.One2many(
        comodel_name="hc.practitioner.qualification",
        inverse_name="practitioner_id",
        string="Qualifications",
        help="Qualification obtained by training and certification")
    role_ids = fields.One2many( # not in standard
        comodel_name="hc.practitioner.practitioner.role",
        inverse_name="practitioner_id",
        string="Roles",
        help="Roles/organizations the practitioner is associated with.")

    # _defaults = {
    #     "is_practitioner": True,
    #     }

    # Indicate that associated Person is a Practitioner.
    @api.model
    def create(self, vals):
        person_obj = self.env['hc.res.person']
        if vals and vals.get('person_id'):
            person_id = person_obj.browse(vals.get('person_id'))
            if person_id:
                person_id.is_practitioner = True
        return super(Practitioner, self).create(vals)

class PractitionerQualification(models.Model):
    _name = "hc.practitioner.qualification"
    _description = "Practitioner Qualification"

    practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Practitioner",
        help="Practitioner associated with this qualification.")
    identifier_ids = fields.One2many(
        comodel_name="hc.practitioner.qualification.identifier",
        inverse_name="qualification_id",
        string="Identifiers",
        help="An identifier for this qualification for the practitioner.")
    code_id = fields.Many2one(
        comodel_name="hc.vs.practitioner.qualification",
        string="Qualification Code",
        help="Coded representation of the qualification.")
    start_date = fields.Datetime(
        string="Start Date",
        help="Start of the period during which the qualification is valid.")
    end_date = fields.Datetime(
        string="End Date",
        help="End of the period during which the qualification status is valid.")
    issuer_id = fields.Many2one(
        comodel_name="hc.res.organization",
        string="Issuer",
        help="Organization that regulates and issues the qualification.")

class PractitionerQualificationIdentifier(models.Model):
    _name = "hc.practitioner.qualification.identifier"
    _description = "Practitioner Qualification Identifier"
    _inherit = ["hc.basic.association", "hc.identifier"]

    qualification_id = fields.Many2one(
        comodel_name="hc.practitioner.qualification",
        string="Qualification",
        help="Qualification associated with this Practitioner Qualification Identifier.")

class PractitionerPractitionerRole(models.Model):
    _name = "hc.practitioner.practitioner.role"
    _description = "Practitioner Practitioner Role"

    practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Practitioner",
        help="Practitioner associated with this Practitioner Practitioner Role.")
    # role_id = fields.many2one(
    #     comodel_name="hc.res.practitioner.role",
    #     string="Role",
    #     help="Practitioner Role associated with this Practitioner Practitioner Role.")


# class PractitionerIdentifier(models.Model):
#     _name = "hc.practitioner.identifier"
#     _description = "Practitioner Identifier"
#     _inherits = {"hc.person.identifier": "identifier_id"}

#     identifier_id = fields.Many2one(
#         comodel_name="hc.person.identifier",
#         string="Identifier",
#         ondelete="restrict",
#         required="True",
#         help="Person Identifier associated with this Practitioner Identifier.")
#     practitioner_id = fields.Many2one(
#         comodel_name="hc.res.practitioner",
#         string="Practitioner",
#         help="Practitioner associated with this Practitioner Identifier.")

# class PractitionerName(models.Model):
#     _name = "hc.practitioner.name"
#     _description = "Practitioner Name"
#     _inherit = ["hc.human.name.use"]
#     _inherits = {"hc.human.name": "name_id"}

#     name_id = fields.Many2one(
#         comodel_name="hc.human.name",
#         string="Name",
#         ondelete="restrict",
#         required="True",
#         help="Human Name associated with this Practitioner Name.")

#     practitioner_id = fields.Many2one(
#         comodel_name="hc.res.practitioner",
#         string="Practitioner",
#         help="Practitioner associated with this human name.")

# class PractitionerTelecom(models.Model):
#     _name = "hc.practitioner.telecom"
#     _description = "Practitioner Telecom"
#     _inherit = ["hc.contact.point.use"]
#     _inherits = {"hc.contact.point": "telecom_id"}

#     telecom_id = fields.Many2one(
#         comodel_name="hc.contact.point",
#         string="Telecom",
#         ondelete="restrict",
#         required="True",
#         help="Telecom associated with this Practitioner Telecom.")
#     practitioner_id = fields.Many2one(
#         comodel_name="hc.res.practitioner",
#         string="Practitioner",
#         help="Practitioner associated with this Practitioner Telecom.")

# class PractitionerAddress(models.Model):
#     _name = "hc.practitioner.address"
#     _description = "Practitioner Address"
#     _inherit = ["hc.address.use"]
#     _inherits = {"hc.address": "address_id"}

#     address_id = fields.Many2one(
#         comodel_name="hc.address",
#         string="Address",
#         required="True",
#         ondelete="restrict",
#         help="Address associated with this Practitioner Address.")
#     practitioner_id = fields.Many2one(
#         comodel_name="hc.res.practitioner",
#         string="Practitioner",
#         help="Practitioner associated with this Practitioner Address.")

# class PractitionerPhoto(models.Model):
#     _name = "hc.practitioner.photo"
#     _description = "Practitioner Photo"
#     _inherits = {"hc.person.photo": "photo_id"}

#     photo_id = fields.Many2one(
#         comodel_name="hc.person.photo",
#         string="Photo",
#         required="True",
#         ondelete="restrict",
#         help="Photo associated with this Practitioner Photo.")
#     practitioner_id = fields.Many2one(
#         comodel_name="hc.res.practitioner",
#         string="Practitioner",
#         help="Practitioner associated with this Practitioner Photo.")

class PractitionerCommunication(models.Model):
    _name = "hc.practitioner.communication"
    _description = "Practitioner Communication"
    _inherit = ["hc.basic.association"]

    practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Practitioner",
        help="Practitioner associated with this language.")
    language_id = fields.Many2one(
        comodel_name="hc.vs.language",
        string="Language",
        help="A language the practitioner is able to use in patient communication.")
    proficiency_ids = fields.One2many(
        comodel_name="hc.practitioner.language.proficiency",
        inverse_name="communication_id",
        string="Proficiencies",
        help="Proficiency of the practitioner with this language.")

class PractitionerLanguageProficiency(models.Model):
    _name = "hc.practitioner.language.proficiency"
    _description = "Practitioner Language Proficiency"
    _inherit = ["hc.basic.association"]

    communication_id = fields.Many2one(
        comodel_name="hc.practitioner.communication",
        string="Communication",
        help="Communication associated with this Practitioner Language Proficiency.")
    language_proficiency_id = fields.Many2one(
        comodel_name="hc.vs.language.ability.proficiency",
        string="Language Proficiency",
        help="Language Proficiency associated with this Practitioner Language Proficiency.")
    language_skill_id = fields.Many2one(
        comodel_name="hc.vs.language.skill",
        string="Language Skill",
        help="Language Skill associated with this Practitioner Language Proficiency.")

class PractitionerQualification(models.Model):
    _name = "hc.vs.practitioner.qualification"
    _description = "Practitioner Qualification"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this practitioner qualification.")
    code = fields.Char(
        string="Code",
        help="Code of this practitioner qualification.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.practitioner.qualification",
        string="Parent",
        help="Parent concept.")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country (can be ISO 3166 3 letter code).")

class PractitionerSpecialty(models.Model):
    _name = "hc.vs.practitioner.specialty"
    _description = "Practitioner Specialty"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Name",
        help="Name of this practitioner specialty.")
    code = fields.Char(
        string="Code",
        help="Code of this practitioner specialty.")
    contains_id = fields.Many2one(
        comodel_name="hc.vs.practitioner.specialty",
        string="Parent",
        help="Parent concept.")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country (can be ISO 3166 3 letter code).")

# External Reference

class Partner(models.Model):
    _inherit = ["res.partner"]

    is_practitioner = fields.Boolean(
        string="Is a practitioner",
        help="This partner is a health care practitioner.")

class PartnerLink(models.Model):
    _inherit = ["hc.partner.link"]

    link_type = fields.Selection(
        selection_add=[
            ("practitioner", "Practitioner")])
    link_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Link Practitioner",
        help="Practitioner who is the resource to which this actual partner is associated.")

    @api.depends('link_type')
    def _compute_link_name(self):
        for hc_partner_link in self:
            if hc_partner_link.link_type == 'person':
                hc_partner_link.link_name = hc_partner_link.link_person_id.name
            elif hc_partner_link.link_type == 'organization':
                hc_partner_link.link_name = hc_partner_link.link_organization_id.name
            elif hc_partner_link.link_type == 'practitioner':
                hc_partner_link.link_name = hc_partner_link.link_practitioner_id.name

class Person(models.Model):
    _inherit = ["hc.res.person"]

    is_practitioner = fields.Boolean(
        string="Is Practitioner",
        help="This person is a practitioner.")

class PersonLink(models.Model):
    _inherit = ["hc.person.link"]

    target_type = fields.Selection(
        selection_add=[
            ("practitioner", "Practitioner")])
    target_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Target Practitioner",
        help="Practitioner who is the resource to which this actual person is associated.")

    @api.depends('target_type')
    def _compute_target_name(self):
        for hc_person_link in self:
            if hc_person_link.target_type == 'person':
                hc_person_link.target_name = hc_person_link.target_person_id.name
            elif hc_person_link.target_type == 'practitioner':
                hc_person_link.target_name = hc_person_link.target_practitioner_id.name

class Annotation(models.Model):
    _inherit = ["hc.annotation"]

    author_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Author Practitioner",
        help="Practitioner responsible for the annotation.")

    @api.depends('author_type')
    def _compute_author_name(self):
        for hc_annotation in self:
            if hc_annotation.author_type == 'string':
                hc_annotation.author_name = hc_annotation.author_string
            elif hc_annotation.author_type == 'practitioner':
                hc_annotation.author_name = hc_annotation.author_practitioner_id.name

class Signature(models.Model):
    _inherit = ["hc.signature"]

    who_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="Who Practitioner",
        help="Practitioner who signed.")
    on_behalf_of_practitioner_id = fields.Many2one(
        comodel_name="hc.res.practitioner",
        string="On Behalf Of Practitioner",
        help="Practitioner the party represented.")

    @api.depends('who_type')
    def _compute_who_name(self):
        for hc_signature in self:
            if hc_signature.who_type == 'uri':
                hc_signature.who_name = hc_signature.who_uri
            elif hc_signature.who_type == 'practitioner':
                hc_signature.who_name = hc_signature.who_practitioner_id.name

    @api.depends('on_behalf_of_type')
    def _compute_on_behalf_of_name(self):
        for hc_signature in self:
            if hc_signature.on_behalf_of_type == 'uri':
                hc_signature.on_behalf_of_name = hc_signature.on_behalf_of_uri
            elif hc_signature.on_behalf_of_type == 'practitioner':
                hc_signature.on_behalf_of_name = hc_signature.on_behalf_of_practitioner_id.name
