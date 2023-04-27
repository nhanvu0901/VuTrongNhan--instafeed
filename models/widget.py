import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime
import datetime as convertDate


class Media(models.Model):
    _name = 'widget.data'
    _description = 'Widget Media'

    feed_title = fields.Char(string="Feed Title", default="Leave empty if you don't want a title")
    spacing = fields.Char(string="spacing", default="0")
    on_post_click = fields.Char(string="on post click", default='Open popup / show product')
    layout = fields.Char(string="layout", default='Grid - Squares')
    configuration = fields.Char(string="configuration", default='Auto')
    rows = fields.Char(string="rows", default="0")
    columns = fields.Char(string="columns", default="0")
    showLikes = fields.Char(string="Show Likes", default="No")
    showFollwers = fields.Char(string="Show Followers", default="No")
    media_data = fields.Many2many('media.data', ondelete='cascade')
    instagram_user = fields.Many2one('instagram.user', string='Instagram Data', ondelete='cascade')
    shopify_shop = fields.Many2one('shopify.mint', string="Shop")
    postToShow = fields.Char(string="Post to show", default="All")
    displayTagPost = fields.Char(string="Display Tag Post", default="Off")
    id_widget = fields.Char(string="Widget ID")
    is_display = fields.Boolean(string="Is Displayed")

    def get_widget_field(self):
        media_data = self.media_data.get_list_media(self.instagram_user)
        choose_widget = {
            "id_widget": self.id_widget,
            "number": self.id
        }
        list_widget = self.get_list_widget(self.instagram_user, self.shopify_shop)
        data = {
            # "media_data":media_data,
            "choose_widget": choose_widget,
            "is_display": self.is_display,
            "title": self.feed_title,
            "spacing": self.spacing,
            "onclickPost": self.on_post_click,
            "layout": self.layout,
            "autoLayout": self.configuration,
            "rows": self.rows,
            "columns": self.columns,
            "showLikes": self.showLikes,
            "showFollwers": self.showFollwers,
            "postToShow": self.postToShow,
            "displayTagPost": self.displayTagPost,
            "list_widget": list_widget,
            "followers":self.instagram_user.followers

        }
        return data

    # TODO hàm wiget chọn thằng để hiển thị
    def set_active_widget(self, instagram, shop):
        # tim thang dang active
        widget_exist = request.env['widget.data'].sudo().search(
            ['&', ('instagram_user.id', '=', instagram.id),
             ('shopify_shop.id', '=', shop.id),
             ('is_display', '=', True)])
        widget_exist.write({
            'is_display': False
        })
        self.write({
            'is_display': True
        })
        data = self.get_widget_field()
        return data


    def get_active_widget(self, instagram, shop):#TODO set media cho widget o day
        widget_exist = request.env['widget.data'].sudo().search(
            ['&', ('instagram_user.id', '=', instagram.id),
             ('shopify_shop.id', '=', shop.id)])
        if not widget_exist:
            widget_id = convertDate.datetime.now().strftime('%Y%m%d%H%M%S%f')
            list_widget_id = request.env['media.data'].get_list_media_id(instagram)
            widget_exist = request.env['widget.data'].sudo().create({
                "instagram_user": instagram.id,
                "id_widget": widget_id,
                "shopify_shop": shop.id,
                "is_display": True,
                "media_data": list_widget_id,
            })
        else:
            if len(widget_exist) > 1:
                widget_exist = request.env['widget.data'].sudo().search(
                    ['&', ('instagram_user.id', '=', instagram.id),
                     ('shopify_shop.id', '=', shop.id),
                     ('is_display', '=', True)])  # TODO tim thang widget dang hoat dong
        return widget_exist

    def get_list_widget(self, instagram, shop):
        widget_exist = request.env['widget.data'].sudo().search(
            ['&', ('instagram_user.id', '=', instagram.id),
             ('shopify_shop.id', '=', shop.id)])
        list_widget = []
        if len(widget_exist) > 0:
            for widget in widget_exist:
                data = {
                    "id_widget": widget.id_widget,
                    "number": widget.id
                }
                list_widget.append(data)
            return list_widget

        else:
            return None
