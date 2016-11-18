# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ActivityDefinition(models.Model):    
    _name = "hc.res.activity.definition"    
    _description = "Activity Definition"            

    url = fields.Char(string="URL", help="Logical URL to reference this asset.")                    
    identifier_ids = fields.One2many(
        comodel_name="hc.activity.definition.identifier", 
        inverse_name="activity_definition_id", 
        string="Identifiers", 
        help="Logical identifier(s) for the asset.")                    
    version = fields.Char(
        string="Version", 
        help="The version of the asset, if any.")                    
    name = fields.Char(
        string="Name", 
        help="A machine-friendly name for the asset.")                    
    title = fields.Char(
        string="Title", 
        help="A user-friendly title for the asset.")                    
    status = fields.Selection(
        string="Status", 
        required="True", 
        selection=[
            ("draft", "Draft"), 
            ("active", "Active"), 
            ("inactive", "Inactive")], 
        help="The status of this activity definition. Enables tracking the life-cycle of the content.")                    
    is_experimental = fields.Boolean(
        string="Experimental", 
        help="If for testing purposes, not real usage.")                    
    description = fields.Char(
        string="Description", 
        help="Natural language description of the activity definition.")                    
    purpose = fields.Char(
        string="Purpose", 
        help="Why this activity definition is defined.")                    
    usage = fields.Char(
        string="Usage", 
        help="Describes the clinical usage of the asset.")                    
    approval_date = fields.Date(
        string="Approval Date", 
        help="When activity definition approved by publisher.")                    
    last_review_date = fields.Date(
        string="Last Review Date", 
        help="Last review date for the activity definition.")                    
    effective_period_start_date = fields.Datetime(
        string="Effective Period Start Date", 
        help="Start of the the effective date range for the asset.")                    
    effective_period_end_date = fields.Datetime(
        string="Effective Period End Date", 
        help="End of the the effective date range for the asset.")                    
    use_context_ids = fields.One2many(
        comodel_name="hc.activity.definition.use.context", 
        inverse_name="activity_definition_id", 
        string="Use Contexts", 
        help="Content intends to support these contexts.")                    
    jurisdiction_ids = fields.Many2many(
        comodel_name="hc.vs.jurisdiction", 
        string="Jurisdictions", 
        help="Intended jurisdiction for activity definition (if applicable).")                    
    topic_ids = fields.Many2many(
        comodel_name="hc.vs.activity.definition.topic", 
        string="Topics", 
        help="Descriptional topics for the asset.")                    
    contributor_ids = fields.One2many(
        comodel_name="hc.activity.definition.contributor", 
        inverse_name="activity_definition_id", 
        string="Contributors", 
        help="A content contributor.")                    
    publisher = fields.Char(
        string="Publisher", 
        help="Name of the publisher (Organization or individual).")                    
    contact_ids = fields.One2many(
        comodel_name="hc.activity.definition.contact", 
        inverse_name="activity_definition_id", 
        string="Contacts", 
        help="Contact details of the publisher.")                    
    copyright = fields.Char(
        string="Copyright", 
        help="Use and/or publishing restrictions.")                    
    related_artifact_ids = fields.One2many(
        comodel_name="hc.activity.definition.related.artifact", 
        inverse_name="activity_definition_id", 
        string="Related Artifacts", 
        help="Related artifacts for the asset.")
    # library_ids = fields.One2many(
    #     comodel_name="hc.activity.definition.library", 
    #     string="Libraries", 
    #     help="Logic used by the asset.")                    
    category = fields.Selection(
        string="Category",
        selection=[
            ("communication", "Communication"), 
            ("device", "Device"),
            ("diagnostic", "Diagnostic"),
            ("diet", "Diet"),
            ("drug", "Drug"),
            ("encounter", "Encounter"),
            ("immunization", "Immunization"),
            ("observation", "Observation"),
            ("procedure", "Procedure"),
            ("referral", "Referral"),
            ("supply", "Supply"),
            ("vision", "Vision"),
            ("other", "Other")],  
        help="High-level categorization of the type of activity.")                    
    code_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.code", 
        string="Code", help="Detail type of activity.")                    
    timing_type = fields.Selection(
        string="Timing Type", 
        selection=[
            ("code", "Code"), 
            ("Timing", "Timing")], 
        help="Type of when activity is to occur.")
    timing_name = fields.Char(
        string="Timing", 
        compute="_compute_timing_name", 
        store="True", 
        help="When activity is to occur.")
    timing_code_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.timing", 
        string="Timing Code", 
        help="Code of when activity is to occur.")
    timing_id = fields.Many2one(
        comodel_name="hc.activity.definition.timing",  
        string="Timing",
        help="Timing when activity is to occur.")                 
    location_id = fields.Many2one(
        comodel_name="hc.res.location", 
        string="Location", 
        help="Where it should happen.")                    
    participant_type = fields.Many2many(
        comodel_name="hc.vs.action.participant.type", 
        string="Participant Types", 
        help="The type of participant in the action.")                    
    product_type = fields.Selection(
        string="Product Type", 
        selection=[
            ("Medication", "Medication"), 
            ("Substance", "Substance"), 
            ("code", "Code")], 
        help="Type of what's administered/supplied.")
    product_name = fields.Char(
        string="Product", 
        compute="_compute_product_name", 
        store="True", 
        help="What's administered/supplied.")
    product_medication_id = fields.Many2one(
        string="Product Medication",
        comodel_name="hc.res.medication", 
        help="Medication administered/supplied.")
    product_substance_id = fields.Many2one(
        comodel_name="hc.res.substance", 
        string="Product Substance", 
        help="Substance administered/supplied.")
    product_code_id = fields.Many2one(
        comodel_name="hc.vs.activity.definition.product", 
        string="Product Code", 
        help="Code of what's administered/supplied.")
    quantity = fields.Float(
        string="Quantity", 
        help="How much is administered/consumed/supplied")                    
    quantity_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Quantity UOM", 
        help="Quantity unit of measure.")                    
    dosage_instruction_ids = fields.One2many(
        comodel_name="hc.activity.definition.dosage.instruction", 
        inverse_name="activity_definition_id", 
        string="Dosage Instructions", 
        help="Detailed dosage instructions.")                    
    # transform_id = fields.Many2one(
    #     comodel_name="hc.res.structure.map", 
    #     string="Transform", 
    #     help="Transform to apply the template.")
    dynamic_value_ids = fields.One2many(
        comodel_name="hc.activity.definition.dynamic.value", 
        inverse_name="activity_definition_id", 
        string="Dynamic Value", 
        help="Dynamic aspects of the definition.")
                    
class ActivityDefinitionDynamicValue(models.Model):    
    _name = "hc.activity.definition.dynamic.value"    
    _description = "Activity Definition Dynamic Value"            

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition", 
        string="Activity Definition", 
        help="Activity Definition associated with this Activity Definition Dynamic Value.")
    description = fields.Char(
        string="Description", 
        help="Natural language description of the dynamic value.")                    
    path = fields.Char(
        string="Path", 
        help="The path to the element to be set dynamically.")                    
    language = fields.Char(
        string="Language", 
        help="Language of the expression.")                    
    expression = fields.Char(
        string="Expression", 
        help="An expression that provides the dynamic value for the customization.")                    

class ActivityDefinitionIdentifier(models.Model):
    _name = "hc.activity.definition.identifier" 
    _description = "Activity Definition Identifier"    
    _inherit = ["hc.basic.association", "hc.identifier"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition", 
        string="Activity Definition", 
        help="Activity Definition associated with this Activity Definition Identifier.")

class ActivityDefinitionUseContext(models.Model):   
    _name = "hc.activity.definition.use.context"    
    _description = "Activity Definition Use Context"        
    _inherit = ["hc.basic.association", "hc.usage.context"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition", 
        string="Activity Definition", 
        help="Activity Definition associated with this Activity Definition Use Context.")             

class ActivityDefinitionContact(models.Model):  
    _name = "hc.activity.definition.contact"    
    _description = "Activity Definition Contact"        
    _inherit = ["hc.basic.association", "hc.contact.detail"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition", 
        string="Activity Definition", 
        help="Activity Definition associated with this Activity Definition Contact.")             

class ActivityDefinitionContributor(models.Model):  
    _name = "hc.activity.definition.contributor"    
    _description = "Activity Definition Contributor"        
    _inherit = ["hc.basic.association", "hc.contributor"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition", 
        string="Activity Definition", 
        help="Activity Definition associated with this Activity Definition Contributor.")             

class ActivityDefinitionDosageInstruction(models.Model):    
    _name = "hc.activity.definition.dosage.instruction" 
    _description = "Activity Definition Dosage Instruction"     
    _inherit = ["hc.basic.association", "hc.dosage.instruction"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition", 
        string="Activity Definition", 
        help="Activity Definition associated with this Activity Definition Dosage Instruction.")              

# class ActivityDefinitionLibrary(models.Model):  
#     _name = "hc.activity.definition.library"    
#     _description = "Activity Definition Library"        
#     _inherit = ["hc.basic.association"]

#     activity_definition_id = fields.Many2one(
#         comodel_name="hc.res.activity.definition", 
#         string="Activity Definition", 
#         help="Activity Definition associated with this Activity Definition Library.")             
#     library_id = fields.Many2one(
#         comodel_name="hc.res.library", 
#         string="Library", 
#         help="Logic used by the asset.")             

class ActivityDefinitionRelatedArtifact(models.Model):  
    _name = "hc.activity.definition.related.artifact"   
    _description = "Activity Definition Related Artifact"       
    _inherit = ["hc.basic.association", "hc.related.artifact"]

    activity_definition_id = fields.Many2one(
        comodel_name="hc.res.activity.definition", 
        string="Activity Definition", 
        help="Activity Definition associated with this Activity Definition Related Artifact.")                

class ActivityDefinitionTiming(models.Model):   
    _name = "hc.activity.definition.timing" 
    _description = "Activity Definition Timing"     
    _inherit = ["hc.basic.association", "hc.timing"]

class ActionParticipantType(models.Model):  
    _name = "hc.vs.action.participant.type" 
    _description = "Action Participant Type"        
    _inherit = ["hc.value.set.contains"]

class ActivityDefinitionCode(models.Model): 
    _name = "hc.vs.activity.definition.code"    
    _description = "Activity Definition Code"       
    _inherit = ["hc.value.set.contains"]

class ActivityDefinitionProduct(models.Model):  
    _name = "hc.vs.activity.definition.product" 
    _description = "Activity Definition Product"        
    _inherit = ["hc.value.set.contains"]

class ActivityDefinitionTiming(models.Model):   
    _name = "hc.vs.activity.definition.timing"  
    _description = "Activity Definition Timing"     
    _inherit = ["hc.value.set.contains"]

class ActivityDefinitionTopic(models.Model):    
    _name = "hc.vs.activity.definition.topic"   
    _description = "Activity Definition Topic"      
    _inherit = ["hc.value.set.contains"]