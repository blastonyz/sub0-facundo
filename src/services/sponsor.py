from typing import Optional, List

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.sponsor import SponsoredProject


class SponsoredProjectService:
    """Service for managing SponsoredProject records in the database.

    All methods are async and expect an `AsyncSession` (from `src.core.depends.db.get_async_session`)
    so they can be used easily from FastAPI endpoints with `Depends`.
    """

    @staticmethod
    async def get_by_id(sponsored_project_id: int, session: AsyncSession) -> Optional[SponsoredProject]:
        """Return a SponsoredProject by its numeric primary key `id` or None."""
        stmt = select(SponsoredProject).where(SponsoredProject.id == sponsored_project_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_project_id(project_id: str, session: AsyncSession) -> Optional[SponsoredProject]:
        """Return a SponsoredProject matching the given `project_id` (string) or None."""
        stmt = select(SponsoredProject).where(SponsoredProject.project_id == project_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_all(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[SponsoredProject]:
        """Return a paginated list of all sponsored projects."""
        stmt = select(SponsoredProject).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def list_by_status(status: str, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[SponsoredProject]:
        """Return all sponsored projects with a specific status with pagination."""
        stmt = select(SponsoredProject).where(SponsoredProject.status == status).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create(sponsored_project_data: dict, session: AsyncSession) -> SponsoredProject:
        """Create a new sponsored project.
        
        Args:
            sponsored_project_data: Dictionary with keys like project_id, name, repo, ai_score, status, etc.
            session: AsyncSession for database operations
            
        Returns:
            The created SponsoredProject instance
        """
        new_sponsored_project = SponsoredProject(**sponsored_project_data)
        session.add(new_sponsored_project)
        await session.commit()
        await session.refresh(new_sponsored_project)
        return new_sponsored_project

    @staticmethod
    async def update(sponsored_project_id: int, sponsored_project_data: dict, session: AsyncSession) -> Optional[SponsoredProject]:
        """Update an existing sponsored project.
        
        Args:
            sponsored_project_id: Primary key of the sponsored project to update
            sponsored_project_data: Dictionary with fields to update
            session: AsyncSession for database operations
            
        Returns:
            The updated SponsoredProject instance or None if not found
        """
        sponsored_project = await SponsoredProjectService.get_by_id(sponsored_project_id, session)
        if not sponsored_project:
            return None
        
        for key, value in sponsored_project_data.items():
            if value is not None:
                setattr(sponsored_project, key, value)
        
        await session.commit()
        await session.refresh(sponsored_project)
        return sponsored_project

    @staticmethod
    async def delete(sponsored_project_id: int, session: AsyncSession) -> bool:
        """Delete a sponsored project by its primary key.
        
        Args:
            sponsored_project_id: Primary key of the sponsored project to delete
            session: AsyncSession for database operations
            
        Returns:
            True if deleted, False if sponsored project not found
        """
        sponsored_project = await SponsoredProjectService.get_by_id(sponsored_project_id, session)
        if not sponsored_project:
            return False
        
        await session.delete(sponsored_project)
        await session.commit()
        return True
