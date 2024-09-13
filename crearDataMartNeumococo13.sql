CREATE TABLE IF NOT EXISTS data_mart_neumococo_13 (
    tipoidentificacion VARCHAR(200),
    fechanacimiento DATE, 
  	nombremunicipioresidencia VARCHAR(200),
    discapacitado VARCHAR(200),
    neumococo_conjugado_13_valente_primera VARCHAR(200),
	neumococo_conjugado_13_valente_segunda VARCHAR(200),
	neumococo_conjugado_13_valente_tercera VARCHAR(200),
    fecha_limite DATE,
    vacunas_0_a_5 INT,
    total_vacunas INT,
    primera_vacuna DATE,
    ultima_vacuna DATE,
    dias_entre_vacunas DECIMAL,
    frecuencia_vacunacion DECIMAL,
	frecuencia_nacimiento_primera TEXT,
	frecuencia_primera_segunda TEXT,
	frecuencia_segunda_tercera TEXT,
	frecuencia_general TEXT
);

COPY public.data_mart_neumococo_13(
	tipoidentificacion,
	fechanacimiento,
	nombremunicipioresidencia,
	discapacitado,
    neumococo_conjugado_13_valente_primera,
	neumococo_conjugado_13_valente_segunda,
	neumococo_conjugado_13_valente_tercera,
	fecha_limite,
	vacunas_0_a_5,
	total_vacunas,
	primera_vacuna,
	ultima_vacuna,
	dias_entre_vacunas,
	frecuencia_vacunacion,
	frecuencia_nacimiento_primera,
	frecuencia_primera_segunda,
	frecuencia_segunda_tercera,
	frecuencia_general
)
FROM 'C:\Hackhathon\data_mart_frecuencia_neumococo_13.csv' DELIMITER '|' CSV HEADER ENCODING 'LATIN1';

--drop table data_mart_neumococo_13;

--delete from data_mart_neumococo_13;

select * from data_mart_neumococo_13;