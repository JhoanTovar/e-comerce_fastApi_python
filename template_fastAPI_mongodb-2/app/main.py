import os
from typing import Union

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")

# Modelos
class Product(BaseModel):
    id: int
    name: str
    size: str
    price: float
    in_stock: bool

class User(BaseModel):
    id: int
    name: str
    email: str

class Order(BaseModel):
    id: int
    user_id: int
    products: List[Product]
    total_price: float


# Datos de ejemplo
products = [
    Product(id=1, name="Camiseta blanca basica", price=40000, size="L", in_stock=True),
    Product(id=2, name="Camisa manga larga negra", price=89000, size="L", in_stock=True),
]

users = [
    User(id=1, name="Jhoan Tovar", email="tovarjhoan82sfgmail.com"),
]

orders = []
# templates = Jinja2Templates(directory="templates")

def get_next_order_id():
    return max([order.id for order in orders], default=0) + 1

@app.get("/")
async def read_root():
    return {"Hola": "Jhoan Tovar"}

@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "app/static", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None,):
    return {"item_id": item_id, "q": q}


# Rutas
@app.get("/products")
def get_products():
    return products

@app.post("/products")
def add_product(product: Product):
    # Verificar si el producto ya existe por ID
    for p in products:
        if p.id == product.id:
            raise HTTPException(status_code=400, detail="El producto ya existe")

    products.append(product)
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    for idx, p in enumerate(products):
        if p.id == product_id:
            products[idx] = product
            return product
    return {"error": "Producto no encontrado"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for idx, p in enumerate(products):
        if p.id == product_id:
            del products[idx]
            return {"message": "Producto eliminado"}
    return {"error": "Producto no encontrado"}

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    for idx, u in enumerate(users):
        if u.id == user_id:
            users[idx] = user
            return user
    return {"error": "Usuario no encontrado"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for idx, u in enumerate(users):
        if u.id == user_id:
            del users[idx]
            return {"message": "Usuario eliminado"}
    return {"error": "Usuario no encontrado"}


# TAREA

@app.get("/orders", tags=["Orders"])
def get_orders():
    return orders

@app.post("/orders")
def create_order(order: Order):
    order_id = get_next_order_id()
    order.id = order_id
    orders.append(order)
    return {"message": f"Orden  numero {order_id} creada"}

@app.put("/orders/{order_id}")
def update_order(order_id: int, updated_order: Order):
    for idx, order in enumerate(orders):
        if order.id == order_id:
            orders[idx] = updated_order
            return {"message": "Orden actualizada"}
    raise HTTPException(status_code=404, detail="Orden no encontrada")

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    for idx, order in enumerate(orders):
        if order.id == order_id:
            del orders[idx]
            return {"message": "Orden eliminada"}
    raise HTTPException(status_code=404, detail="Orden no encontrada")