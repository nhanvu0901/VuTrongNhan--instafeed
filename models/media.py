import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime
import traceback

class Media(models.Model):
    _name = 'media.source'
    _description = 'Instagram Media'


    name =fields.Char()


    admin = fields.Many2one('res.users')

    selected_posts_global = fields.Many2many('post.private')

    #TODO xoa instagram_user va widget_data
    # widget_data = fields.Many2many('widget.data')
    # instagram_user = fields.Many2one('instagram.user', "User", ondelete='cascade')





    def get_list_media_id(self):
        current_user = request.env.user.id
        widget_exist = request.env['widget.data'].sudo().search(
            ['&', ('admin', '=', current_user),
             ('is_display', '=', True)])
        try:
            if widget_exist.media_data:
                list_widget = []
                list_widget_id = []
                for item in widget_exist.media_data:
                    list_widget.append(item.id)
                for i in list_widget:
                    product = (4, i)  # link to an existing record
                    list_widget_id.append(product)
                return list_widget_id
        except Exception as err:
            print(err)
            traceback.print_exc()

    def get_list_media(self):
        current_user = request.env.user.id
        widget_exist = request.env['widget.data'].sudo().search(
            ['&', ('admin', '=', current_user),
             ('is_display', '=', True)])
        if widget_exist.media_data:
            list_media = []

            for media_url in widget_exist.media_data.selected_posts_global:
                list_comment = []
                for comment in media_url.comment:
                    comment_data = {
                        "comment_id": comment.comment_id,
                        "comment_text": comment.comment_text,
                        "comment_timestamp": comment.comment_timestamp,
                        "comment_username": comment.comment_username,
                    }
                    list_comment.append(comment_data)

                list_product = []
                for product in media_url.hotspot:
                    product_data = {
                        "id": product.product_id,
                        "image_src": product.product_img,
                        "name": product.product_name,
                    }
                    list_product.append(product_data)
                media_data = {
                    "media_id": media_url.media_id,
                    "media_url": media_url.media_url,
                    "type": media_url.type,
                    "caption": media_url.caption,
                    "permalink": media_url.permalink,
                    "thumbnail_url": media_url.thumbnail_url,
                    "created_date": media_url.created_date,
                    "selected_product": list_product,
                    "media_like": media_url.media_like,
                    "media_count": media_url.count_comment,
                    "num_of_tagged_product": len(media_url.hotspot),
                    "list_comment": list_comment,

                }
                list_media.append(media_data)

            return list_media

    def get_post_product_tag(self):

        product_list = []
        if self.selected_posts_global:
            for item in self.selected_posts_global.hotspot:
                product = {
                    "id": item.product_id,
                    "image_src": item.product_img,
                    "name": item.product_name
                }
                product_list.append(product)


class NestWidgetPostGlobal(models.Model):
    _name = 'post.private'
    media_id = fields.Char(string="ID")
    media_url = fields.Char(string="media url")
    type = fields.Char(string="media type")
    caption = fields.Char(string="caption")
    permalink = fields.Char(string="permalink")
    thumbnail_url = fields.Char(string="thumbnail url")
    created_date = fields.Char(string="Created at")
    hotspot = fields.One2many('hotspot.private', 'post')
    instagram_user = fields.Many2one('instagram.user')
    media_like = fields.Char('Likes')
    count_comment = fields.Char('')
    comment = fields.One2many("media.comment", "media", string="Comment")
    admin = fields.Many2one('res.users')

    def get_list_product(self):
        list_product=[]
        for item in self.hotspot:
            list_product.append(item.get_product())
        return list_product

    def get_list_comment(self):
        list_comment = []
        for item in self.comment:
            list_comment.append(item.get_comment())
        return list_comment