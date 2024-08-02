import pandas as pd
import matplotlib.pyplot as plt
from ingreso.models import Ingreso 
from egreso.models import Egreso  , GastosVarios , Deudas , Servicios
from ahorros.models import Ahorro
from io import BytesIO
import base64
import numpy as np


# Grafico de barras comparando egresos e ingresos  ------------------------------------------------------------------------------------>
def grafico_egresos_ingresos():
    # Obtener datos de ingresos y egresos
    ingresos = Ingreso.objects.values('monto')
    egresos = Egreso.objects.values('monto')

    # Crear DataFrames para ingresos y egresos
    df_ingresos = pd.DataFrame(ingresos, columns=['monto'])
    df_egresos = pd.DataFrame(egresos, columns=['monto'])

    # Convertir la columna 'monto' a tipo float y manejar datos faltantes
    df_ingresos['monto'] = pd.to_numeric(df_ingresos['monto'], errors='coerce').fillna(0)
    df_egresos['monto'] = pd.to_numeric(df_egresos['monto'], errors='coerce').fillna(0)

    # Agregar una columna 'tipo' para distinguir ingresos y egresos
    df_ingresos['tipo'] = 'Ingreso'
    df_egresos['tipo'] = 'Egreso'

    # Combinar ambos DataFrames
    df_combinado = pd.concat([df_ingresos, df_egresos])

    # Agrupar por tipo y sumar los montos
    df_totales = df_combinado.groupby('tipo').agg({'monto': 'sum'}).reset_index()

    # Verificar y convertir los valores a numéricos
    df_totales['monto'] = pd.to_numeric(df_totales['monto'], errors='coerce').fillna(0)

    # Crear un gráfico de barras
    fig, ax = plt.subplots()
    bars = ax.bar(df_totales['tipo'], df_totales['monto'], color=['lightblue', 'blue'])

    # Definir los valores para los ticks del eje y
    max_value = df_totales['monto'].max()
    mid_value = max_value / 2
    low_value = 100000

    # Asegurarse de que los valores sean números
    max_value = float(max_value)
    mid_value = float(mid_value)
    low_value = float(low_value)

    # Configurar los ticks y etiquetas del eje y
    ax.set_yticks([low_value, mid_value, max_value])
    ax.set_yticklabels([f'{low_value:.2f}', f'{mid_value:.2f}', f'{max_value:.2f}'])

    # Ajustar el límite superior del eje y para dar espacio a las etiquetas
    ax.set_ylim(0, max_value * 1.1)

    # Agregar etiquetas de valor encima de las barras
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'${height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

    # Agregar etiquetas y título al gráfico
    ax.set_xlabel('Tipo')
    ax.set_title('Monto Total por Tipo (Egreso/Ingreso)')

    # Guardar el gráfico en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    # Convertir el objeto BytesIO a una cadena base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return image_base64


# Grafico de torta con los 5 max egresos --------------------------------------------------------------------------------------------->
def grafico_torta_egresos(): 
    egresos = Egreso.objects.values('monto', 'concepto')
    df_egresos = pd.DataFrame(egresos, columns=['monto', 'concepto'])

    # Convertir la columna 'monto' a tipo float
    df_egresos['monto'] = pd.to_numeric(df_egresos['monto'], errors='coerce')

    # Crear un segundo grafico de torta solo para egresos
    df_agrupado_egresos = df_egresos.groupby('concepto')['monto'].sum().reset_index()
    df_top_10_egresos = df_agrupado_egresos.nlargest(5, 'monto')

    # Redimensionar el grafico de torta
    plt.figure(figsize=(10,7))

    # Crear un grafico de torta sin etiquetas
    wedges, texts, autotexts = plt.pie(
        df_top_10_egresos['monto'], labels=None, autopct='%1.1f%%', startangle=90,
        wedgeprops=dict(width=0.3))  # Crear efecto de anillo

    # Añadir un círculo blanco en el centro para el efecto de anillo
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title('Distribución de Egresos por Concepto - Top 5')

    # Agregar la leyenda fuera del gráfico
    plt.legend(wedges, df_top_10_egresos['concepto'], title="Conceptos", loc="center left", bbox_to_anchor=(1.1, 0.5))

    # Posicionar los porcentajes fuera del gráfico
    for i, autotext in enumerate(autotexts):
        angle = wedges[i].theta2 - (wedges[i].theta2 - wedges[i].theta1) / 2
        x = np.cos(np.radians(angle))
        y = np.sin(np.radians(angle))
        horizontal_alignment = 'left' if x > 0 else 'right'
        connectionstyle = "angle,angleA=0,angleB={}".format(angle)
        autotext.set_position((1.1 * x, 1.1 * y))  # Ajusta la posición según sea necesario
        autotext.set_horizontalalignment(horizontal_alignment)
        autotext.set_color('black')
        autotext.set_fontsize(9)
        autotext.set_bbox(dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.3'))

    # Guardar el grafico de torta en un objeto BytesIO
    buffer_egresos = BytesIO()
    plt.savefig(buffer_egresos, format='png', bbox_inches='tight')
    buffer_egresos.seek(0)
    plt.close()

    # Convertir el objeto BytesIO a una cadena base64
    image_base64_egresos = base64.b64encode(buffer_egresos.getvalue()).decode('utf-8')

    return image_base64_egresos


# Grafico lineal con progreso de ahorro en dolar ----------------------------------------------------------------------------------------->
def grafico_ahorro_dolar():
    ahorros = Ahorro.objects.all().order_by('fecha')
    fechas = [ahorro.fecha for ahorro in ahorros if ahorro.tipo_id == 1]
    montos = [ahorro.monto for ahorro in ahorros if ahorro.tipo_id == 1]

    df = pd.DataFrame({'Fecha':fechas,'Monto':montos})

    df.sort_values(by='Fecha',inplace=True)

    plt.plot(df['Fecha'],df['Monto'],marker='o', linestyle='-')

    plt.xlabel('Fecha')
    plt.ylabel('Monto del Dólar')
    plt.title('Progreso de ahorro Dolar')

    # Rotar las etiquetas del eje x para que sean legibles
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64



# Grafico lineal con progreso de ahorro en plazos fijos --------------------------------------------------------------------------------------->
def grafico_ahorro_plazo():
    pass




# Slide con 3 graficos : Maximos Consumos , Servicios , Deudas -------------------------------------------------------------------------------->
class Graficos:

    def grafico_varios_total(self):
            varios = GastosVarios.objects.values('concepto', 'monto', 'fecha')
            df_varios = pd.DataFrame(varios, columns=['concepto', 'monto', 'fecha'])

            # Agrupar por tipo, sumar los montos y ordenarlos de forma descendente
            df_varios_total = df_varios.groupby('concepto').agg({'monto': 'sum'}).reset_index()
            df_varios_total = df_varios_total.sort_values(by='monto', ascending=False).head(5)

            # Crear un gráfico de barras
            fig, ax = plt.subplots()
            bars = ax.bar(df_varios_total['concepto'], df_varios_total['monto'], color=['blue'])

            plt.ylabel('Monto')
            plt.title('Máximos Consumos')
            plt.xticks(rotation=10)

            # Obtener el valor máximo
            max_value = df_varios_total['monto'].max()
            mid_value = max_value / 2
            low_value = 0

            # Asegurarse de que los valores sean números
            max_value = float(max_value)
            mid_value = float(mid_value)
            low_value = float(low_value)

            # Configurar los ticks y etiquetas del eje y
            ax.set_yticks([low_value, mid_value, max_value])
            ax.set_yticklabels([f'${low_value:.2f}', f'${mid_value:.2f}', f'${max_value:.2f}'])

            # Guardar el gráfico en un objeto BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()

            # Convertir el objeto BytesIO a una cadena base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return image_base64

    
    
    def grafico_servicios_total(self):
            varios = Servicios.objects.values('concepto', 'monto', 'fecha')
            df_servicios = pd.DataFrame(varios, columns=['concepto', 'monto', 'fecha'])

            # Agrupar por tipo, sumar los montos y ordenarlos de forma descendente
            df_varios_total = df_servicios.groupby('concepto').agg({'monto': 'sum'}).reset_index()
            df_varios_total = df_varios_total.sort_values(by='monto', ascending=False).head(5)

            # Crear un gráfico de barras
            fig, ax = plt.subplots()
            bars = ax.bar(df_varios_total['concepto'], df_varios_total['monto'], color=['blue'])

            plt.ylabel('Monto')
            plt.title('Servicios')
            plt.xticks(rotation=10)

            # Obtener el valor máximo
            max_value = df_varios_total['monto'].max()
            mid_value = max_value / 2
            low_value = 0

            # Asegurarse de que los valores sean números
            max_value = float(max_value)
            mid_value = float(mid_value)
            low_value = float(low_value)

            # Configurar los ticks y etiquetas del eje y
            ax.set_yticks([low_value, mid_value, max_value])
            ax.set_yticklabels([f'${low_value:.2f}', f'${mid_value:.2f}', f'${max_value:.2f}'])

            # Guardar el gráfico en un objeto BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()

            # Convertir el objeto BytesIO a una cadena base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return image_base64

    
    def grafico_deudas_total(self):
            deudas = Deudas.objects.values('concepto', 'monto', 'fecha')
            df_deudas = pd.DataFrame(deudas, columns=['concepto', 'monto', 'fecha'])

            # Agrupar por tipo, sumar los montos y ordenarlos de forma descendente
            df_varios_total = df_deudas.groupby('concepto').agg({'monto': 'sum'}).reset_index()
            df_varios_total = df_varios_total.sort_values(by='monto', ascending=False).head(5)

            # Crear un gráfico de barras
            fig, ax = plt.subplots()
            bars = ax.bar(df_varios_total['concepto'], df_varios_total['monto'], color=['blue'])

            plt.title('Deudas')
            plt.xticks(rotation=10)

            # Obtener el valor máximo
            max_value = df_varios_total['monto'].max()
            mid_value = max_value / 2
            low_value = 0

            # Asegurarse de que los valores sean números
            max_value = float(max_value)
            mid_value = float(mid_value)
            low_value = float(low_value)

            # Configurar los ticks y etiquetas del eje y
            ax.set_yticks([low_value, mid_value, max_value])
            ax.set_yticklabels([f'${low_value:.2f}', f'${mid_value:.2f}', f'${max_value:.2f}'])

            # Guardar el gráfico en un objeto BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()

            # Convertir el objeto BytesIO a una cadena base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return image_base64