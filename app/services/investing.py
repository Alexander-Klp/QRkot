from datetime import datetime

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def investing_in_project(
    session: AsyncSession,
):
    result_projects = await session.execute(
        select(CharityProject).where(
            CharityProject.fully_invested.is_(False)
        ).order_by(asc(CharityProject.create_date))
    )
    projects = result_projects.scalars().all()
    result_donations = await session.execute(
        select(Donation).where(
            Donation.fully_invested.is_(False)
        ).order_by(asc(Donation.create_date))
    )
    donations = result_donations.scalars().all()
    for donation in donations:
        for project in projects:
            remaining_donation = (
                donation.full_amount - donation.invested_amount
            )
            remaining_project = (
                project.full_amount - project.invested_amount
            )
            if remaining_donation == 0:
                break
            amount_to_invest = min(remaining_donation, remaining_project)
            donation.invested_amount += amount_to_invest
            project.invested_amount += amount_to_invest

            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
            session.add(donation)
            session.add(project)
        await session.commit()
        for donation in donations:
            await session.refresh(donation)
        for project in projects:
            await session.refresh(project)
