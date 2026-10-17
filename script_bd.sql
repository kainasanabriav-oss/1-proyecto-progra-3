
CREATE DATABASE ControlAcademico;
GO

CREATE TABLE estudiantes
(
cedula varchar(12)not null,
nombre varchar(50)  not null,
apellidos  varchar(100) not null,
fechaNacimiento date null,
correo varchar(100) null,
celular varchar(15)  null,
nombreEncargado varchar(100) null,
celularEncargado varchar(15)  null,
CONSTRAINT PK_estudiantes PRIMARY KEY (cedula)
)
go

CREATE TABLE cursos (
referencia varchar(35)   not null,
descripcion varchar(100)  not null,
fechaInicio date not null,
fechaFinal date not null,
estado numeric(1) not null,
docente varchar(30) null,
horasCapacitacion int null,
horasAsesoria decimal(10,2) null,
mes varchar(20)   null,
CONSTRAINT PK_cursos        PRIMARY KEY (referencia),
CONSTRAINT CK_cursos_estado CHECK (estado IN (0, 1)),
CONSTRAINT CK_cursos_fechas CHECK (fechaFinal >= fechaInicio)
)
GO

