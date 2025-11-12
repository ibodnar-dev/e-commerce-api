from app.external.exceptions import InfraException


class RepositoryException(InfraException):
    """Base repository exception."""


class DatabaseException(RepositoryException):
    """Raised when a database operation fails."""
