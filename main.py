from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd

csv = 'data.csv'
df = pd.read_csv(csv)

router = APIRouter(
    tags = ["users list"]
)
templates = Jinja2Templates(directory="templates")



@router.get("/")
def get_users_list(request: Request):
    list_of_users = df.groupby('DstIP').sum()[['Pkts', 'Octets']].sort_values(by='Octets', ascending=False)  # список пользователей c + общий pkts и oktets для каждого
    list_of_users['Octets'] = list_of_users['Octets'].apply(lambda x: round(x, 2))
    list_of_users = list_of_users.reset_index().to_dict('records')
    # return list_of_users
    return templates.TemplateResponse("base.html", {"request": request, "list_of_users": list_of_users})


@router.get("/{user_addres}")
def get_users_list(user_addres):
    user_info = df.to_dict('records')
    return [user for user in user_info if user.get("DstIP") == user_addres]



app = FastAPI(
    title="Netflow Analiser"
)

app.mount("/css", StaticFiles(directory="templates/css"), name="css")

app.include_router(router)