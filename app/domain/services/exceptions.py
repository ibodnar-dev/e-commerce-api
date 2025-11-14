from app.domain.exceptions import DomainException


class ServiceException(DomainException):
    """Base services exception."""
