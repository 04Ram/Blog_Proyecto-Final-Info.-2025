def es_colaborador(request):
    if request.user.is_authenticated:
        return {
            "es_colaborador": request.user.groups.filter(
                name__in=["Colaboradores", "Admin"]
            ).exists() or request.user.is_superuser
        }
    return {"es_colaborador": False}