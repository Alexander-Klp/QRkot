from datetime import datetime
from typing import Any, Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(
                CharityProject.id
            ).where(CharityProject.name == project_name)
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_fully_invested_project(
        self,
        project_id: int,
        session: AsyncSession
    ):
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id,
                CharityProject.fully_invested
            )
        )
        return project.scalars().first()

    async def get_closed_or_invested_project(
        self,
        project_id: int,
        session: AsyncSession
    ):
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id,
                or_(
                    CharityProject.fully_invested,
                    CharityProject.invested_amount > 0
                )
            )
        )
        return project.scalars().first()

    async def invested_project_close(
        self,
        charity_project,
        session: AsyncSession
    ):
        charity_project.fully_invested = True
        charity_project.close_date = datetime.now()
        await session.commit()
        await session.refresh(charity_project)

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[dict[str, Any]]:
        projects = await session.execute(
            select([
                CharityProject.name,
                (func.julianday(
                    CharityProject.close_date
                ) - func.julianday(
                    CharityProject.create_date
                )).label('investing_time'),
                CharityProject.description,
            ],
            ).where(
                CharityProject.fully_invested
            ).order_by('investing_time')
        )
        projects = projects.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
