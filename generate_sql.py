import os
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql

# Import all your SQLModel models here
from src.models.base_model import SQLModel
from src.models.project import Project
from src.models.milestone import Milestone
from src.models.sponsor import SponsoredProject

# Use SQLite in-memory database for initial reflection, but we'll compile to PostgreSQL
engine = create_engine("sqlite:///:memory:", poolclass=NullPool, echo=False)

print("--- SQL DDL for SQLModel Models (PostgreSQL syntax) ---\n")

# Generate CREATE TABLE statements for each table
for table in SQLModel.metadata.sorted_tables:
    # Compile the CREATE TABLE statement using PostgreSQL dialect
    create_table_stmt = CreateTable(table).compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True})
    print(f"-- Table: {table.name}")
    print(f"{create_table_stmt};\n")

print("--- End SQL DDL ---")


