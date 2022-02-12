# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import re
import ast
import random
import string
import json
import pandas as pd
import os


class instagram_content_loader(http.Controller):

    @ http.route('/instagram_content_loader/objects/<model("instagram_content_loader.highlights"):obj>/', website=True, auth='public')
    def nikshighlight(self, obj, **kw):
        print(obj)
        instaposts = ""
        return http.request.render('instagram_content_loader.niksindex', {
            'highlights': instaposts
        })

    @http.route('/import_csv', type="json", website=True, auth='public')
    def testroute(self, **kw):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        df = pd.read_csv(dir_path + '/AnbauplanungBlumen.csv', sep=';')

        instapost = request.env["product.template"].sudo().search([
        ])

        for index, row in df.iterrows():
            if index < 10:
                instapost = request.env["product.template"].sudo().create({
                    "description": "IT",
                    "name": row["Latein"],
                    "name_latein": row["Deutsch"],
                    "name_common": row["Latein"],
                })

        test = {"status": "9499 everything alright"}

        return json.dumps(test)

    @http.route('/instagram/gallery/json', website=True, auth='public')
    def gallery(self, **kw):
        instaposts = ""

        return json.dumps(instaposts)

    @http.route('/instagram/gallery/', website=True, auth='public')
    def gallery(self, **kw):
        instaposts = ""

        return request.render("instagram_content_loader.niksindex", {"highlights": instaposts})

    @http.route('/instagram/highlights/', website=True, auth='public')
    def highlights(self, **kw):
        instaposts = ""

        return request.render("instagram_content_loader.instagram_content_loader_page_highlight", {"instapost": instaposts})

    @http.route('/insta', website=True, auth='public')
    def save(self, **kw):
        instaposts = ""
        return request.render("instagram_content_loader.instagram_content_loader_page_carousel", {"instaposts": [instaposts]})

    @http.route('/instagram/posts/carousel', website=True, auth='public')
    def save(self, **kw):
        instaposts = ""

        return request.render("instagram_content_loader.instagram_content_loader_page_carousel", {"instaposts": [instaposts]})

    @ http.route('/instagram/instagram_content_loader/', website=True, auth='public')
    def instagram_content_loader(self, **kw):
        return "Hello, world"

    @ http.route('/instagram_content_loader/instagram_content_loader/', website=True, auth='public')
    def index(self, **kw):
        # return "Hello, world"
        instapost = request.env["instagram_content_loader.instapost"].sudo().search([
        ])
        return request.render("instagram_content_loader.instagram_content_loader_page", {"instapost": instapost})

    @ http.route('/instagram_content_loader/instagram_content_loader/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('instagram_content_loader.listing', {
            'root': '/instagram_content_loader/instagram_content_loader',
            'objects': http.request.env['instagram_content_loader.instagram_content_loader'].search([]),
        })

    @ http.route('/instagram_content_loader/instagram_content_loader/objects/<model("instagram_content_loader.instagram_content_loader"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('instagram_content_loader.object', {
            'object': obj
        })


def do_before():
    print("Hello before")


class Extension(instagram_content_loader):
    @http.route()
    def nikshighlight(self, obj):
        do_before()
        return super(Extension, self).nikshighlight(obj)
