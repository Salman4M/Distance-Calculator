from django.db import models

# Create your models here.




class Location(models.Model):
    name=models.CharField(max_length=300)
    code=models.CharField(max_length=10,blank=True,null=True) #there are codes of airports so we can use them. Usually length of code is 3
    latitude=models.FloatField()
    longitude=models.FloatField()
    is_airport=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}--({self.code})" if self.code else self.name
    


MODE_CHOICES=(
    ('plane','plane'),
    ('car','car'),
)

class Trip(models.Model):
    user=models.ForeignKey('auth.User',on_delete=models.CASCADE,null=True,blank=True)
    origin =models.ForeignKey(Location,on_delete=models.CASCADE,related_name='trip_origin')
    destination=models.ForeignKey(Location,on_delete=models.CASCADE,related_name='trip_destination')
    mode=models.CharField(max_length=10,choices=MODE_CHOICES,default='car')
    distance_km=models.FloatField()
    cost=models.FloatField()
    travel_time=models.CharField(max_length=300)
    weather_at_destination=models.CharField(max_length=300,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin}-> {self.destination} ({self.mode})"
    
    

