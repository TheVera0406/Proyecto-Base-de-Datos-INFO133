import psycopg2
import schedule
import time
import datetime
import threading

# Configuración de la conexión a la base de datos transaccional
trans_db_config = {
    'dbname': 'db_proyecto',
    'user': 'nico',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

# Configuración de la conexión a la base de datos analítica
analytical_db_config = {
    'dbname': 'db_analisis',
    'user': 'nico',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

def get_trans_db_connection():
    return psycopg2.connect(**trans_db_config)

def get_analytical_db_connection():
    return psycopg2.connect(**analytical_db_config)

def get_last_processed_ids():
    """Retrieve the last processed IDs from the analytical tables."""
    conn = get_analytical_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COALESCE(MAX(id_cita), 0) FROM FactCitas;")
        last_cita_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(MAX(id_cliente), 0) FROM DimClientes;")
        last_cliente_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(MAX(id_emple), 0) FROM DimEmpleados;")
        last_empleado_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(MAX(id_serv), 0) FROM DimServicios;")
        last_servicio_id = cursor.fetchone()[0]
    conn.close()
    return last_cita_id, last_cliente_id, last_empleado_id, last_servicio_id

def extract_and_load_data():
    print(f"{datetime.datetime.now()}: Iniciando la extracción y carga de datos...")

    try:
        trans_conn = get_trans_db_connection()
        anal_conn = get_analytical_db_connection()

        last_cita_id, last_cliente_id, last_empleado_id, last_servicio_id = get_last_processed_ids()

        with trans_conn.cursor() as trans_cursor, anal_conn.cursor() as anal_cursor:
            # Extraer y cargar datos en FactCitas
            trans_cursor.execute("""
                SELECT c.id_cita, c.id_sede, c.id_emple, c.id_cliente, c.hora_inicio, c.hora_fin, c.fecha_cita, c.total, sp.comuna_pelu, cl.comuna_cliente
                FROM public.cita c
                JOIN public.sede_pelu sp ON c.id_sede = sp.id_sede
                JOIN public.clientes cl ON c.id_cliente = cl.id_cliente
                WHERE c.id_cita > %s;
            """, (last_cita_id,))
            fact_citas_data = trans_cursor.fetchall()
            anal_cursor.executemany("""
                INSERT INTO FactCitas (id_cita, id_sede, id_emple, id_cliente, hora_inicio, hora_fin, fecha_cita, total, comuna_pelu, comuna_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, fact_citas_data)

            # Extraer y cargar datos en DimClientes
            trans_cursor.execute("""
                SELECT id_cliente, nombre_cliente, apellido_cliente, direccion_cliente, comuna_cliente, region_cliente, sexo, fecha_nacimiento, rut_cliente
                FROM public.clientes
                WHERE id_cliente > %s;
            """, (last_cliente_id,))
            dim_clientes_data = trans_cursor.fetchall()
            anal_cursor.executemany("""
                INSERT INTO DimClientes (id_cliente, nombre_cliente, apellido_cliente, direccion_cliente, comuna_cliente, region_cliente, sexo, fecha_nacimiento, rut_cliente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, dim_clientes_data)

            # Extraer y cargar datos en DimEmpleados
            trans_cursor.execute("""
                SELECT id_emple, nombre_emple, apellido_emple, direccion_emplea, comuna_emple, region_emplea, rut_emplea, cargo, sueldo, id_sede
                FROM public.empleados
                WHERE id_emple > %s;
            """, (last_empleado_id,))
            dim_empleados_data = trans_cursor.fetchall()
            anal_cursor.executemany("""
                INSERT INTO DimEmpleados (id_emple, nombre_emple, apellido_emple, direccion_emplea, comuna_emple, region_emplea, rut_emplea, cargo, sueldo, id_sede)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, dim_empleados_data)

            # Extraer y cargar datos en DimServicios
            trans_cursor.execute("""
                SELECT id_serv, tipo_serv, precio_serv
                FROM public.servicio
                WHERE id_serv > %s;
            """, (last_servicio_id,))
            dim_servicios_data = trans_cursor.fetchall()
            anal_cursor.executemany("""
                INSERT INTO DimServicios (id_serv, tipo_serv, precio_serv)
                VALUES (%s, %s, %s);
            """, dim_servicios_data)

            anal_conn.commit()

        trans_conn.close()
        anal_conn.close()

        print(f"{datetime.datetime.now()}: Extracción y carga de datos completada.")

    except Exception as e:
        print(f"Error: {e}")

def countdown_to_next_load():
    while True:
        now = datetime.datetime.now()
        next_run = schedule.next_run()
        remaining_time = next_run - now
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Tiempo restante para la próxima carga de datos: {int(hours)}h {int(minutes)}m {int(seconds)}s", end='\r')
        time.sleep(1)

# Ejecutar la carga de datos inmediatamente
extract_and_load_data()

# Programar la carga de datos una vez a la semana a partir de ahora
schedule.every(7).days.do(extract_and_load_data)

# Iniciar la cuenta regresiva en un hilo separado
countdown_thread = threading.Thread(target=countdown_to_next_load)
countdown_thread.start()

# Mantener el script en ejecución
while True:
    schedule.run_pending()
    time.sleep(1)