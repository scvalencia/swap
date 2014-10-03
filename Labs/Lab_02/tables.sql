create table Reservas(
   	idReserva number(5) constraint pk_reservas primary key,
   	idFuncion number(3),
   	idCliente number(8),
   	fecha date,
	estado varchar(8) 
	constraint ck_r_estado 
	check (estado IN ('Reserva','Compra'))
);

create table SillasReservas(
   	idSilla varchar(3),
   	idFuncion number(3),
	idReserva number(5) not null constraint fk_sr_reservas references Reservas,
	constraint pk_sillasReservas 
	primary key (idSilla, idFuncion)
);

