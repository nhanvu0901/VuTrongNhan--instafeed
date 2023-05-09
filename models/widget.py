import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime
import datetime as convertDate
import sys

class Widget(models.Model):
    _name = 'widget.data'
    _description = 'Widget Media'


    # instagram_user = fields.Many2one('instagram.user', string='Instagram Data', ondelete='cascade')
    widget_config = fields.Many2one('widget.config')
    hashed_id = fields.Char(index=True)
    media_data = fields.Many2many('media.data', ondelete='cascade')
    # id_widget = fields.Char(string="Widget ID")
    is_display = fields.Boolean(string="Is Displayed")

    admin = fields.Many2one('res.users')


    def create_action(self):
        list_media_id = request.env['media.data'].get_list_media_id()
        # widget_id = convertDate.datetime.now().strftime('%Y%m%d%H%M%S%f')
        widget_exist = self.sudo().create({
            # "instagram_user": instagram_user_exist.id,
            "is_display": True,
            "media_data": list_media_id,
            "admin":request.env.user.id
            # "id_widget":widget_id
        })
        hashed_value = hash(widget_exist)
        hashed_value += sys.maxsize + 1
        setting = self.env['widget.config'].sudo().create({
            "admin":request.env.user.id
        })
        widget_exist.sudo().write({
            'hashed_id': str(hashed_value),

            'widget_config': setting.id,
        })
        return widget_exist
    def get_widgets(self):
        media_data = self.media_data.get_list_media()
        choose_widget = {
            "hashed_id": self.hashed_id,
            "number": self.id
        }
        widget_config = self.widget_config
        list_widget = self.get_list_widget()

        data = {
            "media_data":media_data,
            "choose_widget": choose_widget,
            "is_display": self.is_display,
            "title": widget_config.feed_title,
            "spacing": widget_config.spacing,
            "onclickPost": widget_config.on_post_click,
            "layout": widget_config.layout,
            "autoLayout": widget_config.configuration,
            "rows": widget_config.rows,
            "columns": widget_config.columns,
            "showLikes": widget_config.showLikes,
            "showFollwers": widget_config.showFollwers,
            "postToShow": widget_config.postToShow,
            "displayTagPost": widget_config.displayTagPost,
            "list_widget": list_widget,


        }
        return data


    # TODO hàm wiget chọn thằng để hiển thị
    def set_active_widget(self):
        # tim thang dang active
        current_user = request.env.user.id
        widget_exist = request.env['widget.data'].sudo().search(
            ['&', ('admin', '=', current_user),
             ('is_display', '=', True)])
        widget_exist.write({
            'is_display': False
        })
        self.write({
            'is_display': True
        })
        data = self.get_widgets()
        return data


    def get_active_widget(self):#TODO set media cho widget o day
        current_user = request.env.user.id
        widget_exist = request.env['widget.data'].sudo().search(
            [ ('admin', '=', current_user)])
        if not widget_exist:

            # widget_exist=  self.create_action()
            return ''
        else:
            if len(widget_exist) > 1:
                widget_exist = request.env['widget.data'].sudo().search(
                    ['&', ('admin', '=',current_user),
                     ('is_display', '=', True)])  # TODO tim thang widget dang hoat dong
        return widget_exist

    def get_list_widget(self):
        current_user = request.env.user.id
        widget_exist = request.env['widget.data'].sudo().search(
            [('admin', '=',current_user)])
        list_widget = []
        if len(widget_exist) > 0:
            for widget in widget_exist:
                data = {
                    "hashed_id": widget.hashed_id,
                    "number": widget.id
                }
                list_widget.append(data)
            return list_widget

        else:
            return None

class WidgetConfig(models.Model):
    _name = 'widget.config'

    widget = fields.Many2one('widget.data', ondelete='cascade')
    admin = fields.Many2one('res.users')

    feed_title = fields.Char(string="Feed Title", default="Leave empty if you don't want a title")
    spacing = fields.Char(string="spacing", default="0")
    on_post_click = fields.Char(string="on post click", default='Open popup / show product')
    layout = fields.Char(string="layout", default='Grid - Squares')
    configuration = fields.Char(string="configuration", default='Auto')
    rows = fields.Char(string="rows", default="0")
    columns = fields.Char(string="columns", default="0")
    showLikes = fields.Char(string="Show Likes", default="No")
    showFollwers = fields.Char(string="Show Followers", default="No")
    postToShow = fields.Char(string="Post to show", default="All")
    displayTagPost = fields.Char(string="Display Tag Post", default="Off")

