CREATE DATABASE  IF NOT EXISTS `shingles` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `shingles`;
-- MySQL dump 10.13  Distrib 5.5.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: shingles
-- ------------------------------------------------------
-- Server version	5.5.28-0ubuntu0.12.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text,
  `active` tinyint(1) DEFAULT '0',
  `url` varchar(255) DEFAULT NULL,
  `source_id` int(11) DEFAULT NULL,
  `created` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_news_source` (`source_id`),
  CONSTRAINT `fk_news_source` FOREIGN KEY (`source_id`) REFERENCES `news_sources` (`id`) ON DELETE SET NULL ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news_sources`
--

DROP TABLE IF EXISTS `news_sources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_sources` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `rss_url` varchar(255) DEFAULT NULL,
  `lang` varchar(45) DEFAULT 'ru',
  PRIMARY KEY (`id`),
  UNIQUE KEY `rss_url_UNIQUE` (`rss_url`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_sources`
--

LOCK TABLES `news_sources` WRITE;
/*!40000 ALTER TABLE `news_sources` DISABLE KEYS */;
INSERT INTO `news_sources` VALUES (1,'cnews.ru','http://cnews.ru/','http://www.cnews.ru/news.xml','ru'),(2,'comnews.ru','http://www.comnews.ru/','http://www.comnews.ru/rss','ru'),(3,'digit.ru','http://digit.ru/','http://digit.ru/export/rss2/index.xml','ru'),(4,'nag.ru','http://nag.ru/','http://nag.ru/rss/articles/','ru'),(5,'tasstelecom.ru','http://tasstelecom.ru/','http://tasstelecom.ru/feed','ru'),(6,'fiercewireless.com','http://www.fiercewireless.com/','http://www.fiercewireless.com/feed','en'),(7,'gigaom.com','http://gigaom.com/','http://feeds.feedburner.com/ommalik','en');
/*!40000 ALTER TABLE `news_sources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news_shingles`
--

DROP TABLE IF EXISTS `news_shingles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_shingles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `news_id` int(11) NOT NULL,
  `crc32_hash` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_shingles_news` (`news_id`),
  CONSTRAINT `fk_shingles_news` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_shingles`
--

LOCK TABLES `news_shingles` WRITE;
/*!40000 ALTER TABLE `news_shingles` DISABLE KEYS */;
/*!40000 ALTER TABLE `news_shingles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news_keywords`
--

DROP TABLE IF EXISTS `news_keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news_keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `news_id` int(11) DEFAULT NULL,
  `keyword` varchar(25) DEFAULT NULL,
  `crc32_hash` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_keywords_news` (`news_id`),
  CONSTRAINT `fk_keywords_news` FOREIGN KEY (`news_id`) REFERENCES `news` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_keywords`
--

LOCK TABLES `news_keywords` WRITE;
/*!40000 ALTER TABLE `news_keywords` DISABLE KEYS */;
/*!40000 ALTER TABLE `news_keywords` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-12-02 16:44:05
