"""
This file is used to migrate database tables to the database.
"""
import Project.Models


def migrate():
    """
    Run database migrations for the defined models.
    :return:
    """
    models_pieces = [
        'BareField', 'BigIntegerField', 'BinaryField', 'BlobField',
        'BooleanField', 'CharField', 'Check', 'Clause', 'CompositeKey',
        'DQ', 'DataError', 'DatabaseError', 'DateField', 'DateTimeField',
        'DecimalField', 'DeferredRelation', 'DoesNotExist', 'DoubleField',
        'Field', 'FixedCharField', 'FloatField', 'ForeignKeyField',
        'ImproperlyConfigured', 'IntegerField', 'IntegrityError',
        'InterfaceError', 'InternalError', 'JOIN', 'JOIN_FULL',
        'JOIN_INNER', 'JOIN_LEFT_OUTER', 'Model', 'MySQLDatabase',
        'NotSupportedError', 'OperationalError', 'Param',
        'PostgresqlDatabase', 'PrimaryKeyField', 'ProgrammingError',
        'Proxy', 'R', 'SQL', 'SqliteDatabase', 'TextField', 'TimeField',
        'UUIDField', 'Using', 'Window', '__builtins__', '__doc__',
        '__file__', '__name__', '__package__', 'datetime', 'db', 'fn',
        'prefetch'
    ]

    migrations = list(set(dir(Project.Models)) - set(models_pieces))
    migrations.remove('BaseModel')

    # Grab the actual class object for the model.
    migrations = [getattr(Project.Models, klass) for klass in migrations]
    # Make sure we didn't pick up stragglers.
    migrations = [c for c in migrations if 'class' in str(c)]

    db = Project.Models.db
    db.connect()
    try:
        db.drop_tables(migrations)
    except:
        pass
    db.create_tables(migrations)
    db.close()

if __name__ == '__main__':
    migrate()
