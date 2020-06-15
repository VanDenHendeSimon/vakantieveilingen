CREATE DATABASE  IF NOT EXISTS `vakantieveilingen` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `vakantieveilingen`;
-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: vakantieveilingen
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `auction`
--

DROP TABLE IF EXISTS `auction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auction` (
  `URL` varchar(345) NOT NULL,
  `ExtraCost` float DEFAULT NULL,
  `RetailPrice` float DEFAULT NULL,
  `Category` varchar(45) DEFAULT NULL,
  `SupplierLink` varchar(345) DEFAULT NULL,
  PRIMARY KEY (`URL`),
  KEY `categoryFK_idx` (`Category`),
  CONSTRAINT `categoryFK` FOREIGN KEY (`Category`) REFERENCES `category` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auction`
--

LOCK TABLES `auction` WRITE;
/*!40000 ALTER TABLE `auction` DISABLE KEYS */;
INSERT INTO `auction` VALUES ('https://www.vakantieveilingen.be/producten/elektronica/aircooler-mobiel_nedis-wit.html',12.45,99.95,'Elektronica',NULL),('https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',12.45,59.99,'Elektronica',NULL),('https://www.vakantieveilingen.be/producten/koken-en-tafelen/aluminium_-hand-juicer.html',12.45,79.95,'Koken en tafelen',NULL),('https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',12.45,199,'Slapen',NULL),('https://www.vakantieveilingen.be/producten/tuin-en-buiten/4-delige-tuingereedschapset_hyundai-58328.html',12.45,39.95,'Tuin en buiten',''),('https://www.vakantieveilingen.be/producten/tuin-en-buiten/hyundai-_zwarte-buitenlamp-met-bewegingssensor.html',12.45,44.95,'Tuin en buiten',NULL),('https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',11.45,49.95,'Tuin en buiten',''),('https://www.vakantieveilingen.be/vakanties/campings-en-vakantieparken/sunparks_waardebon.html',10.45,150,'Campings en vakantieparken',NULL);
/*!40000 ALTER TABLE `auction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `auctions_won`
--

DROP TABLE IF EXISTS `auctions_won`;
/*!50001 DROP VIEW IF EXISTS `auctions_won`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `auctions_won` AS SELECT 
 1 AS `Id`,
 1 AS `Timestamp`,
 1 AS `AuctionURL`,
 1 AS `CurrentPrice`,
 1 AS `Bid`,
 1 AS `Won`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `Name` varchar(45) NOT NULL,
  `Description` varchar(345) DEFAULT NULL,
  `Blacklisted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES ('Bloemen en planten','',1),('Boodschappen','',1),('Campings en vakantieparken','',0),('Elektronica','',0),('Erotiek','',1),('Fotoproducten','',1),('Koken en tafelen','',0),('Persoonlijke verzorging','',1),('Slapen','',0),('Sport en gezondheid','',1),('Tuin en buiten','',1),('Wanddecoratie','',1),('Wonen','',1);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `history`
--

DROP TABLE IF EXISTS `history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `history` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `AuctionURL` varchar(345) NOT NULL,
  `CurrentPrice` float NOT NULL,
  `Bid` int DEFAULT '0',
  `Won` bit(1) DEFAULT b'0',
  PRIMARY KEY (`Id`),
  KEY `auctionFK_idx` (`AuctionURL`),
  CONSTRAINT `auctionFK` FOREIGN KEY (`AuctionURL`) REFERENCES `auction` (`URL`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `history`
--

LOCK TABLES `history` WRITE;
/*!40000 ALTER TABLE `history` DISABLE KEYS */;
INSERT INTO `history` VALUES (4,'2020-06-08 19:38:35','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',20.45,0,_binary '\0'),(5,'2020-06-08 19:40:35','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',16.45,0,_binary '\0'),(6,'2020-06-08 19:42:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',13.45,0,_binary '\0'),(7,'2020-06-08 19:44:35','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',14.45,0,_binary '\0'),(8,'2020-06-08 19:46:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',17.45,0,_binary '\0'),(9,'2020-06-08 19:48:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',13.45,0,_binary '\0'),(10,'2020-06-08 19:50:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',20.45,0,_binary '\0'),(11,'2020-06-08 19:53:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',16.45,0,_binary '\0'),(12,'2020-06-08 19:55:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',16.45,0,_binary '\0'),(13,'2020-06-08 19:57:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',18.45,0,_binary '\0'),(14,'2020-06-08 19:59:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',16.45,0,_binary '\0'),(15,'2020-06-08 20:01:35','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',13.45,0,_binary '\0'),(16,'2020-06-08 20:03:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',13.45,0,_binary '\0'),(17,'2020-06-08 20:06:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',13.45,0,_binary '\0'),(18,'2020-06-08 20:09:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',16.45,0,_binary '\0'),(19,'2020-06-08 20:12:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',14.45,0,_binary '\0'),(20,'2020-06-08 20:15:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',15.45,0,_binary '\0'),(21,'2020-06-08 20:18:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',13.45,0,_binary '\0'),(22,'2020-06-08 20:21:34','https://www.vakantieveilingen.be/producten/tuin-en-buiten/uitzetbare-tuinslang_15-meter.html',15.45,0,_binary '\0'),(23,'2020-06-08 20:29:34','https://www.vakantieveilingen.be/vakanties/campings-en-vakantieparken/sunparks_waardebon.html',14.45,0,_binary '\0'),(24,'2020-06-08 20:34:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(25,'2020-06-08 20:35:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',38.45,0,_binary '\0'),(26,'2020-06-08 20:44:51','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',36.45,0,_binary '\0'),(27,'2020-06-08 20:45:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',35.45,0,_binary '\0'),(28,'2020-06-08 20:49:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',38.45,0,_binary '\0'),(29,'2020-06-08 20:51:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',42.45,0,_binary '\0'),(30,'2020-06-08 20:53:35','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',42.45,0,_binary '\0'),(31,'2020-06-08 20:54:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',46.45,0,_binary '\0'),(32,'2020-06-08 20:55:53','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',36.45,0,_binary '\0'),(33,'2020-06-08 20:57:35','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',41.45,0,_binary '\0'),(34,'2020-06-08 20:58:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',35.45,0,_binary '\0'),(35,'2020-06-08 20:59:35','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',35.45,0,_binary '\0'),(36,'2020-06-08 21:00:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',42.45,0,_binary '\0'),(37,'2020-06-08 21:01:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',41.45,0,_binary '\0'),(38,'2020-06-08 21:02:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',41.45,0,_binary '\0'),(39,'2020-06-08 21:03:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(40,'2020-06-08 21:04:35','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(41,'2020-06-08 21:05:36','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(42,'2020-06-08 21:06:46','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(43,'2020-06-08 21:07:42','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',35.45,0,_binary '\0'),(44,'2020-06-08 21:08:35','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',36.45,0,_binary '\0'),(45,'2020-06-08 21:09:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',35.45,0,_binary '\0'),(46,'2020-06-08 21:10:51','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',36.45,0,_binary '\0'),(47,'2020-06-08 21:12:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',39.45,0,_binary '\0'),(48,'2020-06-08 21:14:35','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',42.45,0,_binary '\0'),(49,'2020-06-08 21:16:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',40.45,0,_binary '\0'),(51,'2020-06-08 21:19:55','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',39.45,0,_binary '\0'),(52,'2020-06-08 22:25:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(53,'2020-06-08 22:41:34','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(54,'2020-06-09 00:29:37','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',38.45,0,_binary '\0'),(55,'2020-06-09 05:31:37','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',49.45,0,_binary '\0'),(56,'2020-06-09 07:52:37','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',40.45,0,_binary '\0'),(57,'2020-06-09 08:29:36','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',41.45,0,_binary '\0'),(58,'2020-06-10 19:11:37','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(59,'2020-06-10 19:15:38','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',35.45,0,_binary '\0'),(60,'2020-06-10 19:20:38','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',40.45,0,_binary '\0'),(61,'2020-06-10 20:14:45','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',20.45,0,_binary '\0'),(62,'2020-06-10 20:15:36','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',24.45,0,_binary '\0'),(63,'2020-06-10 20:16:51','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',20.45,0,_binary '\0'),(64,'2020-06-10 20:17:36','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',21.45,0,_binary '\0'),(65,'2020-06-10 20:18:37','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',20.45,0,_binary '\0'),(66,'2020-06-10 20:19:54','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',22.45,0,_binary '\0'),(67,'2020-06-10 20:20:36','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',22.45,0,_binary '\0'),(68,'2020-06-10 20:21:37','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',24.45,0,_binary '\0'),(69,'2020-06-10 20:22:36','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25.45,0,_binary '\0'),(70,'2020-06-10 20:23:53','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',20.45,0,_binary '\0'),(71,'2020-06-10 20:26:36','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',22.45,0,_binary '\0'),(72,'2020-06-10 20:35:55','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',20.45,0,_binary '\0'),(73,'2020-06-10 20:36:45','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',20.45,0,_binary '\0'),(74,'2020-06-10 20:41:52','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',21.45,0,_binary '\0'),(75,'2020-06-10 20:43:37','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',21.45,0,_binary '\0'),(76,'2020-06-10 20:44:36','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',22.45,0,_binary '\0'),(77,'2020-06-10 20:45:42','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',20.45,0,_binary '\0'),(78,'2020-06-10 20:46:44','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',26.45,0,_binary '\0'),(79,'2020-06-10 20:47:56','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',27.45,0,_binary '\0'),(80,'2020-06-10 20:48:37','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',43.45,0,_binary '\0'),(82,'2020-06-10 20:49:57','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',26.45,0,_binary '\0'),(84,'2020-06-10 21:00:54','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25.45,0,_binary '\0'),(85,'2020-06-10 21:01:55','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25.45,0,_binary '\0'),(86,'2020-06-10 21:02:56','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25.45,0,_binary '\0'),(87,'2020-06-10 21:03:56','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25.45,0,_binary '\0'),(88,'2020-06-10 21:04:56','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25.45,0,_binary '\0'),(89,'2020-06-10 21:05:56','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25.45,0,_binary '\0'),(90,'2020-06-10 21:08:53','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',26.45,0,_binary '\0'),(91,'2020-06-10 21:09:56','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',26.45,0,_binary '\0'),(92,'2020-06-10 21:10:56','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',24.45,1,_binary ''),(93,'2020-06-10 21:10:56','https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25.45,0,_binary '\0'),(94,'2020-06-15 19:28:21','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(95,'2020-06-15 19:52:54','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(96,'2020-06-15 20:00:09','https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',37.45,0,_binary '\0'),(97,'2020-06-15 20:24:55','https://www.vakantieveilingen.be/producten/tuin-en-buiten/4-delige-tuingereedschapset_hyundai-58328.html',17.45,1,_binary '');
/*!40000 ALTER TABLE `history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `Volgnummer` int NOT NULL AUTO_INCREMENT,
  `AuctionURL` varchar(345) NOT NULL,
  `MaxPrice` float NOT NULL,
  `Bought` bit(1) DEFAULT b'0',
  PRIMARY KEY (`Volgnummer`),
  KEY `autcionfk_idx` (`AuctionURL`),
  CONSTRAINT `autcionfk` FOREIGN KEY (`AuctionURL`) REFERENCES `auction` (`URL`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
INSERT INTO `wishlist` VALUES (1,'https://www.vakantieveilingen.be/producten/slapen/verzwaringsdeken_kustaa.html',35,_binary '\0'),(3,'https://www.vakantieveilingen.be/producten/tuin-en-buiten/4-delige-tuingereedschapset_hyundai-58328.html',20,_binary ''),(4,'https://www.vakantieveilingen.be/producten/tuin-en-buiten/hyundai-_zwarte-buitenlamp-met-bewegingssensor.html',25,_binary '\0'),(6,'https://www.vakantieveilingen.be/producten/elektronica/nordland_personenweegshaal-pd8734.html',25,_binary '');
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'vakantieveilingen'
--

--
-- Dumping routines for database 'vakantieveilingen'
--

--
-- Final view structure for view `auctions_won`
--

/*!50001 DROP VIEW IF EXISTS `auctions_won`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `auctions_won` AS select `history`.`Id` AS `Id`,`history`.`Timestamp` AS `Timestamp`,`history`.`AuctionURL` AS `AuctionURL`,`history`.`CurrentPrice` AS `CurrentPrice`,`history`.`Bid` AS `Bid`,`history`.`Won` AS `Won` from `history` where (`history`.`Won` = 1) order by `history`.`Timestamp` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-15 22:39:56
