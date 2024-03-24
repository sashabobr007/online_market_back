import psycopg2
from settings import *
class Database():
    def __init__(self):
        self.con = psycopg2.connect(database=database,
                                    user=user,
                                    password=password,
                                    host=host,
                                    port=port
                                    )

    def sign_up(self, login, password, birthdate):
        cursor = self.con.cursor()
        cursor.execute(f"insert into users (login, password, birthdate) values  ('{login}', '{password}', '{birthdate}');")
        self.con.commit()
        self.con.close()

    def new_product(self, name, price, quantity, description):
        cursor = self.con.cursor()
        cursor.execute(f"insert into products (name, price, quantity, description) values  ('{name}', {price},"
                       f" {quantity}, '{description}');")
        cursor.execute(f"select max(id) from products;")
        result = cursor.fetchone()[0]
        self.con.commit()
        self.con.close()
        return result

    def userimage(self, login, photo):
        cursor = self.con.cursor()
        binary = psycopg2.Binary(photo)
        cursor.execute(f"update users set photo={binary} where login='{login}';")
        self.con.commit()
        self.con.close()

    def productimage(self, id, photo):
        cursor = self.con.cursor()
        binary = psycopg2.Binary(photo)
        cursor.execute(f"update products set photo={binary} where id={id};")
        self.con.commit()
        self.con.close()


    def sign_in(self, login):
        cursor = self.con.cursor()
        cursor.execute(f"select password from users where login='{login}';")
        result = cursor.fetchall()
        return result

    def get_im(self, login):
        cursor = self.con.cursor()
        cursor.execute(f"select photo from users where login='{login}';")
        result = cursor.fetchone()[0]
        return result

    def get_im_prod(self, id):
        cursor = self.con.cursor()
        cursor.execute(f"select photo from products where id={id};")
        result = cursor.fetchone()[0]
        return result

    def get_date(self, login):
        cursor = self.con.cursor()
        cursor.execute(f"select birthdate from users where login='{login}';")
        result = cursor.fetchone()[0]
        return result

    def get_products(self):
        cursor = self.con.cursor()
        cursor.execute(f"select id, name, price, quantity, description from products;")
        result = cursor.fetchall()
        return result
