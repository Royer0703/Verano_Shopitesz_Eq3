/*CREACION DE LA BD*/
create database shopitesz;
use shopitesz;

create table Categorias(
	idCategoria int auto_increment not null,
    nombre varchar(60) not null,
    imagen mediumblob null,
    estatus varchar(10) not null,
    
    constraint pk_categorias primary key(idCategoria),
    constraint uk_nombre_categoria unique(nombre),
    constraint chk_estatus check (estatus in('Activa', 'Inactiva'))
);

create table Productos(
	idProducto int auto_increment not null,
    idCategoria int not null,
    nombre varchar(100) not null,
    descripcion varchar(200) not null,
    precioVenta float not null,
    existencia int not null,
    foto mediumblob null,
    especificaciones mediumblob null,
    estatus varchar(10) not null,
    
    constraint pk_productos primary key(idProducto),
    foreign key(idCategoria) references categorias(idCategoria)
);

create table Usuarios(
	idUsuario int auto_increment not null,
    nombreCompleto varchar(60) not null,
    direccion varchar(200) not null,
    telefono char(12) not null,
    email varchar(100) not null,
    password_hash varchar(20) not null,
    tipo varchar(15) not null,
    estatus varchar(10) not null,
    genero varchar(20) not null,
    
    constraint pk_usuarios primary key(idUsuario)
);

drop table Usuarios;
select * from Productos;

grant select,insert,update,delete on shopitesz.categorias to user_shopitesz;
grant select,insert,update,delete on shopitesz.Usuarios to user_shopitesz;
grant select,insert,update,delete on shopitesz.Productos to user_shopitesz;
