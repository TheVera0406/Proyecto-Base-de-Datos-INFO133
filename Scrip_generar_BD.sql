-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;
-- public.clientes definition

-- Drop table

-- DROP TABLE public.clientes;

CREATE TABLE public.clientes (
	id_cliente int4 NOT NULL,
	nombre_cliente varchar NOT NULL,
	apellido_cliente varchar NOT NULL,
	direccion_cliente varchar NOT NULL,
	comuna_cliente varchar NOT NULL,
	region_cliente varchar NOT NULL,
	sexo bpchar(1) NOT NULL,
	fecha_nacimiento date NOT NULL,
	rut_cliente varchar NOT NULL,
	CONSTRAINT clientes_pk PRIMARY KEY (id_cliente)
);


-- public.producto definition

-- Drop table

-- DROP TABLE public.producto;

CREATE TABLE public.producto (
	id_prod int4 NOT NULL,
	nombre_prod varchar NULL,
	precio_prod money NOT NULL,
	CONSTRAINT producto_pk PRIMARY KEY (id_prod)
);


-- public.sede_pelu definition

-- Drop table

-- DROP TABLE public.sede_pelu;

CREATE TABLE public.sede_pelu (
	id_sede int4 NOT NULL,
	nombre_pelu varchar NOT NULL,
	direccion_pelu varchar NOT NULL,
	comuna_pelu varchar NOT NULL,
	region_pelu varchar NULL,
	CONSTRAINT sede_pelu_pk PRIMARY KEY (id_sede)
);


-- public.servicio definition

-- Drop table

-- DROP TABLE public.servicio;

CREATE TABLE public.servicio (
	id_serv int4 NOT NULL,
	tipo_serv varchar NOT NULL,
	precio_serv money NOT NULL,
	CONSTRAINT servicio_pk PRIMARY KEY (id_serv)
);


-- public.empleados definition

-- Drop table

-- DROP TABLE public.empleados;

CREATE TABLE public.empleados (
	id_emple int4 NOT NULL,
	nombre_emple varchar NOT NULL,
	direccion_emplea varchar NOT NULL,
	comuna_emple varchar NOT NULL,
	region_emplea varchar NOT NULL,
	apellido_emple varchar NOT NULL,
	rut_emplea varchar NOT NULL,
	cargo varchar NOT NULL,
	sueldo money NOT NULL,
	id_sede int4 NOT NULL,
	CONSTRAINT empleados_pk PRIMARY KEY (id_emple),
	CONSTRAINT empleados_sede_pelu_fk FOREIGN KEY (id_sede) REFERENCES public.sede_pelu(id_sede)
);


-- public.cita definition

-- Drop table

-- DROP TABLE public.cita;

CREATE TABLE public.cita (
	id_cita int4 NOT NULL,
	id_sede int4 NOT NULL,
	id_emple int4 NOT NULL,
	id_cliente int4 NOT NULL,
	hora_inicio time NOT NULL,
	hora_fin time NOT NULL,
	fecha_cita date NOT NULL,
	total money NOT NULL,
	CONSTRAINT cita_pk PRIMARY KEY (id_cita),
	CONSTRAINT cita_clientes_fk FOREIGN KEY (id_cliente) REFERENCES public.clientes(id_cliente),
	CONSTRAINT cita_empleados_fk FOREIGN KEY (id_emple) REFERENCES public.empleados(id_emple),
	CONSTRAINT cita_sede_pelu_fk FOREIGN KEY (id_sede) REFERENCES public.sede_pelu(id_sede)
);


-- public.cita_detalle definition

-- Drop table

-- DROP TABLE public.cita_detalle;

CREATE TABLE public.cita_detalle (
	id_cita int4 NOT NULL,
	id_serv int4 NOT NULL,
	id_prod int4 NOT NULL,
	cantidad int4 NULL,
	CONSTRAINT cita_detalle_pkey PRIMARY KEY (id_cita, id_serv, id_prod),
	CONSTRAINT cita_detalle_id_cita_fkey FOREIGN KEY (id_cita) REFERENCES public.cita(id_cita),
	CONSTRAINT cita_detalle_id_prod_fkey FOREIGN KEY (id_prod) REFERENCES public.producto(id_prod),
	CONSTRAINT cita_detalle_id_serv_fkey FOREIGN KEY (id_serv) REFERENCES public.servicio(id_serv)
);

