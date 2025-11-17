from datetime import datetime
from fastapi import FastAPI
from zoneinfo import ZoneInfo
from routes import customer, plan
from db.db2 import create_all_tables



app = FastAPI(lifespan=create_all_tables)

app.include_router(prefix="/api/v1", router=customer.router, tags=["customer"])
app.include_router(prefix="/api/v1", router=plan.router, tags=["plan"])


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
async def time(iso_code: str, time_format: str = '24'):
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
