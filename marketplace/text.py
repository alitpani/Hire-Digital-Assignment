#from store.models import Product
import json
f = open('products.json')
data = json.load(f)
i = 1
"""new_json =    {
      "model": "store.model",
      "productId" "":,
      "productCategory":"",
      "productName":"",
      "productImage":"",
      "productStock": True
      "productPrice":0,
      "salePrice":0
   }"""
for p in data:
    pass
