from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Publicacao(models.Model):
    data_criacao = models.DateTimeField(auto_now_add=True)
    conteudo = models.CharField(max_length=280, blank=True, default='')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets", null=True)

    class Meta:
        ordering = ['data_criacao'] 

    def __str__(self):
        return self.conteudo