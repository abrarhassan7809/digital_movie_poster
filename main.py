import os
from typing import List
from fastapi import FastAPI, UploadFile, File, status, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import uvicorn
from starlette.requests import Request
from starlette.responses import RedirectResponse

from gallery_backend import get_all_groups

IMAGEDIR = 'static'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def gallery(request: Request):
    result = []
    if os.listdir(IMAGEDIR):
        for file_name in os.listdir(IMAGEDIR):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                file_path = f"/static/{file_name}"
                result.append(file_path)

    groups = get_all_groups(IMAGEDIR)
    return templates.TemplateResponse("index_images.html", {"request": request, "result": result, "groups": groups})


@app.post('/upload_files/')
async def upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()

        # save the file
        file_path = os.path.join(IMAGEDIR, file.filename)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(contents)

        else:
            pass

    redirect_url = app.url_path_for('gallery')
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/create_group/")
async def create_group(request: Request):
    result = []
    if os.listdir(IMAGEDIR):
        for file_name in os.listdir(IMAGEDIR):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                file_path = f"/static/{file_name}"
                result.append(file_path)

    groups = get_all_groups(IMAGEDIR)
    return templates.TemplateResponse("create_group.html", {"request": request, "result": result, "groups": groups})


@app.post("/create_group/")
async def process_create_group(group_name: str = Form(...), select_images: List[str] = Form(...)):
    group_dir = os.path.join(IMAGEDIR, group_name)
    if not os.path.exists(group_dir):
        os.makedirs(group_dir, exist_ok=True)

    for image_path in select_images:
        image_name = os.path.basename(image_path)
        src_path = os.path.join(IMAGEDIR, image_name)
        dest_path = os.path.join(group_dir, image_name)
        if os.path.exists(src_path):
            shutil.move(src_path, dest_path)

        else:
            pass

    redirect_url = app.url_path_for('gallery')
    return RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)


@app.get('/group_list/')
async def group_list(request: Request):
    groups = get_all_groups(IMAGEDIR)
    return templates.TemplateResponse("group_list.html", {"request": request, "groups": groups})


@app.get('/group/{group_name}/')
async def show_group_images(request: Request, group_name: str):
    group_dir = os.path.join(IMAGEDIR, group_name)
    result = []
    if os.path.exists(group_dir):
        for file_name in os.listdir(group_dir):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                file_path = f"/static/{group_name}/{file_name}"
                result.append(file_path)

    return templates.TemplateResponse("group_images.html", {"request": request, "group_name": group_name, "result": result})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
