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
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              email TEXT UNIQUE,
              password TEXT,
              role TEXT CHECK(role IN ('donor', 'beneficiary')),
              tokens INTEGER DEFAULT 10
              )
        """)
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            cost INTEGER,
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
    return f"Product '{name}' added!"

def list_products():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT id, name, cost, owner_email FROM products")
    items = c.fetchall()
    conn.close()
    return "\n".join([f"{id}. {name} - {cost} tokens (by {owner})" for id, name, cost, owner in items])

def spend_tokens(user_email, product_id):
    try:
        conn = sqlite3.connect("app.db")
        c = conn.cursor()

        # fetch product
        c.execute("SELECT name, cost FROM products WHERE id = ?", (product_id,))
        product = c.fetchone()
        if not product:
            conn.close()
            return "❌ Product not found"

        name, cost = product

        # fetch user balance
        c.execute("SELECT tokens FROM users WHERE email = ?", (user_email,))
        user = c.fetchone()
        if not user:
            conn.close()
            return "❌ User not found"

        current_tokens = user[0]
        if current_tokens < cost:
            conn.close()
            return f"❌ Not enough tokens (you have {current_tokens}, need {cost})"

        # update balance
        c.execute("UPDATE users SET tokens = tokens - ? WHERE email = ?", (cost, user_email))
        conn.commit()
        conn.close()

        return f"✅ You bought '{name}' for {cost} tokens"
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def get_token_balance(email):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("SELECT tokens FROM users WHERE email = ?", (email,))
    tokens = c.fetchone()
    conn.close()
    return f"You have {tokens[0]} tokens." if tokens else "User not found"

#interface
with gr.Blocks() as app:
    gr.Markdown("## Charity App - Gradio + SQLite + JWT")
    token_state = gr.State(value=None)
    role_state = gr.State(value=None)

    # ---------------- Register ----------------
    with gr.Tab("📝 Register") as register_tab:
        r_name = gr.Textbox(label="Name")
        r_email = gr.Textbox(label="Email")
        r_pass = gr.Textbox(label="Password", type="password")
        r_role = gr.Dropdown(["donor", "beneficiary"], label="Role")
        r_out = gr.Textbox(label="Status")

        def handle_register(name, email, pw, role):
            msg = register(name, email, pw, role)
            if msg.lower().startswith("registration"):
                tok = create_token(email, role)
                return f"✅ {msg}", tok, role
            return f"❌ {msg}", None, None

        gr.Button("Register").click(
            handle_register,
            inputs=[r_name, r_email, r_pass, r_role],
            outputs=[r_out, token_state, role_state],
        )

    # ---------------- Login ----------------
    with gr.Tab("🔐 Login") as login_tab:
        l_email = gr.Textbox(label="Email")
        l_pass = gr.Textbox(label="Password", type="password")
        l_out = gr.Textbox(label="Status")

        def handle_login(email, pw):
            tok = login(email, pw)
            if tok:
                dec = decode_token(tok)
                if dec:
                    return "✅ Login successful", tok, dec["role"]
            return "❌ Login failed", None, None

        gr.Button("Login").click(
            handle_login,
            inputs=[l_email, l_pass],
            outputs=[l_out, token_state, role_state],
        )


    # ---------------- Donor Dashboard ----------------
    with gr.Tab("🏠 Donor Dashboard", visible=False) as donor_tab:
        m_product = gr.Textbox(label="Product Name")
        m_cost = gr.Number(label="Token Cost", precision=0)
        m_out = gr.Textbox(label="Status")

        def donor_add(name, cost, tok):
            dec = decode_token(tok) if tok else None
            if not dec or dec["role"] != "donor":
                return "❌ Unauthorized"
            return add_product(name, int(cost), dec["email"])

        gr.Button("Add Product").click(
            donor_add, inputs=[m_product, m_cost, token_state], outputs=m_out
        )

    # ---------------- Beneficiary Dashboard ----------------
    with gr.Tab("🛍️ Browse & Buy Meals", visible=False) as beneficiary_tab:
        b_output = gr.Textbox(label="Available Meals", lines=8)
        b_id = gr.Number(label="Product ID to Buy")
        b_msg = gr.Textbox(label="Result")

        def buy(pid, tok):
            dec = decode_token(tok) if tok else None
            if not dec or dec["role"] != "beneficiary":
                return "❌ Unauthorized"
            if not pid:
                return "❌ Enter product ID"
            return spend_tokens(dec["email"], int(pid))

        gr.Button("View Meals").click(list_products, outputs=b_output)
        gr.Button("Buy with Token").click(buy, inputs=[b_id, token_state], outputs=b_msg)

        # ---------------- Logout ----------------
    with gr.Tab("🚪 Logout", visible=False) as logout_tab:
        l_msg = gr.Textbox(label="Status")

        def handle_logout():
            return None, None, "✅ Logged out", gr.update(visible=True), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

        gr.Button("Logout").click(
            handle_logout,
            outputs=[token_state, role_state, l_msg, register_tab, login_tab, donor_tab, beneficiary_tab, logout_tab]
        )


    # ---------------- Role-based redirection ----------------
    def show_tabs(role):
        return (
            gr.update(visible=(role == "donor")),
            gr.update(visible=(role == "beneficiary")),
        )

    role_state.change(
        show_tabs, inputs=role_state, outputs=[donor_tab, beneficiary_tab]
    )



app.launch()