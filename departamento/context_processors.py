from departamento.admin import Departamento

def menu_departamento(request):
    lista_departamento = Departamento.objects.all()
    return dict(opcoes_departamento=lista_departamento)