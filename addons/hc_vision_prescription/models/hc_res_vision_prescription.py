# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF

class VisionPrescription(models.Model):    
    _name = "hc.res.vision.prescription"    
    _description = "Vision Prescription"        

    name = fields.Char(
        string="Event Name", 
        compute="_compute_name", 
        store="True", 
        help="Text representation of the vision prescription event. Patient Name + Prescriber Name + Date Written.")
    identifier_ids = fields.One2many(
        comodel_name="hc.vision.prescription.identifier", 
        inverse_name="vision_prescription_id", 
        string="Identifiers", 
        help="Business identifier.")
    status_id = fields.Many2one(
        comodel_name="hc.vs.fm.status", 
        string="Status", 
        help="The status of the resource instance.")   
    status_history_ids = fields.One2many(   
        comodel_name="hc.vision.prescription.status.history",
        inverse_name="vision_prescription_id",
        string="Status History",
        help="The status of the vision prescription over time.")
    patient_id = fields.Many2one(
        comodel_name="hc.res.patient", 
        string="Patient", 
        help="Who prescription is for.")  
    encounter_id = fields.Many2one(
        comodel_name="hc.res.encounter", 
        string="Encounter", 
        help="Created during encounter / admission / stay.")  
    date_written = fields.Datetime(
        string="Date Written", 
        help="When prescription was authorized.")                
    prescriber_id = fields.Many2one(
        comodel_name="hc.res.practitioner", 
        string="Prescriber", 
        help="Who authorizes the Vision product.")                
    reason_type = fields.Selection(
        string="Reason Type", 
        selection=[
            ("code", "Code"), 
            ("Condition", "Condition")], 
        help="Type of reason or indication for writing the prescription.")                
    reason_name = fields.Char(
        string="Reason", 
        compute="_compute_reason_name", 
        store="True", 
        help="Reason or indication for writing the prescription.")                
    reason_code_id = fields.Many2one(
        comodel_name="hc.vs.vision.prescription.reason", 
        string="Reason Code", 
        help="Code of reason or indication for writing the prescription.")                
    reason_condition_id = fields.Many2one(
        comodel_name="hc.res.condition", 
        string="Reason Condition", 
        help="Condition reason or indication for writing the prescription.")                
    dispense_ids = fields.One2many(
        comodel_name="hc.vision.prescription.dispense", 
        inverse_name="vision_prescription_id", 
        string="Dispenses", 
        help="Vision supply authorization.")

    @api.model                          
    def create(self, vals):                         
        status_history_obj = self.env['hc.vision.prescription.status.history']                      
        res = super(VisionPrescription, self).create(vals)                      
        if vals and vals.get('status_id'):                      
            status_history_vals = {                 
                'vision_prescription_id': res.id,               
                'status': res.status_id.name,               
                'start_date': datetime.today()              
                }               
            if vals.get('status_id') == 'entered-in-error':                 
                status_history_vals.update({'end_date': datetime.today()})              
            status_history_obj.create(status_history_vals)                  
        return res                      
                                
    @api.multi                          
    def write(self, vals):                          
        status_history_obj = self.env['hc.vision.prescription.status.history']                      
        fm_status_obj = self.env['hc.vs.fm.status']                     
        res = super(VisionPrescription, self).write(vals)                       
        status_history_record_ids = status_history_obj.search([('end_date','=', False)])                        
        if status_history_record_ids:                       
            if vals.get('status_id') and status_history_record_ids[0].status != vals.get('status_id'):                  
                for status_history in status_history_record_ids:                
                    status_history.end_date = datetime.strftime(datetime.today(), DTF)          
                    time_diff = datetime.today() - datetime.strptime(status_history.start_date, DTF)            
                    if time_diff:           
                        days = str(time_diff).split(',')        
                        if days and len(days) > 1:      
                            status_history.time_diff_day = str(days[0]) 
                            times = str(days[1]).split(':') 
                            if times and times > 1: 
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                        else:       
                            times = str(time_diff).split(':')   
                            if times and times > 1: 
                                status_history.time_diff_hour = str(times[0])
                                status_history.time_diff_min = str(times[1])
                                status_history.time_diff_sec = str(times[2])
                fm_status = fm_status_obj.browse(vals.get('status_id'))             
                status_history_vals = {             
                    'vision_prescription_id': self.id,          
                    'status': fm_status.name,           
                    'start_date': datetime.today()          
                    }           
                if vals.get('status_id') == 'entered-in-error':             
                    status_id_history_vals.update({'end_date': datetime.today()})           
                status_history_obj.create(status_history_vals)              
        return res                      
               
class VisionPrescriptionDispense(models.Model):    
    _name = "hc.vision.prescription.dispense"    
    _description = "Vision Prescription Dispense"        

    vision_prescription_id = fields.Many2one(
        comodel_name="hc.res.vision.prescription", 
        string="Vision Prescription", 
        help="Vision prescription associated with this Vision Prescription Dispense.")                
    product_id = fields.Many2one(
        comodel_name="hc.vs.vision.product", 
        string="Product", 
        required="True", 
        help="Identifies the type of vision correction product which is required for the patient.")                
    eye = fields.Selection(
        string="Eye", 
        selection=[
            ("right", "Right"), 
            ("left", "Left")], 
        help="The eye for which the lens applies.")                
    sphere = fields.Float(
        string="Sphere", 
        help="Lens power measured in diopters (0.25 units).")                
    cylinder = fields.Float(
        string="Cylinder", 
        help="Power adjustment for astigmatism measured in diopters (0.25 units).")                
    axis = fields.Integer(
        string="Axis", 
        help="Adjustment for astigmatism measured in integer degrees.")                
    prism = fields.Float(
        string="Prism", 
        help="Amount of prism to compensate for eye alignment in fractional units.")                
    base = fields.Selection(
        string="Base", 
        selection=[
            ("up", "Up"), 
            ("down", "Down"), 
            ("in", "In"), 
            ("out", "Out")], 
        help="The relative base, or reference lens edge, for the prism.")                
    add = fields.Float(
        string="Add", 
        help="Power adjustment for multifocal lenses measured in diopters (0.25 units).")                
    power = fields.Float(
        string="Power", 
        help="Contact lens power measured in diopters (0.25 units).")                
    back_curve = fields.Float(
        string="Back Curve", 
        help="Back curvature measured in millimeters.")                
    diameter = fields.Float(
        string="Diameter", 
        help="Contact lens diameter measured in millimeters.")                
    duration = fields.Float(
        string="Duration", 
        help="The recommended maximum wear period for the lens.")                
    duration_uom_id = fields.Many2one(
        comodel_name="product.uom", 
        string="Duration UOM", 
        help="Lens wear duration unit of measure.")                
    color = fields.Text(
        string="Color", 
        help="Special color or pattern.")                
    brand = fields.Text(
        string="Brand", 
        help="Brand recommendations or restrictions.")                
    note_ids = fields.One2many(
        comodel_name="hc.vision.prescription.dispense.note", 
        inverse_name="dispense_id", 
        string="Notes", 
        help="Notes for coatings.")              

class VisionPrescriptionIdentifier(models.Model):    
    _name = "hc.vision.prescription.identifier"    
    _description = "Vision Prescription Identifier"        
    _inherit = ["hc.basic.association", "hc.identifier"]

    vision_prescription_id = fields.Many2one(
        comodel_name="hc.res.vision.prescription", 
        string="Vision Prescription", 
        help="Vision Prescription associated with this Vision Prescription Identifier.")                

class VisionPrescriptionStatusHistory(models.Model):        
    _name = "hc.vision.prescription.status.history" 
    _description = "Vision Prescription Status History" 
        
    vision_prescription_id = fields.Many2one(   
        comodel_name="hc.res.vision.prescription",
        string="Vision Prescription",
        help="Vision Prescription associated with this Vision Prescription Status History.")
    status = fields.Char(   
        string="Status",
        help="The status of the vision prescription.")
    start_date = fields.Datetime(   
        string="Start Date",
        help="Start of the period during which this vision prescription status is valid.")
    end_date = fields.Datetime( 
        string="End Date",
        help="End of the period during which this vision prescription status is valid.")
    time_diff_day = fields.Char(    
        string="Time Diff (days)",
        help="Days duration of the status.")
    time_diff_hour = fields.Char(   
        string="Time Diff (hours)",
        help="Hours duration of the status.")
    time_diff_min = fields.Char(    
        string="Time Diff (minutes)",
        help="Minutes duration of the status.")
    time_diff_sec = fields.Char(    
        string="Time Diff (seconds)",
        help="Seconds duration of the status.")
    
class VisionPrescriptionDispenseNote(models.Model):
    _name = "hc.vision.prescription.dispense.note"
    _description = "Vision Prescription Dispense Note"
    _inherit = ["hc.basic.association", "hc.annotation"]

    dispense_id = fields.Many2one(
        comodel_name="hc.vision.prescription.dispense", 
        string="Dispense", 
        help="Dispense associated with this Vision Prescription Dispense Note.")
                  
class VisionPrescriptionReason(models.Model):    
    _name = "hc.vs.vision.prescription.reason"    
    _description = "Vision Prescription Reason"        
    _inherit = ["hc.value.set.contains"]

class VisionProduct(models.Model):    
    _name = "hc.vs.vision.product"    
    _description = "Vision Product"        
    _inherit = ["hc.value.set.contains"]
