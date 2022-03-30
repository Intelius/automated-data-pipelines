# File to store all of the general HTTP exceptions that can be raised by the endpoints

from fastapi import HTTPException, status


notFound_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="No information can be found with the provided parameters",
)