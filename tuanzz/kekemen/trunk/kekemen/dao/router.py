class productRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'product':
            return 'db_product'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'product':
            return 'db_product'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'product' and obj2._meta.app_label == 'product':
            return True
        return None

    def allow_syncdb(self, db, model):
        if db == 'db_product':
            return model._meta.app_label == 'product'
        return None
