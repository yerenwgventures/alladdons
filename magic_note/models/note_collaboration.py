# -*- coding: utf-8 -*-
"""
Note Collaboration Model
Adds collaboration features to magic notes
"""

from odoo import api, fields, models, _


class NoteCollaboration(models.Model):
    """Model for note collaboration features"""
    _name = 'note.collaboration'
    _description = 'Note Collaboration'
    _order = 'create_date desc'

    name = fields.Char(string='Collaboration Name', required=True)
    note_id = fields.Many2one('magic.note', string='Note', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    permission = fields.Selection([
        ('read', 'Read Only'),
        ('write', 'Read & Write'),
        ('admin', 'Full Access'),
    ], string='Permission Level', default='read', required=True)
    shared_date = fields.Datetime(string='Shared Date', default=fields.Datetime.now)
    is_active = fields.Boolean(string='Active', default=True)
    last_accessed = fields.Datetime(string='Last Accessed')

    @api.model
    def create(self, vals):
        """Override create to set collaboration name"""
        if not vals.get('name'):
            note = self.env['magic.note'].browse(vals.get('note_id'))
            user = self.env['res.users'].browse(vals.get('user_id'))
            vals['name'] = f"{note.name} - {user.name}"
        return super().create(vals)

    def action_revoke_access(self):
        """Revoke collaboration access"""
        self.write({'is_active': False})

    def action_restore_access(self):
        """Restore collaboration access"""
        self.write({'is_active': True})


class NoteComment(models.Model):
    """Model for note comments"""
    _name = 'note.comment'
    _description = 'Note Comment'
    _order = 'create_date desc'

    note_id = fields.Many2one('magic.note', string='Note', required=True, ondelete='cascade')
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    comment = fields.Text(string='Comment', required=True)
    parent_comment_id = fields.Many2one('note.comment', string='Parent Comment')
    reply_ids = fields.One2many('note.comment', 'parent_comment_id', string='Replies')
    is_resolved = fields.Boolean(string='Resolved', default=False)
    create_date = fields.Datetime(string='Created On', default=fields.Datetime.now)

    def action_resolve(self):
        """Mark comment as resolved"""
        self.write({'is_resolved': True})

    def action_unresolve(self):
        """Mark comment as unresolved"""
        self.write({'is_resolved': False})


class NoteVersion(models.Model):
    """Model for note version history"""
    _name = 'note.version'
    _description = 'Note Version History'
    _order = 'version_number desc'

    note_id = fields.Many2one('magic.note', string='Note', required=True, ondelete='cascade')
    version_number = fields.Integer(string='Version Number', required=True)
    content = fields.Html(string='Content')
    user_id = fields.Many2one('res.users', string='Modified By', required=True)
    change_summary = fields.Text(string='Change Summary')
    create_date = fields.Datetime(string='Created On', default=fields.Datetime.now)

    @api.model
    def create_version(self, note_id, content, change_summary=''):
        """Create a new version of the note"""
        note = self.env['magic.note'].browse(note_id)
        last_version = self.search([('note_id', '=', note_id)], limit=1, order='version_number desc')
        
        version_number = (last_version.version_number + 1) if last_version else 1
        
        return self.create({
            'note_id': note_id,
            'version_number': version_number,
            'content': content,
            'user_id': self.env.user.id,
            'change_summary': change_summary,
        })

    def action_restore_version(self):
        """Restore this version as current"""
        self.note_id.write({'note': self.content})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Version Restored'),
                'message': _('Note has been restored to version %s') % self.version_number,
                'type': 'success',
            }
        }
