from django.db import models

# Create your models here.
from django.db import models


class Profissional(models.Model):
    id_profissional = models.IntegerField(primary_key=True)
    nome_completo = models.CharField(max_length=100, default='', blank=False) # Nome completo do Profissional
    nome_social = models.CharField(max_length=100, default='', blank=True)    # Nome Social do Profissional (pode ser vazio)
    profissao = models.CharField(max_length=45, default='', blank=False)      # Profissão do Profissional
    endereco = models.CharField(max_length=255, default='', blank=False)      # Endereço do Profissional

    def __str__(self):
        return self.nome_completo


class Contato(models.Model):
    id_contato = models.AutoField(primary_key=True)                           # Identificador Único do contato  
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)  # Relacionamento com Profissional.id_profissional
    tipo = models.CharField(max_length=15)                                    # Tipo de Contato (email, telefone...)
    contato = models.CharField(max_length=45)                                 # Contato do Profissional (pode ser telefone ou email)
    
    class Meta:
        unique_together = ('profissional', 'contato')

    def __str__(self):
        return f"{self.profissional.nome_completo} - {self.contato}"


class Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True)                          # Identificador Único da consulta  
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)  # Relacionamento com Profissional.id_profissional                             # Definir o tipo de contato, como email, telefone...
    data_consulta = models.DateTimeField()                                    # Data da Consulta
    
    class Meta:
        unique_together = ('profissional', 'data_consulta')
    
    def __str__(self):
        return f"Consulta de {self.profissional.nome_completo} em {self.data_consulta}"
