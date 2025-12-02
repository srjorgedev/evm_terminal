-- query base para la creacion de la base de datos

CREATE DATABASE evm_db;
USE evm_db;

CREATE TABLE tipo_licencia (
    codigo CHAR(1) PRIMARY KEY,
    descripcion VARCHAR(30) NOT NULL
);

CREATE TABLE marca (
    codigo VARCHAR(4) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

CREATE TABLE modelo (
    codigo VARCHAR(4) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    periodo INT NOT NULL,
    marca VARCHAR(4) NOT NULL,
    FOREIGN KEY (marca) REFERENCES marca(codigo)
);


CREATE TABLE edo_solicitud (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(50) NOT NULL
);


CREATE TABLE nvl_cobertura (
    numero INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(40)
);

CREATE TABLE tipo_empleado (
    codigo VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(40) NOT NULL
);

CREATE TABLE aseguradora (
    codigo VARCHAR(6) PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL,
    nombreFiscal VARCHAR(60) NOT NULL UNIQUE
);


CREATE TABLE empleado (
    numero INT AUTO_INCREMENT PRIMARY KEY,
    nombrePila VARCHAR(30) NOT NULL,
    apdPaterno VARCHAR(20) NOT NULL,
    apdMaterno VARCHAR(20),
    tipo_empleado VARCHAR(5) NOT NULL,
    FOREIGN KEY (tipo_empleado) REFERENCES tipo_empleado(codigo)
);

CREATE TABLE telefono (
    numero INT AUTO_INCREMENT PRIMARY KEY,
    numTelefono VARCHAR(16) UNIQUE NOT NULL,
    empleado INT NOT NULL,
    FOREIGN KEY (empleado) REFERENCES empleado(numero)
);

CREATE TABLE licencia (
    numero VARCHAR(14),
    fechaExpedicion DATE NOT NULL,
    fechaVencimiento DATE NOT NULL,
    empleado INT NOT NULL,
    tipo_licencia CHAR(1) NOT NULL,
    FOREIGN KEY (empleado) REFERENCES empleado(numero),
    FOREIGN KEY (tipo_licencia) REFERENCES tipo_licencia(codigo)
);

CREATE TABLE seguro (
    numero INT AUTO_INCREMENT PRIMARY KEY,
    numPoliza VARCHAR(30) UNIQUE NOT NULL,
    fechaInicio DATE NOT NULL,
    fechaVigencia DATE NOT NULL,
    aseguradora VARCHAR(6) NOT NULL,
    nvl_cobertura INT NOT NULL,
    FOREIGN KEY (aseguradora) REFERENCES aseguradora(codigo),
    FOREIGN KEY (nvl_cobertura) REFERENCES nvl_cobertura(numero)
);

CREATE TABLE vehiculo (
    numSerie VARCHAR(17) PRIMARY KEY,
    matricula VARCHAR(12) NOT NULL,
    proposito VARCHAR(30) NOT NULL,
    fechaAdquisicion DATE NOT NULL,
    disponibilidad BOOLEAN DEFAULT TRUE,
    marca VARCHAR(4) NOT NULL,
    modelo VARCHAR(4) NOT NULL,
    licencia_requerida CHAR(1) NOT NULL,
    FOREIGN KEY (marca) REFERENCES marca(codigo),
    FOREIGN KEY (modelo) REFERENCES modelo(codigo),
    FOREIGN KEY (licencia_requerida) REFERENCES tipo_licencia(codigo)
);

CREATE TABLE vehiculo_seguro (
    vehiculo VARCHAR(17) NOT NULL UNIQUE,
    seguro INT NOT NULL,
    PRIMARY KEY(vehiculo, seguro),
    FOREIGN KEY (vehiculo) REFERENCES vehiculo(numSerie),
    FOREIGN KEY (seguro) REFERENCES seguro(numero)
);

CREATE TABLE solicitud (
    numero INT AUTO_INCREMENT PRIMARY KEY,
    asunto VARCHAR(50) NOT NULL,
    horaSolicitada TIME NOT NULL,
    fechaSolicitada DATE NOT NULL,
    vehiculo VARCHAR(17) NOT NULL,
    edo_solicitud INT NOT NULL,
    solicitante INT NOT NULL,
    autorizador INT NOT NULL,
    FOREIGN KEY (edo_solicitud) REFERENCES edo_solicitud(numero),
    FOREIGN KEY (vehiculo) REFERENCES vehiculo(numSerie),
    FOREIGN KEY (solicitante) REFERENCES empleado(numero),
    FOREIGN KEY (autorizador) REFERENCES empleado(numero)
);

CREATE TABLE bitacora (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    destino VARCHAR(50) NOT NULL,
    asunto VARCHAR(50) NOT NULL,
    horaSalida TIME NOT NULL,
    horaEntrada TIME,
    fechaSalida DATE NOT NULL,
    fechaEntrada DATE,
    gasSalida FLOAT NOT NULL,
    gasEntrada FLOAT,
    kmSalida FLOAT NOT NULL,
    kmEntrada FLOAT,
    kmTotal FLOAT,
    kmPorLitro FLOAT,
    salida BOOLEAN NOT NULL DEFAULT TRUE,
    entrada BOOLEAN DEFAULT FALSE,
    solicitud INT NOT NULL,
    vehiculo VARCHAR(17) NOT NULL,
    visible BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (solicitud) REFERENCES solicitud(numero),
    FOREIGN KEY (vehiculo) REFERENCES vehiculo(numSerie)
);

CREATE TABLE empleado_bitacora (
    bitacora INT NOT NULL,
    empleado INT NOT NULL,
    PRIMARY KEY(bitacora, empleado),
    FOREIGN KEY (empleado) REFERENCES empleado(numero),
    FOREIGN KEY (bitacora) REFERENCES bitacora(numero)
);


ALTER TABLE empleado ADD activo TINYINT(1) NOT NULL DEFAULT 1;
ALTER TABLE empleado ADD COLUMN password_hash VARCHAR(255) NOT NULL;
ALTER TABLE empleado ADD COLUMN email VARCHAR(100) NOT NULL;


-- CREACION DE TABLAS PARA MANTENIMIENTO Y OBSERVACIONES

CREATE TABLE tipo_mantenimiento (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    comentario VARCHAR(200) NOT NULL
);

CREATE TABLE edo_mantenimiento (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(100) NOT NULL
);

CREATE TABLE tipoObservacion (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(200) NOT NULL
);

CREATE TABLE observacion (
    numero INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(200) NOT NULL,
    tipoObservacion INT NOT NULL,
    bitacora INT NOT NULL,
    FOREIGN KEY (tipoObservacion) REFERENCES tipoObservacion(numero),
    FOREIGN KEY (bitacora) REFERENCES bitacora(numero)
);

CREATE TABLE mantenimiento (
    folio INT PRIMARY KEY AUTO_INCREMENT,
    razon VARCHAR(200) NOT NULL,
    fechaProgramada DATE NOT NULL,
    comentarios VARCHAR(300),
    tipoMantenimiento INT NOT NULL,
    vehiculo VARCHAR(17) NOT NULL,
    estadoMantenimiento INT NOT NULL,
    FOREIGN KEY (tipoMantenimiento) REFERENCES tipo_mantenimiento(numero),
    FOREIGN KEY (vehiculo) REFERENCES vehiculo(numSerie),
    FOREIGN KEY (estadoMantenimiento) REFERENCES edo_mantenimiento(numero)
);

-- TABLA PUENTE NECESARIA PARA CONSULTAS ENTRE MANTENIMIENTO Y BITACORA
CREATE TABLE mantenimiento_bitacora (
    mantenimiento INT NOT NULL,
    bitacora INT NOT NULL,
    PRIMARY KEY(mantenimiento, bitacora),
    FOREIGN KEY (mantenimiento) REFERENCES mantenimiento(folio),
    FOREIGN KEY (bitacora) REFERENCES bitacora(numero)
);