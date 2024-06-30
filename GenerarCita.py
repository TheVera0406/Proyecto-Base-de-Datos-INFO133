import random
from datetime import datetime, date, time, timedelta

# Función para generar una fecha aleatoria entre enero 2024 y junio 2024
def generar_fecha():
    start_date = date(2024, 1, 1)
    end_date = date(2024, 6, 30)
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Función para generar hora de inicio y fin
def generar_horas():
    hora_inicio = time(random.randint(9, 16), random.choice([0, 15, 30, 45]))
    duracion = timedelta(minutes=random.choice([30, 45, 60, 90, 120]))
    hora_fin = (datetime.combine(date.today(), hora_inicio) + duracion).time()
    
    # Asegurarse de que la hora de fin no pase de las 17:00
    if hora_fin > time(17, 0):
        hora_fin = time(17, 0)
    
    return hora_inicio, hora_fin

# Función para generar un total aleatorio
def generar_total():
    return round(random.uniform(10000, 100000), -2)  # Entre $10,000 y $100,000, redondeado a 100

# Lista para almacenar las sentencias SQL
sql_statements = []

# Generar 500 citas aleatorias
for id_cita in range(1, 1501):
    id_sede = random.randint(1, 50)      
    id_emple = random.randint(1, 200)    
    id_cliente = random.randint(1, 700)  
    fecha_cita = generar_fecha()
    hora_inicio, hora_fin = generar_horas()
    total = generar_total()

    # Construir la sentencia SQL para insertar el registro
    sql_statement = f"""INSERT INTO cita (id_cita, id_sede, id_emple, id_cliente, hora_inicio, hora_fin, fecha_cita, total) VALUES ({id_cita}, {id_sede}, {id_emple}, {id_cliente}, '{hora_inicio}', '{hora_fin}', '{fecha_cita}', ${total:.2f});"""
    sql_statements.append(sql_statement)

# Escribir el script SQL en un archivo
with open("insert_cita.sql", "w") as file:
    file.write("\n".join(sql_statements))

print("El script SQL se ha generado correctamente en el archivo 'insert_cita.sql'.")