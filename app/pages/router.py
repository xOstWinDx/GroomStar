from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.services.router import get_services

router = APIRouter(prefix="/pages", tags=["Pages"])


templates = Jinja2Templates(directory="app/templates")


@router.get("/services", response_class=HTMLResponse)
async def services_page(request: Request, services=Depends(get_services)):
    services = [service["Service"] for service in services]
    return templates.TemplateResponse(
        request=request, name="services.html", context={"services": services}
    )
