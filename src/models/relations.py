"""
Define relationships after all models are imported to avoid circular reference issues.
This module should be imported AFTER all models are defined in __init__.py.
"""

# Relationships are now defined directly in the model files using
# sa_relationship_kwargs to avoid circular import issues.
# This file is kept for future relationship configuration if needed.
