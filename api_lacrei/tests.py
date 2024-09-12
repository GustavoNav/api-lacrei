import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Profissional, Contato, Consulta

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def profissional_data():
    return {
        "id_profissional": 1,
        "nome_completo": "Dr. João Silva",
        "nome_social": "Dr. João",
        "profissao": "Médico",
        "endereco": "Rua 123, São Paulo"
    }

@pytest.fixture
def contato_data():
    return {
        "tipo": "email",
        "contato": "joao.silva@exemplo.com"
    }

@pytest.fixture
def consulta_data():
    return {
        "data_consulta": "2024-09-12T10:00:00Z"
    }

# Teste: Criar Profissional
@pytest.mark.django_db
def test_create_profissional(api_client, profissional_data):
    url = reverse('handle_request', args=['profissionais'])
    response = api_client.post(url, profissional_data, format='json')
    
    # Verificações
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id_profissional' in response.data

# Teste: Atualizar Profissional
@pytest.mark.django_db
def test_update_profissional(api_client, profissional_data):
    profissional = Profissional.objects.create(**profissional_data)
    
    url = reverse('handle_request', args=['profissionais'])
    update_data = {"id_profissional": profissional.id_profissional, "profissao": "Cardiologista"}
    
    response = api_client.put(url, update_data, format='json')
    
    # Verificações
    assert response.status_code == status.HTTP_200_OK
    assert response.data['profissao'] == "Cardiologista"

# Teste: Criar Contato
@pytest.mark.django_db
def test_create_contato(api_client, contato_data, profissional_data):
    profissional = Profissional.objects.create(**profissional_data)
    contato_data['profissional'] = profissional.id_profissional
    
    url = reverse('handle_request', args=['contatos'])
    response = api_client.post(url, contato_data, format='json')
    
    # Verificações
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id_contato' in response.data

# Teste: Atualizar Contato
@pytest.mark.django_db
def test_update_contato(api_client, contato_data, profissional_data):
    profissional = Profissional.objects.create(**profissional_data)
    contato = Contato.objects.create(
        tipo=contato_data['tipo'],
        contato=contato_data['contato'],
        profissional=profissional
    )
    
    url = reverse('handle_request', args=['contatos'])
    update_data = {"id_contato": contato.id_contato, "contato": "novo.email@exemplo.com"}
    
    response = api_client.put(url, update_data, format='json')

    # Verificações
    assert response.status_code == status.HTTP_200_OK
    assert response.data['contato'] == "novo.email@exemplo.com"

# Teste: Criar Consulta
@pytest.mark.django_db
def test_create_consulta(api_client, consulta_data, profissional_data):
    profissional = Profissional.objects.create(**profissional_data)
    consulta_data['profissional'] = profissional.id_profissional
    
    url = reverse('handle_request', args=['consultas'])
    response = api_client.post(url, consulta_data, format='json')
    
    # Verificações
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id_consulta' in response.data

# Teste: Atualizar Consulta
@pytest.mark.django_db
def test_update_consulta(api_client, consulta_data, profissional_data):
    profissional = Profissional.objects.create(**profissional_data)
    consulta = Consulta.objects.create(
        data_consulta=consulta_data['data_consulta'],
        profissional=profissional
    )
    
    url = reverse('handle_request', args=['consultas'])
    update_data = {"id_consulta": consulta.id_consulta, "data_consulta": "2024-10-12T10:00:00Z"}
    
    response = api_client.put(url, update_data, format='json')

    # Verificações
    assert response.status_code == status.HTTP_200_OK
    assert response.data['data_consulta'] == "2024-10-12T10:00:00Z"

# Teste: Deletar Profissional
@pytest.mark.django_db
def test_delete_profissional(api_client, profissional_data):
    profissional = Profissional.objects.create(**profissional_data)
    
    url = reverse('handle_request', args=['profissionais'])
    delete_data = {"id_profissional": profissional.id_profissional}
    
    response = api_client.delete(url, delete_data, format='json')

    # Verificações
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Profissional.objects.filter(id_profissional=profissional.id_profissional).count() == 0

# Teste: Deletar Contato
@pytest.mark.django_db
def test_delete_contato(api_client, contato_data, profissional_data):
    profissional = Profissional.objects.create(**profissional_data)
    contato = Contato.objects.create(
        tipo=contato_data['tipo'],
        contato=contato_data['contato'],
        profissional=profissional
    )
    
    url = reverse('handle_request', args=['contatos'])
    response = api_client.delete(url, {'id_contato': contato.id_contato}, format='json')
    
    # Verificações
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Contato.objects.filter(id_contato=contato.id_contato).count() == 0

# Teste: Deletar Consulta
@pytest.mark.django_db
def test_delete_consulta(api_client, consulta_data, profissional_data):
    profissional = Profissional.objects.create(**profissional_data)
    consulta = Consulta.objects.create(
        data_consulta=consulta_data['data_consulta'],
        profissional=profissional
    )
    
    url = reverse('handle_request', args=['consultas'])
    response = api_client.delete(url, {'id_consulta': consulta.id_consulta}, format='json')
    
    # Verificações
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Consulta.objects.filter(id_consulta=consulta.id_consulta).count() == 0

