from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_closed_or_invested(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = (
        await charity_project_crud.get_closed_or_invested_project(
            project_id, session
        )
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('Нельзя удалить закрытый проект '
                    'или с внесенными пожертвованиями!'),
        )


async def check_fully_invested(
    project_id: int,
    session: AsyncSession,
) -> None:
    project = (
        await charity_project_crud.get_fully_invested_project(
            project_id, session
        )
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя изменить проект с внесенными пожертвованиями!',
        )


async def check_full_amount_smaller_already_invested(
    obj_in: CharityProjectUpdate,
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    if obj_in.full_amount is not None and (
        obj_in.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую сумму меньше уже внесённой!'
        )
