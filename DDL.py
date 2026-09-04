#*************My code***********
#فایل ساختار های database
import mysql.connector
from config import *

def drop_n_create_database(Database_name):
    conn = mysql.connector.connection.MySQLConnection(**database_config)  
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {Database_name};")
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {Database_name};")
    conn.commit()
    cur.close()
    conn.close()
    print('Database created!!')
    
#balance برای خرید و چک کردن کارت به کارت است
def create_users_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
    cur = conn.cursor()
    cur.execute("""
                create table users (
	                `cid`  		    bigint unsigned  not null primary key,
                    `first_name` 	varchar(50) not null,
                    `last_name` 	varchar(50) ,
                    `username` 	    varchar(40) ,
                    `phone` 	    varchar(13) ,
                    `balance`       bigint unsigned not null default 0,
                    `is_block`      enum ('yes','no') default 'no',
                    `spam_score`    tinyint unsigned not null default 0,
                    `expire_spam`   datetime default current_timestamp,
                    `num_buy` 	    int unsigned ,
                    `num_invite` 	int unsigned,
                    `register_date` datetime default current_timestamp,
                    `last_update`   datetime default current_timestamp on update current_timestamp
                );""")
    conn.commit()
    cur.close()
    conn.close()
    print('table users created !!')


def create_category_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
    cur = conn.cursor()
    cur.execute("""
                create table category (
                    `id` 		    int unsigned not null AUTO_INCREMENT primary key,
                    `name` 		    varchar(30) not null,
                    `register_date` datetime default current_timestamp,
                    `last_update`   datetime default current_timestamp on update current_timestamp
                )AUTO_INCREMENT=1;""")
    conn.commit()
    cur.close()
    conn.close()
    print('table Category created !!')


def create_product_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
    cur = conn.cursor()
    cur.execute("""
                create table product (
                    `id` 		    int unsigned not null AUTO_INCREMENT primary key,
                    `name` 		    varchar(40) not null,
                    `description`   varchar(100),
                    `price`         double not null,
                    `inventory`     mediumint unsigned not null default 0,
                    `new_pro` 	    varchar(40),
                    `topping_pro` 	varchar(40),
                    `offer_pro` 	varchar(40),
                    `file_id`       varchar(100),
                    `channel_mid`   int unsigned ,
                    `category`      varchar(30),
                    `register_date` datetime default current_timestamp,
                    `last_update`   datetime default current_timestamp on update current_timestamp
                )AUTO_INCREMENT=1;""")
    conn.commit()
    cur.close()
    conn.close()
    print('table product created !!')


def create_favorite_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
    cur = conn.cursor()
    cur.execute("""
                create table favorite (
                    `id` 		    int unsigned not null primary key,
                    `user_cid` 	    bigint unsigned,
                    `prod_id` 	    int unsigned not null,
                    `register_date` datetime default current_timestamp,
                    `last_update`   datetime default current_timestamp on update current_timestamp,
                    foreign key (user_cid) references users(cid),
                    foreign key (prod_id) references product(id) 
                );""")
    conn.commit()
    cur.close()
    conn.close()
    print('table favorite created !!')


def create_orders_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
    cur = conn.cursor()
    cur.execute("""
                create table orders (
                    `id` 		    int unsigned not null primary key,
                    `user_id` 	    bigint unsigned not null,
                    `price` 	    double,
                    `discount` 	    TINYINT unsigned default (0),
                    `date_time` 	DATETIME not null,
                    `code` 		    int unsigned not null,
                    `register_date` datetime default current_timestamp,
                    `last_update`   datetime default current_timestamp on update current_timestamp,
                    foreign key (user_id) references users(cid) 
                );""")
    conn.commit()
    cur.close()
    conn.close()
    print('table orders created !!')


def create_order_item_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
    cur = conn.cursor()
    cur.execute("""
                create table order_item (
                    `id` 		    int unsigned not null primary key,
                    `order_id` 	    int unsigned not null,
                    `prod_id` 	    int unsigned not null,
                    `price` 	    double,
                    `description` 	varchar(100),
                    `register_date` datetime default current_timestamp,
                    `last_update`   datetime default current_timestamp on update current_timestamp,
                    foreign key (order_id) references orders(id),
                    foreign key (prod_id) references product(id) 
                );""")
    conn.commit()
    cur.close()
    conn.close()
    print('table order_item created !!')


def create_cart_shopping_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
    cur = conn.cursor()
    cur.execute("""
                create table cart_shopping (
                    `id` 		    int unsigned not null primary key,
                    `user_id` 	    bigint unsigned not null,
                    `date` 		    DATE not null,
                    `register_date` datetime default current_timestamp,
                    `last_update`   datetime default current_timestamp on update current_timestamp,
                    foreign key (user_id) references users(cid) 
                );""")
    conn.commit()
    cur.close()
    conn.close()
    print('table cart_shopping created !!')


def create_cart_item_table():
    conn = mysql.connector.connection.MySQLConnection(**database_config, database=database_name)
    cur = conn.cursor()
    cur.execute("""
                create table cart_item (
                    `id` 		    int unsigned not null primary key,
                    `cart_id` 	    int unsigned not null,
                    `prod_id` 	    int unsigned not null,
                    `number` 	    SMALLINT unsigned,
                    `register_date` datetime default current_timestamp,
                    `last_update`   datetime default current_timestamp on update current_timestamp,
                    foreign key (cart_id) references cart_shopping(id),
                    foreign key (prod_id) references product(id)  
                );""")
    conn.commit()
    cur.close()
    conn.close()
    print('table cart_item created !!')



if __name__ == '__main__':
    drop_n_create_database(database_name)
    create_users_table()
    create_category_table()
    create_product_table()
    create_favorite_table()
    create_orders_table()
    create_order_item_table()
    create_cart_shopping_table()
    create_cart_item_table()