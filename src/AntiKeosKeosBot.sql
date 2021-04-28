-- MariaDB dump 10.18  Distrib 10.5.8-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: AntiKeosKeosBot
-- ------------------------------------------------------
-- Server version	10.5.8-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `AntiKeosKeosBot`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `antikeoskeosbot` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `AntiKeosKeosBot`;

--
-- Table structure for table `katapenting`
--

DROP TABLE IF EXISTS `katapenting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `katapenting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kata` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `katapenting`
--

LOCK TABLES `katapenting` WRITE;
/*!40000 ALTER TABLE `katapenting` DISABLE KEYS */;
INSERT INTO `katapenting` (`id`, `kata`) VALUES (1,'kuis'),(2,'uts'),(3,'uas'),(4,'tubes'),(5,'tucil'),(6,'pr');
/*!40000 ALTER TABLE `katapenting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tanggal` date DEFAULT NULL,
  `kodeMatkul` varchar(6) DEFAULT NULL,
  `jenis` varchar(255) DEFAULT NULL,
  `judul` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
INSERT INTO `task` (`id`, `tanggal`, `kodeMatkul`, `jenis`, `judul`) VALUES (1,'2021-04-21','IF2250','tugas','HIUPL 8'),(2,'2021-04-14','IF2210','pr','Resume 9 OOP'),(3,'2021-05-11','IF2211','pr','Makalah STIMA'),(4,'2021-05-10','IF2240','tubes','Milestone 4 Basdat'),(5,'2021-05-27','KU4078','uas','Studium Generale'),(6,'2021-05-20','IF2230','uas','Sistem Operasi'),(7,'2021-05-05','IF2250','uas','Rekayasa Perangkat Lunak');
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-27 14:02:55
