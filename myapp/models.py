from django.db import models

class booked(models.Model):

    namedata=models.CharField(max_length=200)
    zonedata=models.TextField()
    numberdata=models.IntegerField()
    previous=models.OneToOneField('self', null=True,on_delete=models.SET_NULL, blank=True, related_name="next")

    def str(self):
        return self.namedata+ ',' + self.zonedata + ',' +str(self.numberdata)
