import sqlite3


def create_users_table():
    database=sqlite3.connect(' 7 SABER.db')
    cursor=database.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users(
           user_id INTEGER PRIMARY KEY AUTOINCREMENT,
           full_name TEXT,
           telegram_id BIGINT NOT NULL UNIQUE,
           phone TEXT
        );
        ''')
    database.commit()
    database.close()

# create_users_table()

def create_carts_table():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
       cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER REFERENCES users(user_id),
       total_price DECIMAL(12, 2) DEFAULT 0,
       total_shirts INTEGER DEFAULT 0
       );
       ''')
    database.commit()
    database.close()

# create_carts_table()


def create_cart_shirts_table():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_shirts(
    cart_shirt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    shirt_name VARCHAR(30),
    quantity INTEGER NOT NULL,
    final_price DECIMAL(12, 2) NOT NULL,
    cart_id INTEGER REFERENCES carts(cart_id),
    
    
    UNIQUE(shirt_name, cart_id)
    );
    ''')
    database.commit()
    database.close()


# create_cart_shirts_table()


def create_categories_table():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name VARCHAR(30) NOT NULL UNIQUE
    );
    ''')
    database.commit()
    database.close()

# create_categories_table()

def insert_categories():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(category_name) VALUES
    ('SPORT Kostyumi'),
    ('SPORT Futbolkasi 👕'),
    ('SPORT Shortigi 🩳'),
    ('SPORT Kedalari'),
    ('SABER Krossovkasi'),
    ('7BIG Maykasi 🎽')
    ''')
    database.commit()
    database.close()


# insert_categories()



def create_shirts_table():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shirts(
    shirt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    shirt_name VARCHAR(30) NOT NULL UNIQUE,
    price DECIMAL(12, 2) NOT NULL,
    description TEXT,
    image TEXT,
    
    FOREIGN KEY(category_id) REFERENCES catigories(category_id)
    );
    ''')
    database.commit()
    database.close()

# create_shirts_table()

def insert_shirts_table():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO shirts(category_id, shirt_name, price, description, image) VALUES
    (1,'sport maykasi',120000,'Qulay sport bop mayka kiyishga qulay','media/kiyimlar/7 _BIG_MAYKASI.jpg'),
    (1,'saber krossovkasi',300000,'juda yumshoq yengil sifatli krossovka','media/kiyimlar/saber krossovkasi.jpg'),
    (1,'sport futbolkasi',100000,'paxtali yumshoq futbolka sintetika emas','media/kiyimlar/sport futbolkasi.jpg'),
    (1,'sport kedalari',200000,'sport bop yugurishga qulay keda','media/kiyimlar/sport kedalari.jpg'),
    (1,'sport kostyumi',240000,'yumshoq matoli sport kostyumi','media/kiyimlar/sport kostyumi.jpg'),
    (1,'sport shortigi',140000,'sport bop yumshoq matoli  shortig','media/kiyimlar/sport shortigi.jpg')
    ''')
    database.commit()
    database.close()


# insert_shirts_table()

def first_select_user(chat_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()
    database.close()
    return user

def first_register_user(chat_id, full_name):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name) VALUES(?, ?)
    ''',(chat_id, full_name))
    database.commit()
    database.close()

def update_user_to_finish_register_(chat_id, phone):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users
    SET phone = ?
    WHERE telegram_id = ?
    ''',(phone, chat_id))
    database.commit()
    database.close()

def insert_to_cart(chat_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO carts(user_id) VALUES
    (
    (SELECT user_id FROM users WHERE telegram_id = ?)
    )
    ''',(chat_id,))
    database.commit()
    database.close()

def get_all_categoires():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM categories
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories

def get_shirts_by_category_id(category_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT shirt_id, shirt_name
    FROM shirts WHERE category_id = ?
    ''', (category_id,))
    shirts = cursor.fetchall()
    database.close()
    return shirts

def get_shirt_detail(shirt_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM shirts
    WHERE shirt_id = ?
    ''',(shirt_id,))
    shirt = cursor.fetchone()
    database.close()
    return shirt

def get_user_cart_id(chat_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_id FROM carts
    WHERE user_id=(SELECT user_id FROM users WHERE telegram_id=?)
    ''',(chat_id, ))
    cart_id= cursor.fetchone()[0]
    database.close()
    return cart_id


def insert_or_update_cart_shirt(cart_id,shirt,quantity,final_price):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    try:
        cursor.execute('''
        INSERT INTO cart_shirts(cart_id,shirt_name,quantity,final_price)
        VALUES(?, ?, ?, ?)
        ''',(cart_id,shirt,quantity,final_price))
        database.commit()
        return True
    except:
        cursor.execute('''
        UPDATE cart_shirts
        SET quantity = ?,
        final_price = ?
        WHERE shirt_name = ? AND cart_id  = ?
        ''',(quantity,final_price,shirt,cart_id))
        database.commit()
        return  False
    finally:
        database.close()


def update_total_shirt_total_price(cart_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE carts 
    SET total_shirts = (
    SELECT SUM(quantity) FROM cart_shirts
    WHERE cart_id = :cart_id
    ),
    total_price = (
    SELECT SUM(final_price) FROM cart_shirts
    WHERE cart_id = :cart_id
    )
    WHERE cart_id = :cart_id
    ''',{'cart_id': cart_id})
    database.commit()
    database.close()


def get_cart_shirts(cart_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT shirt_name, quantity, final_price
    FROM cart_shirts
    WHERE cart_id = ?
    ''',(cart_id,))
    cart_shirts = cursor.fetchall()
    database.close()
    return cart_shirts


def get_total_shirts_price(cart_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT total_shirts,total_price FROM carts WHERE cart_id = ?
    ''',(cart_id,))
    total_shirts,total_price = cursor.fetchone()
    database.close()
    return total_shirts,total_price


def get_cart_shirt_for_delete(cart_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_shirt_id, shirt_name
    FROM cart_shirts
    WHERE cart_id = ?
    ''',(cart_id,))
    cart_shirts = cursor.fetchall()
    database.close()
    return cart_shirts


def  delete_cart_shirt_from_database(cart_shirt_id):
     database = sqlite3.connect(' 7 SABER.db')
     cursor = database.cursor()
     cursor.execute('''
     DELETE FROM cart_shirts WHERE cart_shirt_id = ?
     ''',(cart_shirt_id,))
     database.commit()
     database.close()

def drop_cart_shirts_default(cart_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_shirts
    WHERE cart_id = ?
    ''',(cart_id,))
    database.commit()
    database.close()


def orders_check():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders_check(
    order_check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER REFERENCES carts(cart_id),
    total_price DECIMAL(12, 2) DEFAULT 0,
    total_shirts INTEGER DEFAULT 0,
    time_order TEXT,
    date_order TEXT
    );
    ''')
    database.commit()
    database.close()
# orders_check()

def order():
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_check_id INTEGER REFERENCES orders_check(order_check_id),
    shirt_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    final_price DECIMAL(12, 2) NOT NULL
    );
    ''')

# order()
def  save_order_check(cart_id, total_shirts, total_price, time_order, date_order):
     database = sqlite3.connect(' 7 SABER.db')
     cursor = database.cursor()
     cursor.execute('''
     INSERT INTO orders_check(cart_id, total_shirts, total_price, time_order, date_order)
     VALUES(?,?,?,?,?)
     ''', (cart_id, total_shirts, total_price, time_order, date_order))
     database.commit()
     database.close()

def save_order(order_check_id, shirt_name, quantity, final_price):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO orders(order_check_id, shirt_name, quantity, final_price)
    VALUES(?,?,?,?)
    ''',(order_check_id, shirt_name, quantity, final_price))
    database.commit()
    database.close()


def get_order_check(cart_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM orders_check
    WHERE cart_id = ?
    ''',(cart_id,))
    order_check_info = cursor.fetchall()
    database.close()
    return order_check_info


def get_detail_order(id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT shirt_name,quantity,final_price FROM orders
    WHERE order_check_id = ?
    ''',(id,))
    detail_order = cursor.fetchall()
    database.close()
    return detail_order

def get_order_check_id(cart_id):
    database = sqlite3.connect(' 7 SABER.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT order_check_id FROM orders_check
    WHERE cart_id = ?
    ''',(cart_id,))
    order_check_id = cursor.fetchall()[-1][0]
    database.close()
    return order_check_id
