import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime
import json
class SUser(models.Model):
    _inherit = 'res.users'
    sp_shop_id = fields.Char(string="Shop ID")
class SApp(models.Model):
    _name = 'shopify.mint'
    _description = 'Shopify App'
    _rec_name = "shop_url"

    shop_url = fields.Char(index=True)

    sp_access_token = fields.Char()
    # cdn_tag = fields.Char()

    currency = fields.Char(string="Currency")
    email = fields.Char(string="Email")
    shop_name = fields.Char(string="Shop name")
    shop_id = fields.Char(string="Shop ID")
    user = fields.Many2one('res.users', "User")
    widget = fields.One2many('widget.data','shopify_shop')
    script_tag = fields.Char(string='Script Tag')
    is_update_script_tag = fields.Boolean(default=True)
    instagram_data = fields.Many2one('instagram.user',string='Instagram Data')
    is_delete = fields.Boolean(default=False)


    @api.model
    def initShopifySession(self,shop):


        api_version = self.env['ir.config_parameter'].sudo().get_param('shopify_mint.api_version_shopify_mint')


        new_session = shopify.Session(self.shop_url, api_version, token=self.sp_access_token)
        shopify.ShopifyResource.activate_session(new_session)
        return new_session



    # def auto_update_script_tag(self):
    #     shop_scrip_tag_false =  self.search([('is_update_script_tag', '=', False)], limit=30)
    #     for shop in shop_scrip_tag_false:
    #         if shop:
    #
    #             shop.update_script_tag(shop)
    # def update_script_tag(self,shop):
    #     # Todo: Đưa phần này sang model shopify.api
    #
    #     self.initShopifySession(shop)
    #     scripTag = shopify.ScriptTag.find()
    #     for script in scripTag:
    #         if self.script_tag:
    #             if self.script_tag.split('/')[len(self.script_tag.split('/'))-1] in script.src:
    #                 script.destroy()
    #     if self.script_tag:
    #         scripTagCreate = shopify.ScriptTag.create({
    #             "event": "onload",
    #             "src": self.script_tag + "?v=" + str(time.time())
    #         })
    #         return scripTagCreate.id
    #     # ===============================================


