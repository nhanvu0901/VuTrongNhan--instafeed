import shopify
import time
from odoo import models, fields, api
from odoo.http import request
from odoo.tools.safe_eval import datetime


class Product(models.Model):
    _name = 'product.data'
    _description = 'Prodcut Data'

    product_id = fields.Char(string="Product ID")
    product_img = fields.Char(string="Product image")
    product_name = fields.Char(string="Prodcut name")
    media_select = fields.Many2many('media.data',string="Media")
    shopify_shop = fields.Many2one('shopify.mint','Shopify Shop' ,ondelete='cascade')

    def get_product(self):
        product = {
            "id": self.product_id,
            "image_src": self.product_img,
            "name": self.product_name,
        }
        return product

