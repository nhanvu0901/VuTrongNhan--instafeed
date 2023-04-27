import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime
import traceback


class Comment(models.Model):
    _name = 'media.comment'
    _description = "Instagram Media's Comments"

    comment_id = fields.Char(string="Comment ID")
    comment_text = fields.Char(string="Text")
    comment_timestamp = fields.Char(string="Timestamp")
    comment_username = fields.Char(string="Comment Username")
    media = fields.Many2one('media.data', string="Media",ondelete='cascade')


    def get_comment(self):
        data={
            "comment_id":self.comment_id,
            "comment_text": self.comment_text,
            "comment_timestamp": self.comment_timestamp,
            "comment_username": self.comment_username,
        }
        return data


