from fastapi import FastAPI, HTTPException
from models import User, Order

app = FastAPI()

# In-memory storage
users_db = {}
orders_db = {}

user_id_counter = 1
order_id_counter = 1


@app.get("/")
def health_check():
    return {"status": "API is running"}


# ---------------- USERS ----------------

@app.post("/users", status_code=201)
def create_user(user: User):
    global user_id_counter

    for existing_user in users_db.values():
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    user.id = user_id_counter
    users_db[user_id_counter] = user.dict()
    user_id_counter += 1
    return user


@app.get("/users")
def get_all_users():
    return list(users_db.values())


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}


# ---------------- ORDERS ----------------

@app.post("/orders", status_code=201)
def create_order(order: Order):
    global order_id_counter

    if order.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User does not exist")

    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

    order.order_id = order_id_counter
    orders_db[order_id_counter] = order.dict()
    order_id_counter += 1
    return order


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]
