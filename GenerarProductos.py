import random

# Lista de nombres de productos y precios
nombres_productos = [
    "Shampoo Hidratante", "Acondicionador Reparador", "Mascarilla Capilar", "Laca para Cabello",
    "Gel Fijador", "Crema de Peinado", "Tinte Capilar Rubio", "Tinte Capilar Castano",
    "Tinte Capilar Negro", "Aceite Capilar", "Serum Anticaida", "Cera para Cabello",
    "Espuma de Peinar", "Spray Protector Termico", "Crema Rizadora", "Crema Alisadora",
    "Champu Anticaspa", "Mascarilla Nutritiva", "Champu Voluminizador", "Cepillo para Cabello"
]

precios_productos = [9990, 12990, 14990, 7990, 5990, 8990, 19990, 19990, 19990, 16990, 24990, 11990, 6990, 9990, 12990, 14990, 8990, 16990, 10990, 4990]

# Lista para almacenar las sentencias SQL
sql_statements = []

# Generar 100 registros aleatorios
for _ in range(100):
    nombre_prod = random.choice(nombres_productos)
    precio_prod = random.choice(precios_productos)
    
    # Construir la sentencia SQL para insertar el registro
    sql_statement = f"INSERT INTO producto (nombre_prod, precio_prod) VALUES ('{nombre_prod}', {precio_prod});"
    sql_statements.append(sql_statement)

# Escribir el script SQL en un archivo
with open("insert_productos.sql", "w") as file:
    file.write("\n".join(sql_statements))

print("El script SQL se ha generado correctamente en el archivo 'insert_productos.sql'.")