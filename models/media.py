import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime
import traceback
import json
from ..static.instagram_auth.InstagramAPI import InstagramAPI
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

                list_product = media_url.get_list_tag_product()


                media_data = {
                    "media_id": media_url.post_id,
                    "media_url": media_url.media_url,
                    "type": media_url.type,
                    "caption": media_url.caption,
                    "permalink": media_url.insta_profile_link,
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




class NestWidgetPostGlobal(models.Model):
    _name = 'post.private'
    post_id = fields.Char(string="ID")
    media_url = fields.Char(string="media url")
    type = fields.Char(string="media type")
    caption = fields.Char(string="caption")
    insta_profile_link = fields.Char(string="insta profile link")
    thumbnail_url = fields.Char(string="thumbnail url")
    created_date = fields.Char(string="Created at")
    hotspot = fields.One2many('hotspot.private', 'post')
    instagram_user = fields.Many2one('instagram.user')
    media_like = fields.Char('Likes')
    count_comment = fields.Char('')
    comment = fields.One2many("media.comment", "media", string="Comment")
    admin = fields.Many2one('res.users')






    def save_post(self, media_exist, response_url):
        current_user = request.env.user.id
        instagram = InstagramAPI(request)

        instagram_user_exist = request.env['instagram.user'].sudo().search([
            ('user_name', '=', json.loads(response_url.text).get("username"))
        ], limit=1)
        if media_exist:
            media_exist.write({
                "post_id": json.loads(response_url.text).get('id'),
                "type": json.loads(response_url.text).get('media_type'),
                "caption": json.loads(response_url.text).get('caption'),
                "insta_profile_link": json.loads(response_url.text).get('permalink'),
                "admin": instagram_user_exist.admin,
                "instagram_user":instagram_user_exist.id,
                "created_date": json.loads(response_url.text).get('timestamp'),
                "media_like": ''
            })
            if json.loads(response_url.text).get('media_type') == 'CAROUSEL_ALBUM':

                # call the children
                data_child_image = instagram.get_child_media_details(json.loads(response_url.text).get(
                        'id'),instagram_user_exist.ins_access_token)
                child_url = data_child_image.get('child_url')
                child_thumbnail_url =data_child_image.get('child_thumbnail_url')

                media_exist.write({
                    "media_url": child_url,
                    "thumbnail_url": child_thumbnail_url if len(child_thumbnail_url) != 0  else '',
                })
            else:
                media_exist.write({
                    "media_url": json.loads(response_url.text).get('media_url'),
                    "thumbnail_url": json.loads(response_url.text).get('thumbnail_url'),
                })

        else:
            media_exist = request.env['post.private'].create({
                "post_id": json.loads(response_url.text).get('id'),
                "type": json.loads(response_url.text).get('media_type'),
                "caption": json.loads(response_url.text).get('caption'),
                "insta_profile_link": json.loads(response_url.text).get('permalink'),
                "admin": instagram_user_exist.admin,
                "instagram_user":instagram_user_exist.id,
                "created_date": json.loads(response_url.text).get('timestamp'),
                "media_like": '',
            })
            if json.loads(response_url.text).get('media_type') == 'CAROUSEL_ALBUM':
                data_child_image = instagram.get_child_media_details(json.loads(response_url.text).get(
                    'id'),instagram_user_exist.ins_access_token)
                child_url = data_child_image.get('child_url')
                child_thumbnail_url = data_child_image.get('child_thumbnail_url')

                media_exist.write({
                    "media_url": child_url,
                    "thumbnail_url": child_thumbnail_url if len(child_thumbnail_url) != 0 else '',
                })

            else:
                media_exist.write({
                    "media_url": json.loads(response_url.text).get('media_url'),
                    "thumbnail_url": json.loads(response_url.text).get('thumbnail_url'),
                })



    def get_list_tag_product(self):
        list_product=[]
        for item in self.hotspot:
            if item.status == True:
                list_product.append(item.get_product())
        return list_product

    def get_list_comment(self):
        list_comment = []
        for item in self.comment:
            list_comment.append(item.get_comment())
        return list_comment