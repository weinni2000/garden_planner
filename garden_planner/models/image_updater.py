import xmlrpc.client
from nikenium import get_flower_pictures

# info = xmlrpc.client.ServerProxy('http://localhost:8069/start').start()


def get_client():
    url = "http://localhost:8069"
    db = "nikdb"
    username = 'weinni2000@gmail.com'
    password = 'odoo'

    info = {"url": url, "db": db, "username": username,
            "password": password, "host": url, "database": db, "user": username}

    url, db, username, password = \
        info['host'], info['database'], info['user'], info['password']

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()
    print(version)

    uid = common.authenticate(db, username, password, {})
    print(uid)

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return db, uid, password, models


def get_images():
    db, uid, password, models = get_client()
    model_name = 'product.template'

    products = models.execute_kw(db, uid, password,
                                 model_name, 'search_read',
                                 # [[['is_company', '=', True]]]
                                 #
                                 [[("image_1920", "=", False)]], {'fields': ['name', 'name_latein'], 'limit': 150})

    for product in products:
        # input = {"search_term": "gänseblümchen"}
        product["search_term"] = product["name"]
        product = get_flower_pictures(product)

        models.execute_kw(db, uid, password, model_name, 'write', [[product["id"]], {

        }])

        # product_template_image_ids
        idlist = []
        for image in product["images"]:
            id = models.execute_kw(db, uid, password, "product.image", 'create', [{
                'image_1920': image["src_string"], "name": image["search_term"]
            }])
            idlist.append(id)

        models.execute_kw(db, uid, password, model_name, 'write', [[product["id"]], {
            'product_template_image_ids': idlist,
            'image_1920': product["images"][0]["src_string"]
        }])

        print(product)


if __name__ == '__main__':
    #  test_google()
    get_images()
