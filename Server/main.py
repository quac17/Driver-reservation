from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from database import engine, Base
from routers import user, authen, mentor, car, reserve

# Tạo database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Drive Coach Reservation API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các origin
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, DELETE, ...)
    allow_headers=["*"],  # Cho phép tất cả các header
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Drive Coach Reservation API"}

# Include user router
app.include_router(user.router, prefix="/user", tags=["user"])

# Include authen router
app.include_router(authen.router, prefix="/authen", tags=["authen"])

# Include mentor router
app.include_router(mentor.router, prefix="/mentor", tags=["mentor"])

# Include car router
app.include_router(car.router, prefix="/car", tags=["car"])

# Include reserve router
app.include_router(reserve.router, prefix="/reserve", tags=["reserve"])

# Serve static files
app.mount("/public", StaticFiles(directory="public"), name="public")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
