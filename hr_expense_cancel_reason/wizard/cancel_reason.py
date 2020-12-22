# -*- coding: utf-8 -*-

from openerp import models, fields, api

# from account_move_line 
class HRExpenseCancel(models.TransientModel):

    """ Ask a reason for the hr expense cancellation."""
    _name = 'hr.expense.cancel'
    _description = __doc__
    
    cancel_reason_txt = fields.Char(
        string="Reason",
    )


    @api.one
    def confirm_cancel(self):
        act_close = {'type': 'ir.actions.act_window_close'}
        expense_ids = self._context.get('active_ids')
        if expense_ids is None:
            return act_close
        assert len(expense_ids) == 1, "Only 1 Expense ID expected"
        expense = self.env['hr.expense.expense'].browse(expense_ids)
        expense.cancel_reason_txt = self.cancel_reason_txt
        expense.signal_workflow('refuse')
        return act_close

    # def error_cancel(self, cr, uid, ids, context=None):
    # for line in self.browse(cr, uid, ids, context=context):
    #     if line.invoiced:
    #         raise osv.except_osv(_('Invalid Action!'), _('Test.'))
    # return self.write(cr, uid, ids, {'state': 'draft'})



    # def confirm_cancel(self, cr, uid, journal_id, period_id, context=None):
    #     journal_obj = self.pool.get('account.journal')
    #     period_obj = self.pool.get('account.period')
    #     jour_period_obj = self.pool.get('account.journal.period')
    #     cr.execute('SELECT state FROM account_journal_period WHERE journal_id = %s AND period_id = %s', (journal_id, period_id))
    #     result = cr.fetchall()
    #     journal = journal_obj.browse(cr, uid, journal_id, context=context)
    #     period = period_obj.browse(cr, uid, period_id, context=context)
    #     for (state,) in result:
    #         if state == 'done':
    #             raise osv.except_osv(_('Error!'), _('You can not add/modify entries in a closed period %s of journal %s.') % (period.name, journal.name))
    #     if not result:
    #         jour_period_obj.create(cr, uid, {
    #             'name': (journal.code or journal.name)+':'+(period.name or ''),
    #             'journal_id': journal.id,
    #             'period_id': period.id
    #         })
    #     return True