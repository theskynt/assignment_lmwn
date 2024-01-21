import os
import uvicorn
from fastapi import FastAPI, Path, Query
from fastapi_sqlalchemy import DBSessionMiddleware, db
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine
from dotenv import load_dotenv
from models import Users
from models import Restaurants
from typing import Optional
from geopy.distance import geodesic

load_dotenv(".env")
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/recommend/{user_id}")
async def recommend_restaurants(
    user_id: str = Path(..., description="User's ID"),
    latitude: float = Query(..., description="User's latitude"),
    longitude: float = Query(..., description="User's longitude"),
    size: int = Query(20, description="Number of recommended restaurants", ge=1),
    sort_dis: Optional[float] = Query(0, description="Flag to sort restaurants by displacement", ge=0.0, le=1.0),
    max_dis: Optional[float] = Query(5000, description="Max geodesic displacement in meters", ge=1)
    ):

    users_data = db.session.query(Users).filter_by(user_id=user_id).all()
    users_df = pd.DataFrame({
        'user_id': [user.user_id for user in users_data],
        **{f'feature_{i}': [getattr(feature, f'feature_{i}') for feature in users_data] for i in range(1000)}
    })

    restaurant_df = pd.DataFrame([{'restaurant_id': r.restaurant_id, 'latitude': r.latitude, 'longitude': r.longitude} for r in db.session.query(Restaurants).all()])

    with open("model.pkl", "rb") as f:
        model: NearestNeighbors = pickle.load(f)

    difference, ind = model.kneighbors(users_df.drop(columns="user_id"), n_neighbors=size)

    recommend_df = restaurant_df.loc[ind[0]]
    recommend_df["difference"] = difference[0]

    restaurant_list = [
        {
            "id": restaurant_id,
            "difference": recommend_df["difference"].iloc[i],
            "displacement": (geodesic((latitude, longitude), (float(restaurant_df[restaurant_df["restaurant_id"] == restaurant_id]["latitude"]), float(restaurant_df[restaurant_df["restaurant_id"] == restaurant_id]["longitude"]))).kilometers)* 1000
        }
        for i, restaurant_id in enumerate(recommend_df["restaurant_id"])
        if (geodesic((latitude, longitude), (float(restaurant_df[restaurant_df["restaurant_id"] == restaurant_id]["latitude"]), float(restaurant_df[restaurant_df["restaurant_id"] == restaurant_id]["longitude"]))).kilometers)* 1000 <= max_dis
    ]

    if sort_dis == 1.00:
        restaurant_list = sorted(restaurant_list, key=lambda x: x["displacement"])

    return {"restaurants": restaurant_list}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)