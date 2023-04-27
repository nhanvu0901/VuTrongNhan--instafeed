import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime
import traceback

class Media(models.Model):
    _name = 'media.data'
    _description = 'Instagram Media'

    media_id = fields.Char(string="ID")
    instagram_user = fields.Many2one('instagram.user', "User", ondelete='cascade')
    media_url = fields.Char(string="media url")
    type = fields.Char(string="media type")
    caption = fields.Char(string="caption")
    permalink = fields.Char(string="permalink")
    thumbnail_url = fields.Char(string="thumbnail url")
    created_date = fields.Char(string="Created at")
    selected_product = fields.Many2many('product.data', string="Selected Product")
    widget_data = fields.Many2many('widget.data')
    media_like = fields.Char('Likes')
    count_comment = fields.Char('')
    comment = fields.One2many("media.comment","media",string="Comment")

    def get_list_comment(self):
        list_comment=[]
        for item in self.comment:
            list_comment.append(item.get_comment())
        return list_comment
    def get_list_product(self):
        list_product=[]
        for item in self.selected_product:
            list_product.append(item.get_product())
        return list_product


    def get_list_media_id(self, instagram_user):
        media_data = self.env['media.data'].sudo().search([('instagram_user.id', '=', instagram_user.id)])
        try:
            if media_data:
                list_widget = []
                list_widget_id = []
                for item in media_data:
                    list_widget.append(item.id)
                for i in list_widget:
                    product = (4, i)  # link to an existing record
                    list_widget_id.append(product)
                return list_widget_id
        except Exception as err:
            print(err)
            traceback.print_exc()

    def get_list_media(self, instagram_user):
        media = self.env['media.data'].sudo().search(
            [('instagram_user.id', '=', instagram_user.id)])
        if media:
            list_media = []
            for media_url in media:
                list_comment =[]
                for comment in media_url.comment:
                    comment_data={
                        "comment_id": comment.comment_id,
                        "comment_text": comment.comment_text,
                        "comment_timestamp": comment.comment_timestamp,
                        "comment_username": comment.comment_username,
                    }
                    list_comment.append(comment_data)


                list_product = []
                for product in media_url.selected_product:
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
                    "num_of_tagged_product": len(media_url.selected_product),
                    "list_comment":list_comment,

                }
                list_media.append(media_data)
            return list_media