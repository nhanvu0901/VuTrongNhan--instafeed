# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import shopify

from odoo import fields, models, api

import time

from odoo.http import request


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_version_shopify_mint = fields.Char(string='Api version',
                                           config_parameter="shopify_mint.api_version_shopify_mint")
    redirect_url_shopify_mint = fields.Char(string="Redirect URL",
                                            config_parameter="shopify_mint.redirect_url_shopify_mint")
    sp_api_key_shopify_mint = fields.Char(string='API Key', config_parameter="shopify_mint.sp_api_key_shopify_mint")
    sp_api_secret_key_shopify_mint = fields.Char(string='API secret key',
                                                 config_parameter="shopify_mint.sp_api_secret_key_shopify_mint")
    cdn_tag_shopify_mint = fields.Char(string='CDN tag', config_parameter="shopify_mint.cdn_tag_shopify_mint")

    meta_client_id = fields.Char(string="Meta Client ID", config_parameter="shopify_mint.meta_client_id")
    meta_client_secret = fields.Char(string="Meta Client Secret", config_parameter="shopify_mint.meta_client_secret")
    meta_redirect_url = fields.Char(string="Meta Redirect URL", config_parameter="shopify_mint.meta_redirect_url")
    facebook_appid = fields.Char(string="Facebook App ID", config_parameter="shopify_mint.facebook_appid")

    # dang sua
    def add_script_tag_to_shop_shopify_mint(self):
        src = self.cdn_tag_shopify_mint

        version = self.api_version_shopify_mint

        shop_app_url = request.env['shopify.mint'].sudo().search(
            [('shop_url', '=', 'instgram-mint-odoo.myshopify.com')], limit=1)

        new_session = shopify.Session(shop_app_url.shop_url, version,
                                      token=shop_app_url.sp_access_token)

        shopify.ShopifyResource.activate_session(new_session)

        scripTag = shopify.ScriptTag.find()
        for script in scripTag:
            if "index.js" in script.src:
                script.destroy()
        if src:
            scripTagCreate = shopify.ScriptTag.create({
                "event": "onload",
                "src": src + "?v=" + str(time.time())
            })
            return scripTagCreate.id
