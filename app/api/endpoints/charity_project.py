from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import (
    check_charity_project_closed_or_invested,
    check_charity_project_exists,
    check_full_amount_smaller_already_invested,
    check_fully_invested,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import investing_in_project


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    """
    if charity_project.name is not None:
        await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(
        charity_project, session
    )
    await investing_in_project(session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Нельзя изменить полностью инвестированный проект
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_full_amount_smaller_already_invested(
        obj_in,
        charity_project,
        session
    )
    await check_fully_invested(project_id, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    if charity_project.full_amount == charity_project.invested_amount:
        await charity_project_crud.invested_project_close(
            charity_project, session
        )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Нельзя удалить полностью инвестированный или закрытый проект.
    """
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_closed_or_invested(project_id, session)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
