from django.db import models

class ClientArea(models.Model):
    class Meta:
        managed = False
        db_table = 'tb_area'

    city = models.CharField(max_length=32)
    district = models.CharField(max_length=32)
    province = models.CharField(max_length=32)
    address = models.CharField(max_length=128)

    def __unicode__(self):
        return self.address



class Client(models.Model):
    class Meta:
        managed = False
        db_table = 'user'

    phone = models.CharField(max_length=16)
    area_id = models.IntegerField()
    nick_name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.phone
