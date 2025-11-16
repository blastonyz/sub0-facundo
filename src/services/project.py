from typing import Optional, List

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session as SQLAlchemySession

from src.models.project import Project


class ProjectService:
    """Service for managing Project records in the database.

    All methods are async and expect an `AsyncSession` (from `src.core.depends.db.get_async_session`)
    so they can be used easily from FastAPI endpoints with `Depends`.
    """

    @staticmethod
    async def get_by_project_id(project_id: str, session: AsyncSession) -> Optional[Project]:
        """Return a Project matching the given `project_id` (string) or None."""
        stmt = select(Project).where(Project.project_id == project_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(pk: int, session: AsyncSession) -> Optional[Project]:
        """Return a Project by its numeric primary key `id` or None."""
        stmt = select(Project).where(Project.id == pk)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def list_all(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Project]:
        """Return a paginated list of all projects."""
        stmt = select(Project).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create(project_data: dict, session: AsyncSession) -> Project:
        """Create a new project.
        
        Args:
            project_data: Dictionary with keys like name, repo, description, budget, project_id
            session: AsyncSession for database operations
            
        Returns:
            The created Project instance
        """
        new_project = Project(**project_data)
        session.add(new_project)
        await session.commit()
        await session.refresh(new_project)
        return new_project

    @staticmethod
    async def update(project_id: int, project_data: dict, session: AsyncSession) -> Optional[Project]:
        """Update an existing project.
        
        Args:
            project_id: Primary key of the project to update
            project_data: Dictionary with fields to update
            session: AsyncSession for database operations
            
        Returns:
            The updated Project instance or None if not found
        """
        project = await ProjectService.get_by_id(project_id, session)
        if not project:
            return None
        
        for key, value in project_data.items():
            if value is not None:
                setattr(project, key, value)
        
        await session.commit()
        await session.refresh(project)
        return project

    @staticmethod
    async def delete(project_id: int, session: AsyncSession) -> bool:
        """Delete a project by its primary key.
        
        Args:
            project_id: Primary key of the project to delete
            session: AsyncSession for database operations
            
        Returns:
            True if deleted, False if project not found
        """
        project = await ProjectService.get_by_id(project_id, session)
        if not project:
            return False
        
        await session.delete(project)
        await session.commit()
        return True

