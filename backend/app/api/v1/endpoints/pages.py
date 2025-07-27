# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from app.main import templates  # or import your templates instance

# router = APIRouter()

# @router.get("/about", response_class=HTMLResponse)
# async def about(request: Request):
#     return templates.TemplateResponse("about.html", {"request": request})

# @router.get("/contact", response_class=HTMLResponse)
# async def contact(request: Request):
#     return templates.TemplateResponse("contact.html", {"request": request})

# @router.get("/articles", response_class=HTMLResponse)
# async def articles(request: Request):
#     return templates.TemplateResponse("articles.html", {"request": request})