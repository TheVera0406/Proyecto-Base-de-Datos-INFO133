import psycopg2
import schedule
import time
from datetime import datetime

# Conexión a la base de datos transaccional
conn_trans = psycopg2.connect(
    dbname='db_proyecto',
    user='nico',
    password='1234',
    host='localhost',
    port='5432'
)

# Conexión a la base de datos analítica
conn_analitica = psycopg2.connect(
    dbname='analitica',
    user='nico',
    password='1234',
    host='localhost',
    port='5432'
)

def transfer_data():
    cursor_trans = conn_trans.cursor()
    cursor_analitica = conn_analitica.cursor()

    # Obtener datos de la base de datos transaccional
    cursor_trans.execute("""
        SELECT
            c.id_cita,
            sp.id_sede, sp.nombre_pelu, sp.direccion_pelu, sp.comuna_pelu, sp.region_pelu,
            e.id_emple, e.nombre_emple,
            cl.id_cliente, cl.nombre_cliente, cl.apellido_cliente, cl.direccion_cliente, cl.comuna_cliente, cl.region_cliente, cl.sexo, cl.fecha_nacimiento, cl.rut_cliente,
            c.hora_inicio, c.hora_fin, c.fecha_cita, c.total,
            cd.id_serv, s.tipo_serv, s.precio_serv,
            cd.id_prod, p.nombre_prod, p.precio_prod, cd.cantidad
        FROM cita c
        JOIN sede_pelu sp ON c.id_sede = sp.id_sede
        JOIN empleados e ON c.id_emple = e.id_emple
        JOIN clientes cl ON c.id_cliente = cl.id_cliente
        JOIN cita_detalle cd ON c.id_cita = cd.id_cita
        JOIN servicio s ON cd.id_serv = s.id_serv
        LEFT JOIN producto p ON cd.id_prod = p.id_prod
    """)

    rows = cursor_trans.fetchall()

    # Insertar datos en la base de datos analítica
    for row in rows:
        cursor_analitica.execute("""
            INSERT INTO citas_analitica (
                id_cita, id_sede, nombre_peluqueria, direccion_peluqueria, comuna_peluqueria, region_peluqueria,
                id_emple, nombre_empleado, id_cliente, nombre_cliente, apellido_cliente, direccion_cliente,
                comuna_cliente, region_cliente, sexo_cliente, fecha_nacimiento, rut_cliente, hora_inicio,
                hora_fin, fecha_cita, total, id_servicio, tipo_servicio, precio_servicio,
                id_producto, nombre_producto, precio_producto, cantidad_producto
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, row)

    conn_analitica.commit()

    cursor_trans.close()
    cursor_analitica.close()
    print(f'Datos transferidos a las {datetime.now()}')

# Configurar el scheduler para ejecutar la transferencia de datos cada semana
schedule.every().week.do(transfer_data)

print("Scheduler iniciado. Transfiriendo datos cada semana.")

while True:
    schedule.run_pending()
    time.sleep(1)

# Cerrar las conexiones cuando el script se detiene (esto no se ejecutará debido al bucle infinito)
conn_trans.close()
conn_analitica.close()
