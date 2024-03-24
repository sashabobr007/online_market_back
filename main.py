
import bcrypt
from fastapi import FastAPI, File, UploadFile, Response, Depends
import io
import uvicorn
from db import Database
import json

from pydantic import BaseModel
from PIL import Image

from storage import Storage
disk = Storage()

class Imag(BaseModel):
    data: bytes

class UserAuth(BaseModel):
    login: str
    password: str

class Product(BaseModel):
    name: str
    price: int
    quantity: int
    description : str


class User(BaseModel):
    login: str
    password: str
    birtdate: str

class Image_l(BaseModel):
    id : int
    image: UploadFile = File(...)

app = FastAPI()


@app.post("/userimage")
async def upload_image(id: int, image: UploadFile = File(...)):
    contents = await image.read()
    print(id)
    t = image.filename.split(".")[1]
    with open(f"1.{t}", 'wb') as file:
        file.write(contents)
    disk.upload_file(f"1.{t}", id)
    # db = Database()
    # db.userimage(image.filename, contents)
    return {"message": "Image uploaded successfully"}

@app.post("/productimage")
async def upload_image(image: UploadFile = File(...)):
    contents = await image.read()
    db = Database()
    db.productimage(image.filename, contents)
    return {"message": "Image uploaded successfully"}


@app.get("/getimage/")
async def im_get(login: str):
    db = Database()
    im = db.get_im(login)
    image = Image.open(io.BytesIO(im))
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG')
    response = Response(content=output_buffer.getvalue(), media_type='image/jpeg')

    return response

@app.get("/getimage_product/")
async def im_get(id: int):
    db = Database()
    im = db.get_im_prod(id)
    image = Image.open(io.BytesIO(im))
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG')
    response = Response(content=output_buffer.getvalue(), media_type='image/jpeg')

    return response

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/user/")
def read_item(login : str):
    db = Database()
    date = db.get_date(login)
    return {"date" : date}

@app.post("/signin/")
def read_item(user : UserAuth):
    try:
        db = Database()
        db_pass = db.sign_in(user.login)[0][0]
        password_encode = user.password.encode()
        by = bytes(db_pass.encode())
        if bcrypt.checkpw(password_encode, by):
            return {"success" : "ok"}
        else:
            return {"success": "false"}

    except:
        return {"success": "false"}


@app.post("/signup/")
def read_item(user : User):
    try:
        db = Database()
        password = user.password.encode()
        #Да, библиотека bcrypt солит пароль.
        # Соль - это случайная строка, которая добавляется к паролю перед хешированием, чтобы усложнить процесс взлома хеша.
        # Библиотека bcrypt автоматически генерирует и добавляет соль к паролю перед хешированием.
        hash = bcrypt.hashpw(password, bcrypt.gensalt())
        hash = str(hash).strip("b'")
        db.sign_up(user.login, hash, user.birtdate)
        return {"success" : "ok"}
    except:
        return {"success": "false"}

@app.post("/new_product/")
async def read_item(product : Product):
    try:
        db = Database()
        id = db.new_product(product.name, product.price, product.quantity, product.description)
        return {"success" : str(id)}
    except:
        return {"success": "false"}


@app.get("/select/products")
async def select_workers():
    db = Database()
    res = db.get_products()
    new = {}
    newarr = []
    for item in res:
        workers = {
            'id': item[0],
            'name': item[1],
            'price': item[2],
            'quantity': item[3],
            'description' : item[4]
        }
        newarr.append(workers)
    new['product'] = newarr
    json_data = json.dumps(new, ensure_ascii=True)
    return Response(content=json_data)

#
# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}

if __name__ == "__main__":
    uvicorn.run(app,  port=8000)