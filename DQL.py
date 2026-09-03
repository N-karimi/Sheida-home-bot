#*************My code**********
#*********برای گرفتن اطلاعات
import mysql.connector
from config import *

def get_product_info(pid):
    conn= mysql.connector.connection.MySQLConnection(**database_config, database= database)
    cur= conn.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM PRODUCT WHERE ID=%s"
    cur.execute(SQL_QUERY, (pid,))
    info = cur.fetchone()
    cur.close()
    conn.close()
    return info

#دسته بندی محصولات
def get_products_cat(category):
    conn= mysql.connector.connection.MySQLConnection(**database_config, database= database)
    cur= conn.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM PRODUCT WHERE TRIM(category)=%s"
    cur.execute(SQL_QUERY, (category,))
    products= cur.fetchall()
    cur.close()
    conn.close()
    return products

#جدیدترین محصولات
def get_new_products():
    conn= mysql.connector.connection.MySQLConnection(**database_config, database= database)
    cur= conn.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM PRODUCT ORDER BY ID DESC LIMIT 5"
    cur.execute(SQL_QUERY)
    products= cur.fetchall()
    cur.close()
    conn.close()
    return products

#جست و جو محصولات 
def search_products(name):
    conn= mysql.connector.connection.MySQLConnection(**database_config, database= database)
    cur= conn.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM PRODUCT WHERE name LIKE %s"
    cur.execute(SQL_QUERY, (f"%{name}%",))
    products= cur.fetchall()
    cur.close()
    conn.close()
    return products

# گرفتن اطلاعات کاربران
def get_users(cid):
    conn= mysql.connector.connection.MySQLConnection(**database_config, database= database)
    cur= conn.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM USERS WHERE CID=%s"
    cur.execute(SQL_QUERY, (cid,))
    user_inf= cur.fetchone()
    cur.close()
    conn.close()
    return user_inf
    

def get_all_users():
    conn= mysql.connector.connection.MySQLConnection(**database_config, database= database)
    cur= conn.cursor(dictionary=True)
    SQL_QUERY= "SELECT CID FROM USERS;"
    cur.execute(SQL_QUERY)
    users= cur.fetchall()
    cur.close()
    conn.close()
    return [ row['CID'] for row in users]

def get_cart_shopping(user_id):
    conn= mysql.connector.connection.MySQLConnection(**database_config, database= database)
    cur= conn.cursor(dictionary=True)
    SQL_QUERY= "SELECT * FROM cart_shopping WHERE user_id=%s"
    cur.execute(SQL_QUERY,(user_id,))
    cart_shop= cur.fetchone()
    cur.close()
    conn.close()
    return cart_shop

def get_cart_item(cart_id):
    conn= mysql.connector.connection.MySQLConnection(**database_config, database= database)
    cur= conn.cursor(dictionary=True)
    SQL_QUERY= "SELECT * FROM cart_item WHERE cart_id=%s"
    cur.execute(SQL_QUERY, (cart_id,))
    item= cur.fetchall()
    cur.close()
    conn.close()
    return item

if __name__ == "__main__":
    info= get_product_info(1)
    

