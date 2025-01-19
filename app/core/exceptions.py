from fastapi import HTTPException

def raise_not_found_error(entity: str):
    """
    Поднимает исключение с ошибкой 404 для сущностей.
    :param entity: Название сущности.
    """
    raise HTTPException(status_code=404, detail=f"{entity} не найдено")
