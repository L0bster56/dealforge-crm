from enum import StrEnum

class FieldType(StrEnum):
    text = "text"
    number = "number"
    datetime = "datetime"
    select_one = "select_one"
    select_many = "select_many"
    boolean = "boolean"