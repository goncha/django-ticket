# -*- coding: utf-8 -*-

class MultiDBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'ticket':
            if model._meta.db_table == 'tb_area':
                return 'apas'
            elif model._meta.db_table == 'user':
                return 'luhu'
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, model):
        return True


# Local Variables: **
# comment-column: 56 **
# indent-tabs-mode: nil **
# python-indent: 4 **
# End: **
