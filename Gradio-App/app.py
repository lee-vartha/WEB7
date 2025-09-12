# imports
import gradio as gr
import sqlite3
import jwt
import time
from passlib.hash import pbkdf2_sha256 

# config
JWT_SECRET_KEY = "mysecret"
TOKEN_EXPIRES_SECONDS = 3600 #hour

# initiate database
def init_db():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
              id INT PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              email TEXT UNIQUE,
              password TEXT,
              role TEXT CHECK(role IN ('donor', 'beneficiary')),
              tokens INT DEFAULT 10
              )
        """)
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
            id INT PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            cost INT,
            owner_email TEXT
            )
              
        """)
    
    conn.commit()
    conn.close()

init_db()


# JWT 
def create_token(email, role):
    payload = {
        "email": email,
        "role": role,
        "exp": time.time() + TOKEN_EXPIRES_SECONDS
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def register(name, email, password, role):
    hashed_pw = pbkdf2_sha256.hash(password)
    try:
        conn = sqlite3.connect("app.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                  (name, email, hashed_pw, role))
        conn.commit()
        conn.close()
        return "Registration successful"
    except sqlite3.IntegrityError:
        return "Email already used"
    
def login(email, password):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT password, role FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if row and pbkdf2_sha256.verify(password, row[0]):
        token = create_token(email, row[1])
        return token
    else:
        return None
    
def add_product(name, cost, owner_email):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, cost, owner_email) VALUES (?, ?, ?)",
              (name, cost, owner_email))
    conn.commit()
    conn.close()
    return f"Product '{name} added!"

def list_products():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT id, name, cost, owner_email FROM products")
    items = c.fetchall()
    conn.close()
    return "\n".join([f"{id}. {name} - {cost} tokens (by {owner})" for id, name, cost, owner in items])

def spend_tokens(user_email, product_id):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()

    c.execute("SELECT name, cost FROM products WHERE id =?", (product_id,))
    product = c.fetchone()
    if not product:
        return "Product not found"
    
    name, cost = product
    
    c.execute("SELECT tokens FROM users WHERE email = ?", (user_email,))
    user = c.fetchone()
    if not user:
        return "User not found"
    
    current_tokens = user[0]

    if current_tokens < cost:
        return "Not enough tokens"
    
    c.execute("UPDATE user SET tokens = tokens - ? WHERE email = ?", (cost, user_email))
    conn.commit()
    conn.close()

    return f"You bought '{name}, for {cost} tokens"


def get_token_balance(email):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT tokens FROM users WHERE email = ?", (email,))
    tokens = c.fetchone()
    conn.close()
    return f"You have {tokens[0]} tokens." if tokens else "User not found"

# INTERFACE
with gr.Blocks() as app:
    gr.Markdown("## Charity App - Gradio + SQLite + JWT")
    state = gr.State(value=None) # holds the JWT

    with gr.Tab("Register"):
        r_name = gr.Textbox(label="Name")
        r_email = gr.Textbox(label="Email")
        r_pass = gr.Textbox(label="Password", type="password")
        r_role = gr.Dropdown(["member", "beneficiary"], label="Role")
        r_out = gr.Textbox(label="Status")
        gr.Button("Register").click(register,
            inputs=[r_name, r_email, r_pass, r_role],
            outputs=r_out)
        
    with gr.Tab("🔐 Login"):
        l_email = gr.Textbox(label="Email")
        l_pass = gr.Textbox(label="Password", type="password")
        l_out = gr.Textbox(label="Status")
        def handle_login(email, pw):
            token = login(email, pw)
            if token:
                return "✅ Login successful", token
            else:
                return "❌ Login failed", None
        gr.Button("Login").click(handle_login,
            inputs=[l_email, l_pass],
            outputs=[l_out, state])

    with gr.Tab("🏠 Member Dashboard"):
        m_product = gr.Textbox(label="Product Name")
        m_cost = gr.Number(label="Token Cost", precision=0)
        m_out = gr.Textbox(label="Status")
        def member_add(name, cost, token):
            decoded = decode_token(token)
            if not decoded or decoded["role"] != "member":
                return "❌ Unauthorized"
            return add_product(name, cost, decoded["email"])
        gr.Button("Add Product").click(member_add,
            inputs=[m_product, m_cost, state],
            outputs=m_out)

    with gr.Tab("🛍️ Browse & Buy Meals"):
        b_output = gr.Textbox(label="Available Meals", lines=8)
        b_id = gr.Number(label="Product ID to Buy")
        b_msg = gr.Textbox(label="Result")
        def buy(pid, token):
            decoded = decode_token(token)
            if not decoded or decoded["role"] != "beneficiary":
                return "❌ Unauthorized"
            return spend_tokens(decoded["email"], int(pid))
        gr.Button("View Meals").click(list_products, outputs=b_output)
        gr.Button("Buy with Token").click(buy, inputs=[b_id, state], outputs=b_msg)

    with gr.Tab("💰 Token Balance"):
        t_out = gr.Textbox(label="Balance")
        def show_balance(token):
            decoded = decode_token(token)
            if not decoded:
                return "❌ Invalid token"
            return get_token_balance(decoded["email"])
        gr.Button("Check My Balance").click(show_balance, inputs=state, outputs=t_out)

app.launch()