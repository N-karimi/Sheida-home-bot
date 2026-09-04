#*************My code***********
#******برای اضافه کردن محصولات و اطلاعات
import mysql.connector
from config import *

def insert_users_data(cid, first_name,last_name=None,username=None,phone=None):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "INSERT INTO users (cid, first_name,last_name,username,phone) VALUES (%s, %s, %s, %s, %s);"
   cur.execute(SQL_QUERY, (cid, first_name,last_name,username,phone))
   conn.commit()
   #id_user = cur.lastrowid
   cur.close()
   conn.close()
   return True


def insert_product_data(name, price, inventory=0, description=None, file_id=None, channel_mid=None, category=None):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "INSERT INTO product (name, description, price, inventory, file_id, channel_mid,category) VALUES (%s, %s, %s, %s, %s, %s, %s);"
   cur.execute(SQL_QUERY, (name, description, price, inventory, file_id, channel_mid,category))
   pid=cur.lastrowid
   conn.commit()
   cur.close()
   conn.close()
   return pid


def insert_category_data(name):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "INSERT INTO category (name) VALUES (%s);"
   cur.execute(SQL_QUERY, (name,))
   conn.commit()
   cur.close()
   conn.close()

def insert_favorite_data(id,user_cid,prod_id):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "INSERT INTO favorite (id,user_cid,prod_id) VALUES (%s,%s,%s);"
   cur.execute(SQL_QUERY, (id,user_cid,prod_id))
   conn.commit()
   cur.close()
   conn.close()


def insert_orders_data(id,user_id,price=None,discount=None,date_time=None,code=None):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "INSERT INTO orders (id,user_id,price,discount,date_time,code) VALUES (%s,%s,%s,%s,%s,%s);"
   cur.execute(SQL_QUERY, (id,user_id,price,discount,date_time,code))
   conn.commit()
   cur.close()
   conn.close()


def insert_order_item_data(id, order_id, prod_id, price=None, description=None):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "INSERT INTO order_item (id, order_id, prod_id, price, description) VALUES (%s,%s,%s,%s,%s);"
   cur.execute(SQL_QUERY, (id, order_id, prod_id, price, description))
   conn.commit()
   cur.close()
   conn.close()


def insert_cart_shopping_data(user_id, date):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "SELECT MAX(id) FROM cart_shopping"
   cur.execute(SQL_QUERY)
   result=cur.fetchone()
   if result[0] is None:
      cart_id= 1
   else: 
      cart_id= result[0]+1
   SQL_QUERY="INSERT INTO cart_shopping (id, user_id, date) VALUES (%s,%s,%s)"
   cur.execute(SQL_QUERY, (cart_id, user_id, date))
   conn.commit()
   cur.close()
   conn.close()
   return cart_id


def insert_cart_item_data(cart_id, prod_id, number=1):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "INSERT INTO cart_item (cart_id, prod_id, number) VALUES (%s,%s,%s);"
   cur.execute(SQL_QUERY, (cart_id, prod_id, number))
   conn.commit()
   cur.close()
   conn.close()

def edit_name(cid, name):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "UPDATE users SET first_name=%s WHERE  cid=%s"
   cur.execute(SQL_QUERY, (name,cid))
   conn.commit()
   cur.close()
   conn.close()

def edit_phone(cid, phone):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "UPDATE users SET phone=%s WHERE  cid=%s"
   cur.execute(SQL_QUERY, (phone,cid))
   print(cur.rowcount)
   conn.commit()
   cur.close()
   conn.close()

def edit_address(cid, address):
   conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
   cur = conn.cursor()
   SQL_QUERY = "UPDATE users SET address=%s WHERE  cid=%s"
   cur.execute(SQL_QUERY, (address,cid))
   conn.commit()
   cur.close()
   conn.close()

def edit_cart_item(cart_id, prod_id, number):
   conn= mysql.connector.connection.MySQLConnection(**database_config, database= database_name)
   cur= conn.cursor()
   SQL_QUERY= "DELETE FROM cart_item WHERE cart_id=%s AND prod_id=%s"
   cur.execute(SQL_QUERY, (cart_id, prod_id))
   SQL_QUERY="INSERT INTO cart_item (cart_id, prod_id, number) VALUES (%s,%s,%s)"
   cur.execute(SQL_QUERY, (cart_id, prod_id, number))
   conn.commit()
   cur.close()
   conn.close()

def delete_cart(cart_id, prod_id):
   conn= mysql.connector.connection.MySQLConnection(**database_config, database= database_name)
   cur= conn.cursor()
   SQL_QUERY= "DELETE FROM cart_item WHERE cart_id=%s AND prod_id=%s"
   cur.execute(SQL_QUERY, (cart_id, prod_id))
   conn.commit()
   cur.close()
   conn.close()
