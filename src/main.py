from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

csv = 'data.csv'
df = pd.read_csv(csv)

router = APIRouter(
    tags = ["users list"]
)
templates = Jinja2Templates(directory="templates")



@router.get("/user")
def get_users_list(request: Request):
    list_of_users = df.groupby('DstIP').sum()[['Pkts', 'Octets']].sort_values(by='Octets', ascending=False)  # список пользователей c + общий pkts и oktets для каждого
    list_of_users['Octets'] = list_of_users['Octets'].apply(lambda x: round(x, 2))
    list_of_users = list_of_users.reset_index().to_dict('records')
    return list_of_users
    # return templates.TemplateResponse("base.html", {"request": request, "list_of_users": list_of_users})


@router.get("/user/{user_addres}")
def get_users_list(user_addres):
    user_info = df.to_dict('records')
    return [user for user in user_info if user.get("DstIP") == user_addres]



app = FastAPI(
    title="Netflow Analiser"
)

origins = [
    "http://localhost.tiangolo.com/",
    "https://localhost.tiangolo.com/",
    "http://localhost/",
    "http://localhost:8000/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)

app.mount("/css", StaticFiles(directory="templates/css"), name="css")

app.include_router(router)