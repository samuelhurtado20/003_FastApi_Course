from datetime import datetime
import time
from fastapi import FastAPI, Request
from zoneinfo import ZoneInfo
from app.routes import customer, transaction, plan
from app.db.db2 import create_all_tables
from fastapi_pagination import add_pagination


app = FastAPI(lifespan=create_all_tables)

app.include_router(prefix="/api/v1", router=customer.router, tags=["customer"])
app.include_router(prefix="/api/v1", router=transaction.router, tags=["transaction"])
app.include_router(prefix="/api/v1", router=plan.router, tags=["plan"])
add_pagination(app)


@app.middleware("http") 
async def log_request_headers(request: Request, call_next):    
    start = time.time()
    print("Request Headers:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")
    response = await call_next(request)
    process_time = time.time() - start
    print(f"Request processed in {process_time:.4f} seconds for {request.url.path}")
    print(f"Request: {request.url} headers: {dict(request.headers)}")
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/datetime")
async def datetime_now():
    return {"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


country_timezones = {
  "US": "America/New_York",
  "UK": "Europe/London",
  "DE": "Europe/Berlin",
  "FR": "Europe/Paris",
  "JP": "Asia/Tokyo",
  "CO": "America/Bogota",
  "BR": "America/Sao_Paulo",
  "AR": "America/Argentina/Buenos_Aires",
  "MX": "America/Mexico_City",
}

time_formats = {
    '24': '%B %d %Y %H:%m:%S',
    '12': '%B %d %Y %I:%m:%S'
}

@app.get('/time/{iso_code}/{time_format}')
async def get_time(iso_code: str, time_format: str = '24'):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    time_formatstr = time_formats.get(time_format)
    tz = ZoneInfo(key=timezone_str)
    if (time_format == '24'):
        return {'time': datetime.now(tz).strftime(time_formatstr)}
    elif (time_format == '12'):
        return {'time': datetime.now(tz).strftime(time_formatstr)}
    else: 
        return {'Error': 'Invalid Format'}



# python3 -m venv venv curso_fastapi

# source venv/bin/activate

# pip install "fastapi[standard]"

# uvicorn main:app --reload

# mkdir curso-fast-api-project
# cd curso-fast-api-project

# source ../venv/bin/activate

# sqlite3 db.sqlite3
# .tables


# Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse -Force
# Remove-Item -Recurse -Force .\**\__pycache__\
# Get-ChildItem -Recurse -Directory -Filter models | Select-Object FullName

# pip install fastapi-pagination
# pip install zoneinfo
# pip install "fastapi[all]"
# pip install sqlalchemy==1.4.46
# pip install databases[sqlite]
# pip show databases