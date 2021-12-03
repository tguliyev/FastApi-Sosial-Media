from fastapi import FastAPI
from routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins =[
    "https://www.google.com"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Index page
@app.get('/')
def root():
    return {'message': 'Hello Turals Great Futuree!!!'}
