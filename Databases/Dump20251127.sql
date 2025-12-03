-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: librarysystem
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authors` (
  `author_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `country` varchar(100) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `birth_year` date DEFAULT NULL,
  PRIMARY KEY (`author_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authors`
--

LOCK TABLES `authors` WRITE;
/*!40000 ALTER TABLE `authors` DISABLE KEYS */;
INSERT INTO `authors` VALUES (1,'Олесь','Гончар','Україна',2,'1954-09-27'),(2,'Тарас','Шевченко','Україна',3,'1943-04-10'),(3,'Леся','Українка','Україна',4,'1966-05-15'),(4,'Микола','Куліш','Україна',22,'1964-08-12'),(5,'Ліна','Костенко','Україна',50,'2025-11-12');
/*!40000 ALTER TABLE `authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `book_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `author_id` int NOT NULL,
  `category_id` int DEFAULT NULL,
  `year` year DEFAULT NULL,
  `languages` varchar(50) DEFAULT NULL,
  `quantity` int NOT NULL DEFAULT '1',
  `access_type` enum('Тільки в читальній залі','У читальній залі і вдома') DEFAULT 'Тільки в читальній залі',
  `inventory_number` varchar(45) DEFAULT NULL,
  `collection_id` int DEFAULT NULL,
  `date_added` date NOT NULL DEFAULT (curdate()),
  `borrowed_count` int DEFAULT '0',
  `publisher_id` int DEFAULT NULL,
  PRIMARY KEY (`book_id`),
  KEY `author_id` (`author_id`),
  KEY `category_id` (`category_id`),
  KEY `fk_books_collections` (`collection_id`),
  KEY `idx_books_publisher` (`publisher_id`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `authors` (`author_id`) ON DELETE CASCADE,
  CONSTRAINT `books_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE SET NULL,
  CONSTRAINT `fk_books_collections` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`collection_id`),
  CONSTRAINT `fk_books_publisher` FOREIGN KEY (`publisher_id`) REFERENCES `publishers` (`publisher_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (7,'Тіні забутих предків',1,1,1940,'Українська',2,'Тільки в читальній залі','INV-00001',NULL,'2023-11-08',3,1),(8,'Кобзар',2,1,1940,'Українська',3,'У читальній залі і вдома','INV-00002',NULL,'2024-03-13',10,2),(12,'Лісова пісня',3,1,1911,'Українська',3,'Тільки в читальній залі','INV-00003',NULL,'2025-07-08',6,3),(15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',4,'У читальній залі і вдома','0000012',8,'2022-06-15',9,1),(18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008',NULL,'2025-08-28',0,1),(23,'[ЗБІРКА] Рік',4,4,1995,'Українська',2,'У читальній залі і вдома','COLL-00010',12,'2025-08-28',0,2),(25,'Бузарест (1920)',1,1,1920,'Українська',1,'У читальній залі і вдома','INV-00008',NULL,'2025-10-27',1,2),(27,'Марокко',1,1,1990,'Українська',1,'У читальній залі і вдома','INV-00009',NULL,'2025-10-28',4,5),(34,'[ЗБІРКА] omn',1,4,1998,'Українська',2,'У читальній залі і вдома','COLL-BOOK-00016',16,'2025-11-08',0,NULL),(35,'[ЗБІРКА] Образ',1,NULL,1999,'Українська',1,'У читальній залі і вдома','COL-BOOK-00019',19,'2025-11-08',0,NULL),(37,'[ЗБІРКА] Овес',4,NULL,1950,'Українська',1,'Тільки в читальній залі','COL-BOOK-00021',21,'2025-11-08',0,NULL),(41,'Зоряні оркести',5,9,2005,'Українська',2,'Тільки в читальній залі','INV-00021',NULL,'2025-11-12',0,NULL),(46,'Вітрила',5,1,1958,'Українська',2,'Тільки в читальній залі','INV-00018',NULL,'2025-11-15',0,NULL),(47,'[ЗБІРКА] цццц',5,NULL,2000,'Українська',1,'Тільки в читальній залі','COL-BOOK-00025',25,'2025-11-15',0,3),(48,'Таврія',1,1,1952,'Українська',1,'Тільки в читальній залі','INV-00019',NULL,'2025-11-17',0,NULL),(50,'Прапороносці',1,1,1948,'Українська',3,'Тільки в читальній залі','INV-00017',NULL,'2025-11-17',3,2),(51,'Берег любові',1,1,1976,'Українська',1,'Тільки в читальній залі','INV-00018',NULL,'2025-11-17',0,NULL),(52,'Проміння замлі',5,3,1957,'Українська',2,'Тільки в читальній залі','INV-00019',NULL,'2025-11-17',0,NULL),(53,'Колонія',4,4,1927,'Українська',1,'Тільки в читальній залі','INV-00020',NULL,'2025-11-17',0,NULL),(54,'Прощай село22',4,1,1927,'Українська',2,'Тільки в читальній залі','INV-00021',NULL,'2025-11-17',0,NULL),(55,'Вічний бунт',4,4,1932,'Українська',1,'Тільки в читальній залі','INV-00022',NULL,'2025-11-17',0,NULL),(56,'Мина Мазайло',4,9,1928,'Українська',1,'Тільки в читальній залі','INV-00023',NULL,'2025-11-17',0,NULL),(57,'Давня казка',3,2,1983,'Українська',4,'Тільки в читальній залі','INV-00024',NULL,'2025-11-17',0,2),(59,'Місячна легенда',3,5,1921,'Українська',3,'Тільки в читальній залі','INV-00026',NULL,'2025-11-17',0,NULL),(60,'Думи і мірії',3,9,1923,'Українська',3,'Тільки в читальній залі','INV-00027',NULL,'2025-11-17',0,NULL),(61,'Біда навчинь',2,5,1990,'Українська',1,'Тільки в читальній залі','INV-00028',NULL,'2025-11-17',1,NULL),(62,'Гайдамаки',2,5,1940,'Українська',1,'Тільки в читальній залі','INV-00029',NULL,'2025-11-17',0,NULL),(63,'Кавказ',2,3,1920,'Украхнська',1,'У читальній залі і вдома','INV-00030',NULL,'2025-11-17',1,NULL),(64,'Ліва',1,9,1996,'Українська',1,'Тільки в читальній залі','INV-00031',NULL,'2025-11-27',1,NULL),(65,'Завтра',1,8,2001,'Україна',4,'У читальній залі і вдома','COL-BOOK-00026',26,'2025-11-27',0,3),(67,'[ЗБІРКА] Сьогодні',1,NULL,2001,'Україна',2,'Тільки в читальній залі','COL-BOOK-00028',28,'2025-11-27',0,NULL),(68,'Вчора',1,9,2000,'Уркааїнська',2,'Тільки в читальній залі','INV-00033',NULL,'2025-11-27',0,3),(69,'[ЗБІРКА] Презія',1,NULL,2000,'Українська',1,'Тільки в читальній залі','COL-BOOK-00029',29,'2025-11-27',0,NULL),(71,'[ЗБІРКА] Червоне сонце',1,NULL,2000,'Українська',1,'Тільки в читальній залі','COL-BOOK-00030',30,'2025-11-27',0,NULL);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booktypes`
--

DROP TABLE IF EXISTS `booktypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booktypes` (
  `type_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`type_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booktypes`
--

LOCK TABLES `booktypes` WRITE;
/*!40000 ALTER TABLE `booktypes` DISABLE KEYS */;
INSERT INTO `booktypes` VALUES (3,'газети'),(6,'дисертації'),(2,'журнали'),(5,'збірники віршів'),(8,'збірники доповідей'),(4,'збірники статей'),(1,'книги'),(7,'реферати');
/*!40000 ALTER TABLE `booktypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `borrowing`
--

DROP TABLE IF EXISTS `borrowing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `borrowing` (
  `borrowing_id` int NOT NULL AUTO_INCREMENT,
  `reader_id` int NOT NULL,
  `book_id` int NOT NULL,
  `borrow_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  `due_date` date NOT NULL,
  `status` enum('active','returned','overdue') DEFAULT 'active',
  `librarian_id` int DEFAULT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`borrowing_id`),
  KEY `librarian_id` (`librarian_id`),
  KEY `idx_reader_date` (`reader_id`,`borrow_date`),
  KEY `idx_book_date` (`book_id`,`borrow_date`),
  KEY `idx_status` (`status`),
  KEY `idx_due_date` (`due_date`),
  CONSTRAINT `borrowing_ibfk_1` FOREIGN KEY (`reader_id`) REFERENCES `readers` (`reader_id`) ON DELETE CASCADE,
  CONSTRAINT `borrowing_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE,
  CONSTRAINT `borrowing_ibfk_3` FOREIGN KEY (`librarian_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `borrowing`
--

LOCK TABLES `borrowing` WRITE;
/*!40000 ALTER TABLE `borrowing` DISABLE KEYS */;
/*!40000 ALTER TABLE `borrowing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Книги'),(2,'Журнали'),(3,'Газети'),(4,'Збірники статей'),(5,'Збірники віршів'),(6,'Дисертації'),(7,'Реферати'),(8,'Збірники доповідей і тез доповідей'),(9,'Збірники');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collectionbooks`
--

DROP TABLE IF EXISTS `collectionbooks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collectionbooks` (
  `collection_id` int NOT NULL,
  `book_id` int NOT NULL,
  PRIMARY KEY (`collection_id`,`book_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `collectionbooks_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collectionbooks`
--

LOCK TABLES `collectionbooks` WRITE;
/*!40000 ALTER TABLE `collectionbooks` DISABLE KEYS */;
INSERT INTO `collectionbooks` VALUES (7,7),(8,7),(10,7),(11,7),(12,7),(13,7),(14,7),(15,7),(16,7),(22,7),(23,7),(24,7),(9,8),(9,12),(13,12),(14,12),(10,15),(11,15),(12,15),(13,15),(14,15),(15,15),(16,15),(22,15),(23,15),(24,15),(10,18),(11,18),(12,18),(13,18),(14,18),(15,18),(16,18),(22,18),(23,18),(24,18),(15,23),(16,23),(22,23),(13,25),(14,25),(15,25),(16,25),(22,25),(23,25),(24,25),(13,27),(14,27),(15,27),(16,27),(22,27),(23,27),(24,27),(22,34),(23,34),(24,34),(22,35),(23,35),(24,35),(22,37),(24,41);
/*!40000 ALTER TABLE `collectionbooks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collectionitems`
--

DROP TABLE IF EXISTS `collectionitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collectionitems` (
  `collection_id` int NOT NULL,
  `book_id` int NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `author_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `year` year DEFAULT NULL,
  `languages` varchar(50) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `access_type` enum('Тільки в читальній залі','У читальній залі і вдома') DEFAULT NULL,
  `inventory_number` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`collection_id`,`book_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `collectionitems_ibfk_1` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`collection_id`),
  CONSTRAINT `collectionitems_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collectionitems`
--

LOCK TABLES `collectionitems` WRITE;
/*!40000 ALTER TABLE `collectionitems` DISABLE KEYS */;
INSERT INTO `collectionitems` VALUES (8,7,'Тіні забутих предків',1,1,1940,'Українська',8,'У читальній залі і вдома','INV-00001'),(9,8,'Кобзар',2,1,1940,'Українська',17,'У читальній залі і вдома','INV-00002'),(9,12,'Лісова пісня',3,1,1911,'Українська',3,'Тільки в читальній залі','INV-00003'),(10,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(10,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',2,'У читальній залі і вдома','0000012'),(10,18,'Зелений клин (1919)',1,1,1950,'Українська',1,'Тільки в читальній залі','INV-00008'),(11,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(11,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',2,'У читальній залі і вдома','0000012'),(11,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(12,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(12,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',2,'У читальній залі і вдома','0000012'),(12,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(13,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(13,12,'Лісова пісня',3,1,1911,'Українська',3,'У читальній залі і вдома','INV-00003'),(13,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',2,'У читальній залі і вдома','0000012'),(13,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(13,25,'Бузарест (1920)',1,1,1920,'Українська',1,'У читальній залі і вдома','INV-00008'),(13,27,'Марокко',1,1,1990,'Українська',1,'Тільки в читальній залі','INV-00009'),(14,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(14,12,'Лісова пісня',3,1,1911,'Українська',3,'У читальній залі і вдома','INV-00003'),(14,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',2,'У читальній залі і вдома','0000012'),(14,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(14,25,'Бузарест (1920)',1,1,1920,'Українська',1,'У читальній залі і вдома','INV-00008'),(14,27,'Марокко',1,1,1990,'Українська',1,'Тільки в читальній залі','INV-00009'),(15,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(15,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',2,'У читальній залі і вдома','0000012'),(15,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(15,23,'[ЗБІРКА] Рік',4,4,1995,'Українська',2,'У читальній залі і вдома','COLL-00010'),(15,25,'Бузарест (1920)',1,1,1920,'Українська',1,'У читальній залі і вдома','INV-00008'),(15,27,'Марокко',1,1,1990,'Українська',1,'У читальній залі і вдома','INV-00009'),(16,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(16,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',2,'У читальній залі і вдома','0000012'),(16,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(16,23,'[ЗБІРКА] Рік',4,4,1995,'Українська',2,'У читальній залі і вдома','COLL-00010'),(16,25,'Бузарест (1920)',1,1,1920,'Українська',1,'У читальній залі і вдома','INV-00008'),(16,27,'Марокко',1,1,1990,'Українська',1,'У читальній залі і вдома','INV-00009'),(19,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,15,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,23,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(19,34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,15,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,23,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(20,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(21,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(21,23,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(21,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(22,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(22,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',2,'У читальній залі і вдома','0000012'),(22,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(22,23,'[ЗБІРКА] Рік',4,4,1995,'Українська',2,'У читальній залі і вдома','COLL-00010'),(22,25,'Бузарест (1920)',1,1,1920,'Українська',1,'У читальній залі і вдома','INV-00008'),(22,27,'Марокко',1,1,1990,'Українська',1,'У читальній залі і вдома','INV-00009'),(22,34,'[ЗБІРКА] omn',1,4,1998,'Українська',2,'У читальній залі і вдома','COLL-BOOK-00016'),(22,35,'[ЗБІРКА] Образ',1,NULL,1999,'Українська',1,'У читальній залі і вдома','COL-BOOK-00019'),(22,37,'[ЗБІРКА] Овес',4,NULL,1950,'Українська',1,'Тільки в читальній залі','COL-BOOK-00021'),(23,7,'Тіні забутих предків',1,1,1940,'Українська',2,'У читальній залі і вдома','INV-00001'),(23,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',3,'У читальній залі і вдома','0000012'),(23,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(23,25,'Бузарест (1920)',1,1,1920,'Українська',1,'У читальній залі і вдома','INV-00008'),(23,27,'Марокко',1,1,1990,'Українська',1,'У читальній залі і вдома','INV-00009'),(23,34,'[ЗБІРКА] omn',1,4,1998,'Українська',2,'У читальній залі і вдома','COLL-BOOK-00016'),(23,35,'[ЗБІРКА] Образ',1,NULL,1999,'Українська',1,'У читальній залі і вдома','COL-BOOK-00019'),(24,7,'Тіні забутих предків',1,1,1940,'Українська',2,'Тільки в читальній залі','INV-00001'),(24,15,'[ЗБІРКА] Крауль',1,5,2000,'Українська',3,'У читальній залі і вдома','0000012'),(24,18,'Зелений клин (1919)',1,1,1950,'Українська',3,'У читальній залі і вдома','INV-00008'),(24,25,'Бузарест (1920)',1,1,1920,'Українська',1,'У читальній залі і вдома','INV-00008'),(24,27,'Марокко',1,1,1990,'Українська',1,'У читальній залі і вдома','INV-00009'),(24,34,'[ЗБІРКА] omn',1,4,1998,'Українська',2,'У читальній залі і вдома','COLL-BOOK-00016'),(24,35,'[ЗБІРКА] Образ',1,NULL,1999,'Українська',1,'У читальній залі і вдома','COL-BOOK-00019'),(24,41,'Зоряні оркести',5,9,2005,'Українська',2,'Тільки в читальній залі','INV-00021'),(25,23,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,37,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,41,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(25,46,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,12,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,15,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,48,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,50,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,57,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,59,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,60,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(26,64,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,12,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,15,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,48,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,50,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,57,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,59,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,60,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,64,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(27,65,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,12,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,15,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,48,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,50,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,57,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,59,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,60,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,64,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(28,65,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,15,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,41,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,46,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,47,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,48,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,50,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,52,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,64,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,65,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,67,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(29,68,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,7,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,15,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,18,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,23,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,25,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,27,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,34,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,35,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,37,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,48,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,50,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,53,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,54,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,55,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,56,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,64,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,65,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,67,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,68,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(30,69,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `collectionitems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collections`
--

DROP TABLE IF EXISTS `collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collections` (
  `collection_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `category_id` int DEFAULT NULL,
  `year` year DEFAULT NULL,
  `languages` varchar(50) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `access_type` enum('Тільки в читальній залі','У читальній залі і вдома') DEFAULT NULL,
  `inventory_number` varchar(50) DEFAULT NULL,
  `type_id` int DEFAULT NULL,
  `author_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`collection_id`),
  KEY `category_id` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collections`
--

LOCK TABLES `collections` WRITE;
/*!40000 ALTER TABLE `collections` DISABLE KEYS */;
INSERT INTO `collections` VALUES (3,'123',5,2012,'Українська',2,'У читальній залі і вдома','123',NULL,NULL),(4,'Одвірок',4,2015,'Українська',2,'У читальній залі і вдома','00005',NULL,NULL),(5,'34555',8,2000,'Українська',2,'Тільки в читальній залі','00001',NULL,NULL),(6,'333',5,2000,'Укарїнська',3,'Тільки в читальній залі','000012',NULL,NULL),(7,'98i',2,2000,'Erhf]ycmrf',3,'Тільки в читальній залі','00007',NULL,NULL),(8,'Крауль',5,2000,'Українська',2,'Тільки в читальній залі','0000012',5,NULL),(9,'aio',5,1984,'Українська',2,'Тільки в читальній залі','COLL-00007',5,NULL),(10,'Золото карпат',8,1999,'Українська',3,'Тільки в читальній залі','COLL-00008',8,NULL),(11,'Інетерлюдія',8,2001,'Українська',3,'Тільки в читальній залі','COLL-00009',8,NULL),(12,'Рік',4,1995,'Українська',2,'Тільки в читальній залі','COLL-00010',4,NULL),(13,'Оресь',8,NULL,NULL,7,'Тільки в читальній залі','COLL-00011',8,NULL),(14,'Зор',8,2000,'Українська',2,'Тільки в читальній залі','COLL-00012',8,NULL),(15,'ЛАБ',5,2000,'Українська',1,'Тільки в читальній залі','COLL-00013',5,NULL),(16,'omn',4,1998,'Українська',2,'У читальній залі і вдома','COLL-00014',4,'1'),(19,'Образ',NULL,1999,'Українська',1,'У читальній залі і вдома','COLL-00015',8,'1'),(20,'Еврика',NULL,2000,'Українстька',1,'Тільки в читальній залі','COLL-00016',8,'1'),(21,'Овес',NULL,1950,'Українська',1,'Тільки в читальній залі','COLL-00017',4,'4'),(22,'78',8,2000,'Українська',1,'Тільки в читальній залі','COLL-00018',8,'1'),(23,'222',8,2000,'Українська',2,'Тільки в читальній залі','COLL-00019',8,'1'),(24,'2',5,2000,'Українська',2,'Тільки в читальній залі','COLL-00020',5,'1'),(25,'цццц',NULL,2000,'Українська',1,'Тільки в читальній залі','COLL-00021',4,'5'),(26,'Сьогодні',NULL,2001,'Україна',2,'Тільки в читальній залі','COLL-00022',1,'1'),(27,'Сьогодні',NULL,2001,'Україна',2,'Тільки в читальній залі','COLL-00022',1,'1'),(28,'Сьогодні',NULL,2001,'Україна',2,'Тільки в читальній залі','COLL-00022',1,'1'),(29,'Презія',NULL,2000,'Українська',1,'Тільки в читальній залі','COLL-00025',8,'1'),(30,'Червоне сонце',NULL,2000,'Українська',1,'Тільки в читальній залі','COLL-00026',3,'1');
/*!40000 ALTER TABLE `collections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issuedbooks`
--

DROP TABLE IF EXISTS `issuedbooks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issuedbooks` (
  `issue_id` int NOT NULL AUTO_INCREMENT,
  `reader_id` int NOT NULL,
  `book_id` int NOT NULL,
  `issue_date` date NOT NULL,
  `return_date` date DEFAULT NULL,
  `actual_return_date` date DEFAULT NULL,
  `reading_place` enum('Тільки в читальній залі','У читальній залі і в дома') DEFAULT NULL,
  `returned` tinyint(1) NOT NULL DEFAULT '0',
  `room_id` varchar(45) DEFAULT NULL,
  `librarian_id` varchar(45) DEFAULT NULL,
  `collection_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`issue_id`),
  KEY `fk_issued_reader_new` (`reader_id`),
  KEY `fk_issued_book_new` (`book_id`),
  KEY `fk_issuedbooks_collection` (`collection_id`),
  CONSTRAINT `fk_issued_book_new` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_issued_reader_new` FOREIGN KEY (`reader_id`) REFERENCES `readers` (`reader_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_issuedbooks_collection` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`collection_id`)
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issuedbooks`
--

LOCK TABLES `issuedbooks` WRITE;
/*!40000 ALTER TABLE `issuedbooks` DISABLE KEYS */;
INSERT INTO `issuedbooks` VALUES (119,24,7,'2025-06-27','2025-06-27','2025-11-19','Тільки в читальній залі',1,'1','2',NULL,'2025-08-28 12:20:09','2025-11-19 11:13:33',0),(143,1,25,'2025-11-15','2025-11-15','2025-11-27','Тільки в читальній залі',1,'1','47',NULL,'2025-11-15 15:37:54','2025-11-27 10:31:56',0),(144,1,8,'2025-11-15','2025-11-15','2025-11-19','У читальній залі і в дома',1,'1','47',NULL,'2025-11-15 15:38:07','2025-11-19 11:12:22',0),(145,23,61,'2025-11-27','2025-11-27','2025-11-27','Тільки в читальній залі',1,'3','24',NULL,'2025-11-27 02:01:49','2025-11-27 11:09:43',0),(146,23,12,'2025-11-27','2025-11-27','2025-11-27','Тільки в читальній залі',1,'3','24',NULL,'2025-11-27 10:29:29','2025-11-27 11:09:32',0),(147,23,50,'2025-11-27','2025-11-27','2025-11-27','Тільки в читальній залі',1,'3','24',NULL,'2025-11-27 10:33:17','2025-11-27 10:33:27',0),(148,23,50,'2025-11-27','2025-11-27','2025-11-27','Тільки в читальній залі',1,'3','24',NULL,'2025-11-27 10:33:46','2025-11-27 10:36:57',0),(149,23,50,'2025-11-27','2025-11-27','2025-11-27','Тільки в читальній залі',1,'3','24',NULL,'2025-11-27 10:37:07','2025-11-27 11:09:41',0),(150,23,64,'2025-11-27','2025-11-27','2025-11-27','Тільки в читальній залі',1,'3','24',NULL,'2025-11-27 10:50:17','2025-11-27 11:09:35',0),(151,23,63,'2025-11-27','2025-11-27','2025-11-27','Тільки в читальній залі',1,'3','24',NULL,'2025-11-27 10:51:28','2025-11-27 11:09:37',0),(152,23,12,'2025-11-27','2025-11-27','2025-11-27','Тільки в читальній залі',1,'3','24',NULL,'2025-11-27 11:09:56','2025-11-27 12:09:09',0);
/*!40000 ALTER TABLE `issuedbooks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `item_type` enum('book','collection') NOT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `librarians`
--

DROP TABLE IF EXISTS `librarians`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `librarians` (
  `librarian_id` int NOT NULL,
  `name` varchar(150) NOT NULL,
  `reading_room_id` int DEFAULT NULL,
  PRIMARY KEY (`librarian_id`),
  KEY `reading_room_id` (`reading_room_id`),
  CONSTRAINT `librarians_ibfk_1` FOREIGN KEY (`librarian_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `librarians_ibfk_2` FOREIGN KEY (`reading_room_id`) REFERENCES `readingrooms` (`room_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `librarians`
--

LOCK TABLES `librarians` WRITE;
/*!40000 ALTER TABLE `librarians` DISABLE KEYS */;
INSERT INTO `librarians` VALUES (24,'2',3),(46,'11',2),(49,'Інна',2),(52,'123',1),(67,'Богдан',1);
/*!40000 ALTER TABLE `librarians` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `libraries`
--

DROP TABLE IF EXISTS `libraries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `libraries` (
  `library_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`library_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libraries`
--

LOCK TABLES `libraries` WRITE;
/*!40000 ALTER TABLE `libraries` DISABLE KEYS */;
INSERT INTO `libraries` VALUES (1,'Головна бібліотека'),(2,'Міська бібліотека');
/*!40000 ALTER TABLE `libraries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `libraryvisits`
--

DROP TABLE IF EXISTS `libraryvisits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `libraryvisits` (
  `visit_id` int NOT NULL AUTO_INCREMENT,
  `reader_id` int NOT NULL,
  `visit_date` date NOT NULL,
  `visit_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `librarian_id` int NOT NULL,
  `room_id` int DEFAULT NULL,
  `visit_purpose` enum('Взяття книги','Повернення книги','Читання в залі','Консультація') DEFAULT 'Читання в залі',
  PRIMARY KEY (`visit_id`),
  KEY `reader_id` (`reader_id`),
  CONSTRAINT `libraryvisits_ibfk_1` FOREIGN KEY (`reader_id`) REFERENCES `readers` (`reader_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `libraryvisits`
--

LOCK TABLES `libraryvisits` WRITE;
/*!40000 ALTER TABLE `libraryvisits` DISABLE KEYS */;
INSERT INTO `libraryvisits` VALUES (1,1,'2025-08-27','2025-08-26 22:18:16',2,1,'Взяття книги'),(2,1,'2025-08-27','2025-07-26 23:04:04',2,1,'Взяття книги'),(3,24,'2025-06-27','2025-03-27 00:23:20',2,1,'Взяття книги'),(5,1,'2025-08-28','2025-08-28 12:49:44',2,1,'Взяття книги'),(6,1,'2025-08-28','2025-08-28 12:49:57',2,1,'Взяття книги'),(7,1,'2025-08-28','2025-08-28 12:51:51',2,1,'Взяття книги'),(8,1,'2025-08-28','2025-08-28 12:52:05',2,1,'Взяття книги'),(9,1,'2025-08-28','2025-08-28 13:36:45',2,1,'Взяття книги'),(10,1,'2025-09-19','2025-09-19 15:25:18',2,1,'Взяття книги'),(11,1,'2025-09-19','2025-09-19 15:25:44',24,3,'Взяття книги'),(12,1,'2025-10-27','2025-10-27 14:27:59',2,1,'Взяття книги'),(13,1,'2025-10-28','2025-10-28 13:58:14',2,1,'Взяття книги'),(14,1,'2025-10-28','2025-10-28 14:01:14',2,1,'Взяття книги'),(15,1,'2025-10-28','2025-10-28 15:10:12',2,1,'Взяття книги'),(16,33,'2025-10-28','2025-10-28 20:09:25',2,1,'Взяття книги'),(17,33,'2025-10-28','2025-10-28 20:10:23',2,1,'Взяття книги'),(18,1,'2025-10-29','2025-10-29 18:19:56',2,1,'Взяття книги'),(19,1,'2025-11-04','2025-11-04 12:12:44',24,3,'Взяття книги'),(20,1,'2025-11-04','2025-11-04 12:18:26',47,1,'Взяття книги'),(25,1,'2025-11-12','2025-11-12 21:22:45',24,3,'Взяття книги'),(27,1,'2025-11-15','2025-11-15 15:37:54',47,1,'Взяття книги'),(28,1,'2025-11-15','2025-11-15 15:38:07',47,1,'Взяття книги'),(30,1,'2025-11-19','2025-11-19 11:12:22',24,3,'Повернення книги'),(31,24,'2025-11-19','2025-11-19 11:13:33',24,3,'Повернення книги'),(34,23,'2025-11-27','2025-11-27 02:01:49',24,3,'Взяття книги'),(35,23,'2025-11-27','2025-11-27 10:29:29',24,3,'Взяття книги'),(36,1,'2025-11-27','2025-11-27 10:31:56',24,3,'Повернення книги'),(37,23,'2025-11-27','2025-11-27 10:33:17',24,3,'Взяття книги'),(38,23,'2025-11-27','2025-11-27 10:33:27',24,3,'Повернення книги'),(39,23,'2025-11-27','2025-11-27 10:33:46',24,3,'Взяття книги'),(40,23,'2025-11-27','2025-11-27 10:36:57',24,3,'Повернення книги'),(41,23,'2025-11-27','2025-11-27 10:37:07',24,3,'Взяття книги'),(42,23,'2025-11-27','2025-11-27 10:50:17',24,3,'Взяття книги'),(43,23,'2025-11-27','2025-11-27 10:51:28',24,3,'Взяття книги'),(44,23,'2025-11-27','2025-11-27 11:09:32',24,3,'Повернення книги'),(45,23,'2025-11-27','2025-11-27 11:09:35',24,3,'Повернення книги'),(46,23,'2025-11-27','2025-11-27 11:09:37',24,3,'Повернення книги'),(47,23,'2025-11-27','2025-11-27 11:09:41',24,3,'Повернення книги'),(48,23,'2025-11-27','2025-11-27 11:09:44',24,3,'Повернення книги'),(49,23,'2025-11-27','2025-11-27 11:09:56',24,3,'Взяття книги'),(50,23,'2025-11-27','2025-11-27 12:09:09',24,3,'Повернення книги');
/*!40000 ALTER TABLE `libraryvisits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `placements`
--

DROP TABLE IF EXISTS `placements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `placements` (
  `placement_id` int NOT NULL AUTO_INCREMENT,
  `book_id` int NOT NULL,
  `room_id` int NOT NULL,
  `shelf` varchar(50) DEFAULT NULL,
  `row` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`placement_id`),
  KEY `book_id` (`book_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `placements_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE,
  CONSTRAINT `placements_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `readingrooms` (`room_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `placements`
--

LOCK TABLES `placements` WRITE;
/*!40000 ALTER TABLE `placements` DISABLE KEYS */;
INSERT INTO `placements` VALUES (19,12,2,'B','4'),(47,23,2,'A','2'),(55,12,1,'C','3'),(56,12,2,'C','3'),(57,12,3,'C','3'),(58,12,1,'C','3'),(59,12,2,'C','3'),(60,12,3,'C','3'),(65,25,1,'B','1'),(72,27,1,'A','1'),(87,12,1,'A','3'),(88,12,2,'A','3'),(89,12,3,'A','3'),(99,12,1,'A','1'),(101,8,1,'C','2'),(102,15,1,'A','5'),(103,47,2,'С','3'),(106,7,1,'A','4'),(107,63,1,'C','5'),(108,63,2,'C','5'),(109,63,3,'C','5'),(110,61,1,'A','1'),(111,61,2,'A','1'),(112,61,3,'A','1'),(117,50,3,'С','8'),(118,65,1,'B','10'),(119,65,2,'B','10'),(120,65,3,'B','10'),(121,68,2,'C','2'),(122,64,1,'D','4'),(123,64,2,'D','4'),(124,64,3,'D','4'),(125,57,3,'C','2'),(126,18,3,'C','4');
/*!40000 ALTER TABLE `placements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `publishers`
--

DROP TABLE IF EXISTS `publishers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `publishers` (
  `publisher_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(500) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`publisher_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publishers`
--

LOCK TABLES `publishers` WRITE;
/*!40000 ALTER TABLE `publishers` DISABLE KEYS */;
INSERT INTO `publishers` VALUES (1,'Наукова думка','Київ, вул. Терещенківська, 4','+380441234567','info@naukova-dumka.ua','2025-08-28 10:57:12'),(2,'Видавництво \"Освіта\"','Київ, пр. Перемоги, 56','+380442345678','contact@osvita.ua','2025-08-28 10:57:12'),(3,'А-БА-БА-ГА-ЛА-МА-ГА','Київ, вул. Хрещатик, 32','+380443456789','books@ababagalamaga.ua','2025-08-28 10:57:12'),(4,'Фоліо','Харків, пл. Конституції, 1','+380571111111','info@folio.ua','2025-08-28 10:57:12'),(5,'Ранок','Харків, вул. Космічна, 21а','+380572222222','ranok@ranok.com.ua','2025-08-28 10:57:12');
/*!40000 ALTER TABLE `publishers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `readers`
--

DROP TABLE IF EXISTS `readers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `readers` (
  `reader_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `user_name` varchar(150) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `reader_type` enum('Студент','Викладач','Науковець','Інше') DEFAULT 'Студент',
  `university` varchar(255) DEFAULT NULL,
  `faculty` varchar(255) DEFAULT NULL,
  `organization` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`reader_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `readers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `readers`
--

LOCK TABLES `readers` WRITE;
/*!40000 ALTER TABLE `readers` DISABLE KEYS */;
INSERT INTO `readers` VALUES (1,1,'Vlad','вул. Шевченка, 10','Студент','КНУ','Факультет філології',NULL),(21,23,'1','1','Студент','1','1',NULL),(22,25,'3','3','Науковець',NULL,NULL,'3'),(23,26,'4','4','Студент','4','4',NULL),(24,27,'Влад','Голоовна','Студент','ЧНУ','ІФнТК',NULL),(25,28,'5','5','Студент','5','5',NULL),(27,30,'7','7','Студент','7','7',NULL),(29,32,'890','890','Студент','890','890',NULL),(30,36,'йцу','йцу','Студент','йцу','йцу',NULL),(33,43,'67','67','Студент','67','67',NULL),(34,44,'92','92','Студент','92','92',NULL),(35,48,'Влад','Головна 89','Студент','ЧНУ','ІНФТН',NULL),(37,54,'енгшщ','кенгш','Науковець',NULL,NULL,'3'),(38,55,'Ілон Макс','м.Чернівці вул. Комарова 14б','Студент','ЧНУ','ІФНТтаКН',NULL),(39,57,'!234','1234','Студент','1234','1234',NULL),(41,61,'Мудряк Євгеній Валентинович','м.Чернівці .вул.Головна 100','Студент','ЧНУ','Факультет фізичної культури',NULL),(44,66,'Сусла Владислав Валерійович','Вулю Головна 200','Студент','ЧНУ','Філологічний',NULL);
/*!40000 ALTER TABLE `readers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `readingrooms`
--

DROP TABLE IF EXISTS `readingrooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `readingrooms` (
  `room_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `access_type` enum('Тільки читання','З дозволом на виніс') DEFAULT 'Тільки читання',
  `library_id` int DEFAULT NULL,
  PRIMARY KEY (`room_id`),
  KEY `fk_library` (`library_id`),
  CONSTRAINT `fk_library` FOREIGN KEY (`library_id`) REFERENCES `libraries` (`library_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `readingrooms`
--

LOCK TABLES `readingrooms` WRITE;
/*!40000 ALTER TABLE `readingrooms` DISABLE KEYS */;
INSERT INTO `readingrooms` VALUES (1,'Головний читальний зал','З дозволом на виніс',1),(2,'Міський читальний зал','З дозволом на виніс',1),(3,'Науковий зал','З дозволом на виніс',2);
/*!40000 ALTER TABLE `readingrooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thinkbooks`
--

DROP TABLE IF EXISTS `thinkbooks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thinkbooks` (
  `issue_id` int NOT NULL AUTO_INCREMENT,
  `reader_id` int DEFAULT NULL,
  `book_id` int DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `actual_return_date` date DEFAULT NULL,
  `reading_place` enum('Тільки в читальній залі','У читальній залі і в дома') DEFAULT NULL,
  `returned` tinyint(1) DEFAULT NULL,
  `room_id` varchar(45) DEFAULT NULL,
  `librarian_id` varchar(45) DEFAULT NULL,
  `collection_id` int DEFAULT NULL,
  PRIMARY KEY (`issue_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thinkbooks`
--

LOCK TABLES `thinkbooks` WRITE;
/*!40000 ALTER TABLE `thinkbooks` DISABLE KEYS */;
INSERT INTO `thinkbooks` VALUES (1,1,13,'2025-08-28','2025-08-28',NULL,'Тільки в читальній залі',0,'1','2',NULL),(2,1,8,'2025-08-28','2025-08-28',NULL,'Тільки в читальній залі',0,'1','2',NULL),(3,1,15,'2025-09-19','2025-09-19',NULL,'Тільки в читальній залі',0,'1','2',NULL),(4,1,12,'2025-10-27','2025-10-27',NULL,'Тільки в читальній залі',0,'1','2',NULL),(5,1,27,'2025-10-28','2025-10-28',NULL,'Тільки в читальній залі',0,'1','2',NULL),(6,33,15,'2025-10-28','2025-10-28',NULL,'Тільки в читальній залі',0,'1','2',NULL),(7,1,29,'2025-10-29','2025-10-29',NULL,'Тільки в читальній залі',0,'1','2',NULL),(8,1,12,'2025-11-12','2025-11-12',NULL,'Тільки в читальній залі',0,'3','24',NULL),(9,1,25,'2025-11-15','2025-11-15',NULL,'Тільки в читальній залі',0,'1','47',NULL);
/*!40000 ALTER TABLE `thinkbooks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Learner','Reader','Librarian','Writer','Admin','Guest','Operator') DEFAULT 'Guest',
  `usercol` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Vlad','123','Reader',NULL),(2,'oles_gonchar','123','Writer',NULL),(3,'taras_shevchenko','password_hash','Writer',NULL),(4,'lesya_ukrainka','password_hash','Writer',NULL),(5,'admin','admin','Admin',NULL),(22,'kulish','123','Writer',NULL),(23,'1','1','Reader',NULL),(24,'2','2','Librarian',NULL),(25,'3','3','Reader',NULL),(26,'4','4','Reader',NULL),(27,'Влад','123','Reader',NULL),(28,'5','5','Reader',NULL),(30,'7','7','Reader',NULL),(32,'890','890','Reader',NULL),(36,'йцу','йцу','Reader',NULL),(39,'68','68','Admin',NULL),(40,'operator','operator','Operator',NULL),(42,'9','9999','Admin',NULL),(43,'67','67','Reader',NULL),(44,'92','92','Reader',NULL),(45,'123','123','Operator',NULL),(46,'11','11','Librarian',NULL),(48,'vlad00','1234','Reader',NULL),(49,'Інна','1234','Librarian',NULL),(50,'Костенко','9999','Writer',NULL),(51,'1234','4321','Writer',NULL),(52,'123333','1234','Librarian',NULL),(54,'нгшщ','6789','Reader',NULL),(55,'Ilon','12345678','Reader',NULL),(56,'Lana','12345','Guest','{\"requested_role\": \"Reader\", \"status\": \"pending\", \"name\": \"Lana Rouse\", \"address\": \"м. Чернівці вул.Головна 200\", \"reader_type\": \"Студент\", \"university\": \"ЧНУ\", \"faculty\": \"Педагогічний\", \"organization\": null}'),(57,'Dima','1234','Reader',NULL),(59,'Ilia','12345','Guest','{\"requested_role\": \"Reader\", \"status\": \"pending\", \"name\": \"Ілля\", \"address\": \"М. Чернівці, вул. Героїв Майдану 77а\", \"reader_type\": \"Студент\", \"university\": \"ЧНУ\", \"faculty\": \"ІН та ФТК\", \"organization\": null}'),(61,'Женя','12345','Reader',NULL),(66,'Владислав','1234','Reader',NULL),(67,'Богдан','1234','Librarian',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `v_active_issues`
--

DROP TABLE IF EXISTS `v_active_issues`;
/*!50001 DROP VIEW IF EXISTS `v_active_issues`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_active_issues` AS SELECT 
 1 AS `issue_id`,
 1 AS `reader_name`,
 1 AS `book_title`,
 1 AS `author_name`,
 1 AS `issue_date`,
 1 AS `return_date`,
 1 AS `days_overdue`,
 1 AS `reading_room`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_books_public`
--

DROP TABLE IF EXISTS `v_books_public`;
/*!50001 DROP VIEW IF EXISTS `v_books_public`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_books_public` AS SELECT 
 1 AS `book_id`,
 1 AS `title`,
 1 AS `author_name`,
 1 AS `country`,
 1 AS `category`,
 1 AS `year`,
 1 AS `languages`,
 1 AS `availability`,
 1 AS `access_type`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_library_statistics`
--

DROP TABLE IF EXISTS `v_library_statistics`;
/*!50001 DROP VIEW IF EXISTS `v_library_statistics`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_library_statistics` AS SELECT 
 1 AS `total_books`,
 1 AS `total_authors`,
 1 AS `total_readers`,
 1 AS `total_book_copies`,
 1 AS `currently_borrowed`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `writtenoffbooks`
--

DROP TABLE IF EXISTS `writtenoffbooks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `writtenoffbooks` (
  `writeoff_id` int NOT NULL AUTO_INCREMENT,
  `original_book_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `author_id` int NOT NULL,
  `category_id` int DEFAULT NULL,
  `year` year DEFAULT NULL,
  `languages` varchar(50) DEFAULT NULL,
  `access_type` enum('Тільки в читальній залі','У читальній залі і вдома') DEFAULT NULL,
  `inventory_number` varchar(50) DEFAULT NULL,
  `date_added` date DEFAULT NULL,
  `date_written_off` date DEFAULT NULL,
  `writeoff_reason` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`writeoff_id`),
  KEY `author_id` (`author_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `writtenoffbooks_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `authors` (`author_id`) ON DELETE CASCADE,
  CONSTRAINT `writtenoffbooks_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `writtenoffbooks`
--

LOCK TABLES `writtenoffbooks` WRITE;
/*!40000 ALTER TABLE `writtenoffbooks` DISABLE KEYS */;
INSERT INTO `writtenoffbooks` VALUES (1,16,'tre',1,8,2000,'Erhf]ycmrf','Тільки в читальній залі','INV-00007',NULL,'2025-08-23','нова редакція'),(2,17,'[ЗБІРКА] aio',3,5,1984,'Українська','Тільки в читальній залі','COLL-00007',NULL,'2025-08-28','Уа'),(3,19,'[ЗБІРКА] Золото карпат',1,8,1999,'Українська','У читальній залі і вдома','COLL-00008',NULL,'2025-08-28','фн'),(13,24,'11',1,3,2022,'украхнська','Тільки в читальній залі','INV-00012','2025-09-16','2025-09-16','11'),(14,20,'Океан',1,1,2001,'Українська','У читальній залі і вдома','INV-00008','2025-08-28','2025-09-16','Нова редакція'),(15,14,'Романс',4,4,1992,'Українська','У читальній залі і вдома','INV-00005','2025-03-21','2025-09-16','Редакція'),(16,22,'Осіннє сонце',1,5,1990,'Украхнська','Тільки в читальній залі','INV-00010','2025-08-28','2025-09-17','Оновлення'),(17,13,'Промені',1,5,1994,'Українська','У читальній залі і вдома','INV-00004','2020-04-24','2025-10-27','33'),(18,26,'uiii',1,1,2000,'Українська','У читальній залі і вдома','INV-00009','2025-10-27','2025-10-27','o'),(19,28,'[ЗБІРКА] Оресь',1,8,NULL,NULL,'У читальній залі і вдома','COLL-00011','2025-10-28','2025-10-28','09'),(20,30,'pyhon',1,3,2020,'Українська','У читальній залі і вдома','INV-00011','2025-10-28','2025-10-28','09'),(21,38,'[ЗБІРКА] 78',1,8,2000,'Українська','Тільки в читальній залі','COLL-BOOK-00022','2025-11-08','2025-11-13','68'),(22,36,'[ЗБІРКА] Еврика',1,NULL,2000,'Українстька','Тільки в читальній залі','COL-BOOK-00020','2025-11-08','2025-11-14','qq'),(23,40,'[ЗБІРКА] 223',1,8,2001,'Українська','У читальній залі і вдома','COLL-BOOK-00023','2025-11-12','2025-11-14','йй'),(24,33,'[ЗБІРКА] ЛАБ',4,5,2000,'Українська','Тільки в читальній залі','COLL-00013','2025-11-08','2025-11-14','22'),(25,39,'122',1,6,2000,'Українська','Тільки в читальній залі','INV-00019','2025-11-12','2025-11-14','33'),(26,21,'[ЗБІРКА] Інетерлюдія',1,8,2001,'Українська','Тільки в читальній залі','COLL-00009','2025-08-28','2025-11-14','333'),(27,44,'[ЗБІРКА] 22',1,5,2002,'Українська','Тільки в читальній залі','COLL-BOOK-00024','2025-11-12','2025-11-15','333'),(28,29,'[ЗБІРКА] Зор',3,8,2000,'Українська','Тільки в читальній залі','COLL-00012','2025-10-28','2025-11-15','11'),(29,43,'1',1,5,2000,'Українська','Тільки в читальній залі','INV-00023','2025-11-12','2025-11-15','редакція'),(30,45,'2020',5,3,2000,'Українська','Тільки в читальній залі','INV-00017','2025-11-15','2025-11-17','Стара редакція'),(31,42,'33',5,3,2000,'Українська','Тільки в читальній залі','INV-00022','2025-11-12','2025-11-17','33'),(32,32,'78',1,3,2000,'Укрпаїнська','Тільки в читальній залі','INV-00012','2025-11-05','2025-11-17','334'),(33,31,'Ребелія22',1,2,2025,'Українська','Тільки в читальній залі','INV-00011','2025-11-05','2025-11-17','321'),(34,49,'12321',1,3,1948,'123','Тільки в читальній залі','INV-00016','2025-11-17','2025-11-27','123'),(35,66,'[ЗБІРКА] Сьогодні',1,NULL,2001,'Україна','Тільки в читальній залі','COL-BOOK-00027','2025-11-27','2025-11-27','Редакція'),(36,58,'Сім струн',3,5,1961,'Українська','Тільки в читальній залі','INV-00025','2025-11-17','2025-11-27','Редакція'),(37,70,'23',4,3,2000,'Українська','Тільки в читальній залі','INV-00034','2025-11-27','2025-11-27','Редакція');
/*!40000 ALTER TABLE `writtenoffbooks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `v_active_issues`
--

/*!50001 DROP VIEW IF EXISTS `v_active_issues`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_active_issues` AS select `ib`.`issue_id` AS `issue_id`,`r`.`user_name` AS `reader_name`,`b`.`title` AS `book_title`,concat(`a`.`name`,' ',`a`.`surname`) AS `author_name`,`ib`.`issue_date` AS `issue_date`,`ib`.`return_date` AS `return_date`,(to_days(curdate()) - to_days(`ib`.`return_date`)) AS `days_overdue`,`rr`.`name` AS `reading_room` from ((((`issuedbooks` `ib` join `readers` `r` on((`ib`.`reader_id` = `r`.`reader_id`))) join `books` `b` on((`ib`.`book_id` = `b`.`book_id`))) join `authors` `a` on((`b`.`author_id` = `a`.`author_id`))) left join `readingrooms` `rr` on((`ib`.`room_id` = `rr`.`room_id`))) where (`ib`.`returned` = 0) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_books_public`
--

/*!50001 DROP VIEW IF EXISTS `v_books_public`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_books_public` AS select `b`.`book_id` AS `book_id`,`b`.`title` AS `title`,concat(`a`.`name`,' ',`a`.`surname`) AS `author_name`,`a`.`country` AS `country`,`c`.`name` AS `category`,`b`.`year` AS `year`,`b`.`languages` AS `languages`,(case when (`b`.`quantity` > 0) then 'Доступна' else 'Недоступна' end) AS `availability`,`b`.`access_type` AS `access_type` from ((`books` `b` join `authors` `a` on((`b`.`author_id` = `a`.`author_id`))) left join `categories` `c` on((`b`.`category_id` = `c`.`category_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_library_statistics`
--

/*!50001 DROP VIEW IF EXISTS `v_library_statistics`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_library_statistics` AS select (select count(0) from `books`) AS `total_books`,(select count(0) from `authors`) AS `total_authors`,(select count(0) from `readers`) AS `total_readers`,(select sum(`books`.`quantity`) from `books`) AS `total_book_copies`,(select count(0) from `issuedbooks` where (`issuedbooks`.`returned` = 0)) AS `currently_borrowed` */;
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

-- Dump completed on 2025-11-27 15:14:48
