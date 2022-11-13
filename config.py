from pydantic import BaseSettings


class Settings(BaseSettings):
    FRONTEND_URL = "http://localhost:3000"
    left = 100.3
    right = 101.0
    top = 14.0
    bottom = 13.4
    GRID_WIDTH = [0.01, 0.005, 0.0025, 0.001, 0.0005]
    BIG_GRID_WIDTH = [0.1, 0.05, 0.025, 0.01, 0.005]
    BIG_GRID_HALF_WIDTH = [0.05, 0.025, 0.0125, 0.005, 0.0025]
    GRID_LEVEL = [12, 13, 14, 15, 16]
    REDIS_URL = "172.28.1.4"
    REDIS_PORT = 6379
    REDIS_AUTH = "p@ssw0rd"

    class Config:
        env_file = ".env"


config = Settings()
