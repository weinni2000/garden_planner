import pandas as pd
import pathlib
from image_updater import get_client
import math


def create_product_with_variantes(row):
    db, uid, password, models = get_client()

    # product_template_image_ids
    idlist = []

    model_name = "product.template"

    try:
        if math.isnan(row["Sorte"]):
            row["Sorte"] = ""
    except Exception as e:
        pass

    langer_name = row["Latein"] + " " + row["Sorte"]
    row["langer_name"] = langer_name

    products = models.execute_kw(db, uid, password,
                                 model_name, 'search_read',
                                 # [[['is_company', '=', True]]]
                                 #
                                 [[("name", "=", langer_name)]], {'fields': ['name', 'name_latein'], 'limit': 50})

    if products == []:
        id = models.execute_kw(db, uid, password, "product.template", 'create', [{
            "name": row["langer_name"],
            "name_latein": row["Latein"],
            "name_common": row["Deutsch"],
            "sorte": row["Sorte"],
            "dtm": row["DTM"],
            "generation": row["generation"],
            "aussaat": str(row["Aussaat"]),
            "start_harvest": str(row["START OF HARVEST"]),
            "end_harvest": str(row["END OF HARVEST"]),
        }])


path = pathlib.Path(__file__).parent.resolve()

df = pd.read_excel(
    str(path) + "/../data/Anbauplanung/AnbauplanungBlumen LisiGrün.xlsx", sheet_name="GAME PLAN")

for index, row in df.iterrows():
    create_product_with_variantes(row)


print(df)
