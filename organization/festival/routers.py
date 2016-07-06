
class FestivalRouter(object):
    """
    A router to control all database operations on models in festival
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'festival':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'festival':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'festival' or \
           obj2._meta.app_label == 'festival':
           return True
        return None

    # def allow_migrate(self, db, app_label, model=None, **hints):
    #     if app_label == 'festival':
    #         return db == 'default'
    #     return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if 'target_db' in hints:
            return db == hints['target_db']
        return True
