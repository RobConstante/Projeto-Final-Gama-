
-- DROP TABLE PAIS;
CREATE TABLE PAIS(
	COD_ISO2 VARCHAR(2) NOT NULL
	,NOME VARCHAR(100) NOT NULL
	,CONSTRAINT PK_PAIS PRIMARY KEY (COD_ISO2)
	);

-- DROP TABLE CASOS
CREATE TABLE CASOS(
	COD_ISO2 VARCHAR(2) NOT NULL
	,DATA DATE NOT NULL
	,CASOS_CONFIRMADOS INT NOT NULL
	,MORTES INT NOT NULL
	--,CONSTRAINT PK_CASOS PRIMARY KEY (COD_ISO2, DATA)
	,CONSTRAINT FK_CASOS_PAIS FOREIGN KEY (COD_ISO2) REFERENCES PAIS (COD_ISO2)
	);