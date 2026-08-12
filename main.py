from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from auth import hash_password, verify_password
from database.session import create_db_and_tables, get_session
from models.product import Product
from models.user import User


app = FastAPI(
    title="Product API",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "Product API is running"
    }


# =========================
# AUTHENTICATION
# =========================

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: dict,
    session: Session = Depends(get_session),
):
    username = user_data.get("username")
    email = user_data.get("email")
    password = user_data.get("password")
    full_name = user_data.get("full_name")

    if not username or not email or not password or not full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All fields are required",
        )

    existing_user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
    }


@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "access_token": f"test-token-{user.username}",
        "token_type": "bearer",
    }


# =========================
# PRODUCTS
# =========================

@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: Product,
    session: Session = Depends(get_session),
):
    session.add(product)
    session.commit()
    session.refresh(product)

    return product


@app.get(
    "/products",
    response_model=List[Product],
)
def list_products(
    session: Session = Depends(get_session),
):
    products = session.exec(
        select(Product)
    ).all()

    return products


@app.get(
    "/products/{product_id}",
    response_model=Product,
)
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@app.patch(
    "/products/{product_id}",
    response_model=Product,
)
def update_product(
    product_id: int,
    product_data: Product,
    session: Session = Depends(get_session),
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock

    session.add(product)
    session.commit()
    session.refresh(product)

    return product


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    session.delete(product)
    session.commit()

    return None