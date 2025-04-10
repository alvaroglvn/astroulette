from typing import Union
from fastapi import HTTPException, status


class DatabaseError(HTTPException):
    def __init__(self, operation: str, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database {operation} failed: {detail}",
        )


class RecordNotFound(HTTPException):
    def __init__(self, model: str, record_id: Union[int, str]) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model} with id {record_id} not found.",
        )


class TableNotFound(HTTPException):
    def __init__(self, table_name: str) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Table '{table_name}' does not exist in the database.",
        )
