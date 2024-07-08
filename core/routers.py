class ReadOnlyRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "news":
            return "mysql_db"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "news":
            return None
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "news" or obj2._meta.app_label == "news":
            return False
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default" and app_label != "news"
