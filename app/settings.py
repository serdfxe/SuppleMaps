from environs import Env

env = Env()

env.read_env('.env')

DATABASE_URL = env("DATABASE_URL")
