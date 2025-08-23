from db import get_connection

user_data='''
CREATE TABLE IF NOT EXISTS UserData(
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100) UNIQUE
)'''

users='''CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone INT UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
)'''

sellers = '''CREATE TABLE IF NOT EXISTS sellers(
    seller_id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    contact_info VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    rating DECIMAL(2,1)
)'''

templates = '''CREATE TABLE IF NOT EXISTS templates(
    template_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) CHECK (type IN ('frame','poster','collage','gift')),
    price NUMERIC(10,2) NOT NULL,
    preview_image TEXT,
    design_file TEXT,
    seller_id INT NOT NULL,
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id) ON DELETE CASCADE
)'''

orders = '''CREATE TABLE IF NOT EXISTS orders(
    order_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    template_id INT NOT NULL,
    uploaded_photo_url TEXT,
    order_status VARCHAR(20) DEFAULT 'Pending' CHECK (order_status IN ('Pending','Processing','Shipped','Delivered','Cancelled')),
    payment_status VARCHAR(20) DEFAULT 'Pending' CHECK (payment_status IN ('Pending','Paid','Refunded')),
    total_price NUMERIC(10,2) NOT NULL,
    shipping_partner VARCHAR(100),
    tracking_id VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES templates(template_id) ON DELETE CASCADE
)'''

payments = '''CREATE TABLE IF NOT EXISTS payments(
    payment_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    amount NUMERIC(10,2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    transaction_status VARCHAR(20) DEFAULT 'Pending' CHECK (transaction_status IN ('Pending','Paid','Refunded')),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
)'''

delivery_tracking = '''CREATE TABLE IF NOT EXISTS delivery_tracking(
    tracking_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    courier_partner VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Shipped' CHECK (status IN ('Shipped','In Transit','Delivered')),
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
)'''

async def create_table():
    conn=await get_connection()
    try:
        await conn.execute(user_data)
        await conn.execute(users)
        await conn.execute(sellers)
        print("Tables created successfully")
    except Exception as e:
        return e
    finally:
        await conn.close()