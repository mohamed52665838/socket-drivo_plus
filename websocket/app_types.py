
from enum import StrEnum
from dataclasses import dataclass



@dataclass
class NotificationBody:
    category: str
    user_id: str
    token: str


    def __post__init__(self):
        if self.token is None or self.category is None or self.user_id is None:
            raise ValueError("Missing Attribute: One or more requried attributes missing")

        if not (isinstance( self.token, str) and isinstance( self.category, str ) and isinstance( self.user_id, str )):
            raise ValueError("Type Erro: All Atributes of type str")

class Categories(StrEnum):
    MENTAL_ALERT = 'mental_alert'
    PHYSICAL_ALERT = 'physical_alert'
    DISTRACTION_ALERT = 'distraction_alert'

