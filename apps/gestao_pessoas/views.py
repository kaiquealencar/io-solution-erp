from django.shortcuts import render
from django.http import HttpResponse

def gestao_list(request):
    return  HttpResponse("<p> Olá, essa é a view de gestão de pessoas</p>")