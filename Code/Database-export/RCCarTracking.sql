-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: projectone
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `actions`
--

DROP TABLE IF EXISTS `actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actions` (
  `idactions` int NOT NULL,
  `description` varchar(200) NOT NULL,
  PRIMARY KEY (`idactions`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actions`
--

LOCK TABLES `actions` WRITE;
/*!40000 ALTER TABLE `actions` DISABLE KEYS */;
INSERT INTO `actions` VALUES (1,'Read values'),(2,'Save values'),(3,'Turn on'),(4,'Send instruction'),(5,'Set default');
/*!40000 ALTER TABLE `actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices` (
  `iddevices` int NOT NULL,
  `abbreviation` varchar(5) NOT NULL,
  `code` varchar(15) DEFAULT NULL,
  `manufacturer` varchar(45) DEFAULT NULL,
  `description` varchar(200) NOT NULL,
  `type` tinyint NOT NULL,
  `cost` float DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`iddevices`),
  UNIQUE KEY `abbreviation_UNIQUE` (`abbreviation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES (1,'ACC','ADXL335','Adafruit','5V ready triple-axis accelerometer',0,13.35,'g'),(2,'TEMP','TO-92','Maxim','One-Wire Digital Thermometer',0,3.07,'°C'),(3,'LIGHT',NULL,'Hamamatsu','Photo IC diode - Ambient light sensor',0,2.72,NULL),(4,'NEO',NULL,'Adafruit','NeoPixel Stick 8 RGB LED',1,6.24,NULL),(5,'SPEAK',NULL,'Visation GmbH & Co.KG','Small speaker 1.6cm 8 Ohm 1 W',1,4.77,NULL);
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history` (
  `idhistory` int NOT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  `value` float DEFAULT NULL,
  `comments` varchar(200) DEFAULT NULL,
  `deviceid` int NOT NULL,
  `actionid` int NOT NULL,
  PRIMARY KEY (`idhistory`),
  KEY `deviceid_idx` (`deviceid`),
  KEY `actionid_idx` (`actionid`),
  CONSTRAINT `actionid` FOREIGN KEY (`actionid`) REFERENCES `actions` (`idactions`),
  CONSTRAINT `deviceid` FOREIGN KEY (`deviceid`) REFERENCES `devices` (`iddevices`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-15 11:10:01
