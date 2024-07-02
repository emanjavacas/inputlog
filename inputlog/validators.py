
class InvalidColumnsException(Exception):
    pass


def validate_columns(df, columns):
    if columns is not None and sorted(list(df.keys())) != sorted(list(columns)):
        raise InvalidColumnsException(
            {"message": "Invalid input cols", 
             "data": {"received": columns, "expected": list(df.keys())}})
    return True
