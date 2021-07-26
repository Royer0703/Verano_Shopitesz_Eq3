/*CREACION DE LA BD*/
create database shopitesz;
drop database shopitesz;
use shopitesz;
---------------------------------/*CATEGORIA*/
create table Categorias(
	idCategoria int auto_increment not null,
    nombre varchar(60) not null,
    imagen mediumblob null,
    estatus varchar(10) not null,
    
    constraint pk_categorias primary key(idCategoria),
    constraint uk_nombre_categoria unique(nombre),
    constraint chk_estatus check (estatus in('Activa', 'Inactiva'))
);


---------------------------------/*PRODUCTOS*/
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

-------------------------/*USUARIOS*/
create table Usuarios(
	idUsuario int auto_increment not null,
    nombreCompleto varchar(60) not null,
    direccion varchar(200) not null,
    telefono char(12) not null,
    email varchar(100) not null,
    password_hash varchar(128) not null,
    tipo varchar(15) not null,
    estatus varchar(10) not null,
    genero varchar(20) not null,
    
    constraint pk_usuarios primary key(idUsuario)
);


----------------------/*CARRITO*/
create table Carrito(
	idCarrito int auto_increment not null,
    idUsuario int not null,
    idProducto int not null,
    fecha date not null,
	cantidad int not null,
    estatus varchar(10) not null,
    
    constraint pk_carrito primary key(idCarrito),
    foreign key(idUsuario) references usuarios(idUsuario),
    foreign key(idProducto) references producto(idProducto)
);

----------------------/*TARJETA*/
create table Tarjetas(
	idTarjeta int auto_increment not null,
    idUsuario int not null,
    noTarjeta varchar(16) not null,
	saldo float not null,
    Banco varchar(50) not null,
    estatus varchar(10) not null,
    
    constraint pk_tarjetas primary key(idTarjeta),
    foreign key(idUsuario) references usuarios(idUsuario)
);

----------------------/*Pedidos*/
create table Pedidos(
	idPedido int auto_increment not null,
    idComprador int not null,
    idVendedor int not null,
    idTarjeta int not null,
    fechaRegistro date not null,
    fechaAtencion date not null,
    fechaRecepcion date not null,
    fechaCierre date not null,
    total float not null,
    estatus varchar(10) not null,
    
    constraint pk_pedidos primary key(idPedido),
    foreign key(idTarjeta) references tarjetas(idTarjeta)
);

----------------------/*DetallesPedidos*/
create table DetallePedidos(
	idDetalle int auto_increment not null,
    idPedido int not null,
    idProducto int not null,
	precio float not null,
    cantidadPedida int not null,
    cantidadEnviada int not null,
    cantidadAceptada int not null,
    cantidadRechazada int not null,
    subtotal float not null,
    estatus varchar(10) not null,
	comentario varchar(200) not null,
    
    constraint pk_detalle primary key(idDetalle),
    foreign key(idPedido) references pedidos(idPedido),
    foreign key(idProducto) references productos(idProducto)
);
use shopitesz;
drop table Categorias;
insert into categorias(nombre,estatus) values('Equipo de computo','Activa');
select * from Usuarios;
select * from Categorias;
select * from Productos;
select * from ENVIOS;
select * from pedidos;
select * from paqueterias;

/*crear usuarios*/
create user user_shopitesz identified by 'Shopit3sz.123';

drop table Categorias;


grant select,insert,update,delete on shopitesz.categorias to user_shopitesz;
grant select,insert,update,delete on shopitesz.Usuarios to user_shopitesz;
grant select,insert,update,delete on shopitesz.Productos to user_shopitesz;
grant select,insert,update,delete on shopitesz.paqueterias to user_shopitesz;
grant select,insert,update,delete on shopitesz.envios to user_shopitesz;