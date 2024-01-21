from locust import HttpUser, task
import pandas as pd

class MyUser(HttpUser):

    @task
    def recommend_restaurants(self):
        request_df = pd.read_parquet("request.parquet")

        user_request = request_df.sample().squeeze()
        user_id = user_request["user_id"]
        
        sort_dis = user_request["sort_dis"]
        if pd.isna(sort_dis):
            sort_dis = None

        max_dis = user_request["max_dis"]
        if pd.isna(max_dis):
            max_dis = None

        params = {
            "latitude": user_request["latitude"],
            "longitude": user_request["longitude"],
            "size": user_request["size"],
            "sort_dis": sort_dis,
            "max_dis": max_dis
        }

        response = self.client.get(f"/recommend/{user_id}", params=params)
        assert response.status_code == 200, f"Unexpected response code: {response.status_code}"
