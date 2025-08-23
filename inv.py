from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
from typing import Optional
import uuid


app=FastAPI()


inventory={}


class item(BaseModel):
    name:str
    price:float
    available:bool
class update_item(BaseModel):
    name:Optional [str]=None
    price:Optional [float]=None
    available:Optional [bool]=None    
    

#showing an added product using its id
@app.get("/products/{id}")
def get_by_id(id:str):
    if id in inventory:
        return {
            "id":id,
            "product":inventory[id]
        }
    raise HTTPException(status_code=404,detail="product not found")

#search for a product by name or max price category (making them optional)
@app.get("/products")
def search_product(name:Optional[str]=None,max_price:Optional[float]=None):
    found_items=[]
    for id,product in inventory.items():
        if name and name.lower() not in product["name"].lower():
            continue
        if max_price and product["price"]>max_price:#to handle none
            continue
        found_items.append({"id":id,"product":product})
    if found_items:    
        return found_items    
    raise HTTPException(status_code=404,detail="not found")

#adding a product
@app.post("/products")
def add_product(product:item):
    product_id=str(uuid.uuid4())
    tmp_product= product.model_dump()#.dict()
    if tmp_product["price"]<=0:
        raise HTTPException(status_code=400,detail="price must be positive value")
    inventory[product_id]=tmp_product
    
    return {
    "id": product_id,
    "product": inventory[product_id],
    "message": "Product added successfully"
}

    #return {"product":inventory[next_id-1]},{"ID": next_id-1},"is added successfully"#enhancing the return when adding a product by inventory user


#updating a product
@app.put("/products/{id}")
def update (id:str ,item:update_item):
    if id not in inventory:
        raise HTTPException(status_code=404,detail="product doesn't exist")#
    tmp_item=item.model_dump(exclude_unset=True)
    inventory[id].update(tmp_item)
    return {"id": id, "product": inventory[id], "message": "Product updated successfully"}


#deleting a product
@app.delete("/products/{id}")
def delete_product(id: str):
    if id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    deleted = inventory.pop(id)
    return {"id": id, "deleted_product": deleted, "message": "Product deleted successfully"}
#generate the id Internally
#and return it to the frontend
#first we need to apply REST API to our backend


#auth in restful api