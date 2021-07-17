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
)

select * from Categorias