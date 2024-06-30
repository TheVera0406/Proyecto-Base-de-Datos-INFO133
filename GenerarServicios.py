import random

# Lista de tipos de servicios de peluquería
tipos_servicios = [
    "Corte de cabello", "Tinte", "Mechas", "Peinado", "Alisado", 
    "Permanente", "Tratamiento capilar", "Lavado y secado", "Recogido",
    "Extensiones", "Barba y bigote", "Manicura", "Pedicura", "Depilación facial",
    "Maquillaje"
]

# Lista para almacenar las sentencias SQL
sql_statements = []

# Generar 20 registros
for id_serv in range(1, 21):  # Generamos 20 servicios
    tipo_serv = random.choice(tipos_servicios)
    
    # Generar un precio aleatorio entre $5000 y $100000
    precio_serv = random.randint(5000, 100000)

    # Construir la sentencia SQL para insertar el registro
    sql_statement = f"INSERT INTO servicio (id_serv, tipo_serv, precio_serv) VALUES ({id_serv}, '{tipo_serv}', '{precio_serv}');"
    sql_statements.append(sql_statement)

# Escribir el script SQL en un archivo
with open("insert_servicio.sql", "w") as file:
    file.write("\n".join(sql_statements))

print("El script SQL se ha generado correctamente en el archivo 'insert_servicio.sql'.")