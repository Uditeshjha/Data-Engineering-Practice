import re
class MissingValueError(Exception):
    pass
def check_missing_values(record):
    for i,rows in enumerate(record,start=1):
        for key,value in rows.items():
            if value is None or value == "":
                raise MissingValueError(f"Missing value in row {i}, column '{key}'")


dataset = [
    {"name": "Udit", "age": 27},
    {"name": "Anand", "age": None},
    {"name": "Bhumit", "age": None},
    {"name": "", "age": None}
    ]
try:
    check_missing_values(dataset)
except MissingValueError as e:
    print("Data Error:", e)