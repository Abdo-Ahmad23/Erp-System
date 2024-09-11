from odoo import fields,models

class ToDoTask(models.Model):
    _name='to.do.task'

    task_name=fields.Char(string="Task Name")
    assign_to=fields.Many2one('employee',string="Assign To")
    description=fields.Text(string="Description")
    due_date=fields.Date(string="Due Date")
    state=fields.Selection([
        ('new','New'),
        ('in_progress',"In Progress"),
        ('completed','Completed')
    ])

     def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.state = 'completed'
