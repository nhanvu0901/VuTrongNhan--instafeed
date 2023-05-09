import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime


class Product(models.Model):
    _name = 'hotspot.private'
    _description = 'Hotspot'

    name = fields.Char(default='')
    shopify_product_id = fields.Char(default='')
    shopify_product_handle = fields.Char(default='')
    shopify_product_img_src = fields.Char(default='')
    shopify_product_variant_num = fields.Integer(default=0)
    shopify_product_product_url = fields.Char(default='')
    shopify_product_price_range = fields.Char(default='')


    admin = fields.Many2one('res.users')
    post = fields.Many2one('post.private')
    status = fields.Boolean(default=False)

    def get_product(self):
        product = {
            "id": self.shopify_product_id,
            "image_src": self.shopify_product_img_src,
            "name": self.name,
            "handle":self.shopify_product_handle,
            "variant_num":self.shopify_product_variant_num,
            "product_url":self.shopify_product_product_url,
            "price_range":self.shopify_product_price_range
        }
        return product

