from django.shortcuts import render
from .analisis import grafico_egresos_ingresos , grafico_torta_egresos , grafico_ahorro_dolar , Graficos
from django.contrib.auth.decorators import login_required




@login_required
def metricas(request):
    ingresos_vs_egresos = grafico_egresos_ingresos()
    torta_egresos = grafico_torta_egresos()
    ahorro_dolar = grafico_ahorro_dolar()
    gastos_total_varios = Graficos().grafico_varios_total()
    gastos_total_servicios = Graficos().grafico_servicios_total()
    gastos_total_deudas = Graficos().grafico_deudas_total()

    # Pasar la cadena base64 al contexto
    context = {
        'ingresos_vs_egresos': ingresos_vs_egresos,
        'torta_egresos':torta_egresos,
        'ahorro_dolar': ahorro_dolar,
        'gastos_categoria':gastos_total_varios,
        'gastos_servicios':gastos_total_servicios,
        'gastos_deudas':gastos_total_deudas,
    }

    return render(request, 'metricas/metricas.html', context)








    
