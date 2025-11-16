from typing import Optional, List

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.milestone import Milestone


class MilestoneService:
    """Service for managing Milestone records in the database.

    All methods are async and expect an `AsyncSession` (from `src.core.depends.db.get_async_session`)
    so they can be used easily from FastAPI endpoints with `Depends`.
    """

    @staticmethod
    async def get_by_id(milestone_id: int, session: AsyncSession) -> Optional[Milestone]:
        """Return a Milestone by its numeric primary key `id` or None."""
        stmt = select(Milestone).where(Milestone.id == milestone_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_by_project(project_id: int, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Milestone]:
        """Return all milestones for a specific project with pagination."""
        stmt = select(Milestone).where(Milestone.project_id == project_id).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def list_all(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Milestone]:
        """Return a paginated list of all milestones."""
        stmt = select(Milestone).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create(milestone_data: dict, session: AsyncSession) -> Milestone:
        """Create a new milestone.
        
        Args:
            milestone_data: Dictionary with keys like name, description, amount, project_id
            session: AsyncSession for database operations
            
        Returns:
            The created Milestone instance
        """
        new_milestone = Milestone(**milestone_data)
        session.add(new_milestone)
        await session.commit()
        await session.refresh(new_milestone)
        return new_milestone

    @staticmethod
    async def update(milestone_id: int, milestone_data: dict, session: AsyncSession) -> Optional[Milestone]:
        """Update an existing milestone.
        
        Args:
            milestone_id: Primary key of the milestone to update
            milestone_data: Dictionary with fields to update
            session: AsyncSession for database operations
            
        Returns:
            The updated Milestone instance or None if not found
        """
        milestone = await MilestoneService.get_by_id(milestone_id, session)
        if not milestone:
            return None
        
        for key, value in milestone_data.items():
            if value is not None:
                setattr(milestone, key, value)
        
        await session.commit()
        await session.refresh(milestone)
        return milestone

    @staticmethod
    async def delete(milestone_id: int, session: AsyncSession) -> bool:
        """Delete a milestone by its primary key.
        
        Args:
            milestone_id: Primary key of the milestone to delete
            session: AsyncSession for database operations
            
        Returns:
            True if deleted, False if milestone not found
        """
        milestone = await MilestoneService.get_by_id(milestone_id, session)
        if not milestone:
            return False
        
        await session.delete(milestone)
        await session.commit()
        return True
