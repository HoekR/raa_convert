USE `republiek`;
DROP TABLE data;
DROP TABLE functielokaal;
DROP TABLE functiebovenlokaal;
DROP TABLE regentoud;
DROP TABLE bronfunctiedetails;

CREATE TABLE `bronregentdetails_` (`IDBronregentdetails` BIGINT(20) AUTO_INCREMENT PRIMARY KEY) SELECT * FROM `bronregentdetails` ORDER BY `IDRegent`,`IDBron`;
ALTER TABLE `bronregentdetails_` ADD UNIQUE IDBronRegent (`IDBron`,`IDRegent`);
DROP TABLE bronregentdetails;
ALTER TABLE bronregentdetails_ RENAME bronregentdetails;

ALTER TABLE `regent` ADD `eindcontrole` varchar(255);
ALTER TABLE `regent` ADD `geboortedag` varchar(255);
ALTER TABLE `regent` ADD `geboortemaand` varchar(255);
ALTER TABLE `regent` ADD `doopjaar` varchar(255);
ALTER TABLE `regent` ADD `geboorteplaats` varchar(255);
ALTER TABLE `regent` ADD `overlijdensplaats` varchar(255);
ALTER TABLE `regent` DROP `opmerkingen2`;

ALTER TABLE `aliassen` CHANGE `IDPersoon` `IDRegent` bigint(20);
ALTER TABLE `aliassen` ADD `id` bigint(20);

RENAME TABLE `regionaal` TO `regio`;
ALTER TABLE `provinciaal` CHANGE `IDprovincie` `IDProvinciaal` bigint(20);

ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `ID` `IDBovenlokaalcollegeregentdetails` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `lokaal` `IDLokaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `provinciaal` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `regio` `IDRegio` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `stand` `IDStand` bigint(20);
# toelichting
ALTER TABLE `college` ADD `toelichting` text;

USE `batfra`;
DROP TABLE data;
DROP TABLE functielokaal;
DROP TABLE functiebovenlokaal;
DROP TABLE bronfunctiedetails;
CREATE TABLE `bronregentdetails_` (`IDBronregentdetails` BIGINT(20) AUTO_INCREMENT PRIMARY KEY) SELECT * FROM `bronregentdetails` ORDER BY `IDRegent`,`IDBron`;
ALTER TABLE `bronregentdetails_` ADD UNIQUE IDBronRegent (`IDBron`,`IDRegent`);
DROP TABLE bronregentdetails;
ALTER TABLE bronregentdetails_ RENAME bronregentdetails;
ALTER TABLE `regent` ADD `Opmerkingen2` text AFTER `Opmerkingen`;
ALTER TABLE `regent` ADD `Overlijdensdag` char(2) AFTER `Periode`;
ALTER TABLE `regent` ADD `Overlijdensmaand` char(2) AFTER `Overlijdensdag`;
ALTER TABLE `regent` DROP `opmerkingen2`;
ALTER TABLE `aliassen` CHANGE `IDPersoon` `IDRegent` bigint(20);
ALTER TABLE `aliassen` ADD `id` bigint(20);
RENAME TABLE `regionaal` TO `regio`;
ALTER TABLE `provinciaal` CHANGE `IDprovincie` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `ID` `IDBovenlokaalcollegeregentdetails` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `lokaal` `IDLokaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `provinciaal` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `regio` `IDRegio` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `stand` `IDStand` bigint(20);

USE `divperioden`;
DROP TABLE data;
DROP TABLE functielokaal;
DROP TABLE functiebovenlokaal;
DROP TABLE bronfunctiedetails;
CREATE TABLE `bronregentdetails_` (`IDBronregentdetails` BIGINT(20) AUTO_INCREMENT PRIMARY KEY) SELECT * FROM `bronregentdetails` ORDER BY `IDRegent`,`IDBron`;
ALTER TABLE `bronregentdetails_` ADD UNIQUE IDBronRegent (`IDBron`,`IDRegent`);
DROP TABLE bronregentdetails;
ALTER TABLE bronregentdetails_ RENAME bronregentdetails;
ALTER TABLE `regent` ADD `Eindcontrole` tinyint(4) AFTER `Overlijdensmaand`;
ALTER TABLE `regent` DROP `opmerkingen2`;
ALTER TABLE `aliassen` CHANGE `IDPersoon` `IDRegent` bigint(20);
ALTER TABLE `aliassen` ADD `id` bigint(20);
RENAME TABLE `regionaal` TO `regio`;
ALTER TABLE `provinciaal` CHANGE `IDprovincie` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `ID` `IDBovenlokaalcollegeregentdetails` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `lokaal` `IDLokaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `provinciaal` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `regio` `IDRegio` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `stand` `IDStand` bigint(20);

USE `negentien`;
DROP TABLE data;
DROP TABLE functielokaal;
#DROP TABLE functiebovenlokaal;
DROP TABLE bronfunctiedetails;
CREATE TABLE `bronregentdetails_` (`IDBronregentdetails` BIGINT(20) AUTO_INCREMENT PRIMARY KEY) SELECT * FROM `bronregentdetails` ORDER BY `IDRegent`,`IDBron`;
ALTER TABLE `bronregentdetails_` ADD UNIQUE IDBronRegent (`IDBron`,`IDRegent`);
DROP TABLE bronregentdetails;
ALTER TABLE bronregentdetails_ RENAME bronregentdetails;

ALTER TABLE `regent` ADD `Eindcontrole` tinyint(4) AFTER `Overlijdensmaand`;

ALTER TABLE `aliassen` CHANGE `IDPersoon` `IDRegent` bigint(20);
ALTER TABLE `aliassen` ADD `id` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `lokaal` `IDLokaal` bigint(20);
RENAME TABLE `regionaal` TO `regio`;
ALTER TABLE `provinciaal` CHANGE `IDprovincie` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `ID` `IDBovenlokaalcollegeregentdetails` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `provinciaal` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `regio` `IDRegio` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `stand` `IDStand` bigint(20);

ALTER TABLE `regent` DROP `tempid`;
# toelichting
ALTER TABLE `college` ADD `toelichting` text;

# Change to varchars like in the other databases.
ALTER TABLE `regent` CHANGE `Geboortedag` `Geboortedag` varchar(255);
ALTER TABLE `regent` CHANGE `Geboortemaand` `Geboortemaand` varchar(255);
ALTER TABLE `regent` CHANGE `Geboortejaar` `Geboortejaar` varchar(255);
ALTER TABLE `regent` CHANGE `Overlijdensdag` `Overlijdensdag` varchar(255);
ALTER TABLE `regent` CHANGE `Overlijdensmaand` `Overlijdensmaand` varchar(255);
ALTER TABLE `regent` CHANGE `Overlijdensjaar` `Overlijdensjaar` varchar(255);
ALTER TABLE `regent` CHANGE `Doopjaar` `Doopjaar` varchar(255);
alter table bovenlokaalcollegeregentdetails change Begindag Begindag varchar(255);
alter table bovenlokaalcollegeregentdetails change Beginmaand Beginmaand varchar(255);
alter table bovenlokaalcollegeregentdetails change Beginjaar Beginjaar varchar(255);
alter table bovenlokaalcollegeregentdetails change Einddag Einddag varchar(255);
alter table bovenlokaalcollegeregentdetails change Eindmaand Eindmaand varchar(255);
alter table bovenlokaalcollegeregentdetails change Eindjaar Eindjaar varchar(255);

USE `me`;
DROP TABLE data;
DROP TABLE functielokaal;
DROP TABLE functiebovenlokaal;
DROP TABLE bronfunctiedetails;
CREATE TABLE `bronregentdetails_` (`IDBronregentdetails` BIGINT(20) AUTO_INCREMENT PRIMARY KEY) SELECT * FROM `bronregentdetails` ORDER BY `IDRegent`,`IDBron`;
ALTER TABLE `bronregentdetails_` ADD UNIQUE IDBronRegent (`IDBron`,`IDRegent`);
DROP TABLE bronregentdetails;
ALTER TABLE bronregentdetails_ RENAME bronregentdetails;
ALTER TABLE `regent` ADD `Opmerkingen2` text AFTER `Opmerkingen`;
ALTER TABLE `regent` ADD `Overlijdensdag` char(2) AFTER `Periode`;
ALTER TABLE `regent` ADD `Overlijdensmaand` char(2) AFTER `Overlijdensdag`;
ALTER TABLE `regent` DROP `opmerkingen2`;
ALTER TABLE `aliassen` CHANGE `IDPersoon` `IDRegent` bigint(20);
ALTER TABLE `aliassen` ADD `id` bigint(20);
RENAME TABLE `regionaal` TO `regio`;
ALTER TABLE `provinciaal` CHANGE `IDprovincie` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `ID` `IDBovenlokaalcollegeregentdetails` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `lokaal` `IDLokaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `provinciaal` `IDProvinciaal` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `regio` `IDRegio` bigint(20);
ALTER TABLE `bovenlokaalcollegeregentdetails` CHANGE `stand` `IDStand` bigint(20);
