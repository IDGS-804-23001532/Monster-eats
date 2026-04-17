-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: monster_eats_db
-- ------------------------------------------------------
-- Server version	9.5.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'bffeb25c-e5c8-11f0-bdee-c43d1ac472b8:1-2651';

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `caja`
--

DROP TABLE IF EXISTS `caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `caja` (
  `id_caja` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `saldo_actual` decimal(12,2) NOT NULL DEFAULT '0.00',
  `activa` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_caja`),
  UNIQUE KEY `nombre` (`nombre`),
  CONSTRAINT `chk_caja_saldo` CHECK ((`saldo_actual` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `caja`
--

LOCK TABLES `caja` WRITE;
/*!40000 ALTER TABLE `caja` DISABLE KEYS */;
INSERT INTO `caja` VALUES (1,'Caja Principal',2777.40,1);
/*!40000 ALTER TABLE `caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Bebidas'),(8,'Combos'),(10,'Desayunos'),(2,'Fuertes'),(4,'Hamburguesas'),(5,'Hot Dogs'),(9,'Papas'),(6,'Postres'),(7,'Snacks');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias_proveedor`
--

DROP TABLE IF EXISTS `categorias_proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias_proveedor` (
  `id_categoria_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_categoria_proveedor`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_proveedor`
--

LOCK TABLES `categorias_proveedor` WRITE;
/*!40000 ALTER TABLE `categorias_proveedor` DISABLE KEYS */;
INSERT INTO `categorias_proveedor` VALUES (1,'Abarrotes'),(4,'Bebidas'),(3,'Carnes'),(5,'Desechables'),(2,'Lácteos');
/*!40000 ALTER TABLE `categorias_proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `combos`
--

DROP TABLE IF EXISTS `combos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `combos` (
  `id_combo` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `precio_venta` decimal(10,2) NOT NULL,
  `imagen` varchar(255) DEFAULT 'default_combo.png',
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_combo`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combos`
--

LOCK TABLES `combos` WRITE;
/*!40000 ALTER TABLE `combos` DISABLE KEYS */;
INSERT INTO `combos` VALUES (1,'Combo Jujutsu','Dos haburguesas jujutsu y unas papas sukuna ',280.00,'Combo.png',1),(2,'Desayuno Monstruoso','¡El combo perfecto sí existe! Disfruta de un delicioso burrito bien servido, acompañado de papas crujientes y una refrescante agua de limón de 600ml. ¡Sabor real en cada bocado!',150.00,'Combo_desayuno.png',1);
/*!40000 ALTER TABLE `combos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras`
--

DROP TABLE IF EXISTS `compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras` (
  `id_compra` int NOT NULL AUTO_INCREMENT,
  `id_proveedor` int NOT NULL,
  `id_usuario` int NOT NULL,
  `fecha_compra` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) NOT NULL DEFAULT '0.00',
  `estado_compra` enum('Completada','Cancelada') NOT NULL DEFAULT 'Completada',
  PRIMARY KEY (`id_compra`),
  KEY `fk_compras_proveedor` (`id_proveedor`),
  KEY `fk_compras_usuario` (`id_usuario`),
  KEY `idx_compras_fecha` (`fecha_compra`),
  KEY `idx_compras_estado` (`estado_compra`),
  CONSTRAINT `fk_compras_proveedor` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`),
  CONSTRAINT `fk_compras_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `chk_compras_total` CHECK ((`total` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
INSERT INTO `compras` VALUES (3,13,8,'2026-04-13 19:29:54',144.00,'Completada'),(4,11,8,'2026-04-13 19:30:24',17.00,'Completada'),(5,11,8,'2026-04-13 19:31:10',0.00,'Cancelada'),(6,11,8,'2026-04-13 19:31:58',0.00,'Cancelada'),(7,11,8,'2026-04-13 19:33:01',0.00,'Cancelada'),(8,11,8,'2026-04-13 19:38:29',50.00,'Completada'),(9,11,8,'2026-04-13 19:43:04',40.00,'Completada'),(10,11,8,'2026-04-13 20:07:18',101.34,'Completada'),(11,11,8,'2026-04-14 01:38:03',34.00,'Completada'),(12,11,8,'2026-04-14 02:23:17',17.00,'Completada'),(13,11,8,'2026-04-14 02:24:29',17.00,'Completada'),(14,11,8,'2026-04-14 02:27:55',17.00,'Completada'),(15,11,8,'2026-04-14 02:30:04',40.00,'Completada'),(16,11,8,'2026-04-14 17:14:23',47.04,'Completada'),(17,13,8,'2026-04-14 17:45:49',100.00,'Completada'),(18,11,8,'2026-04-14 18:00:18',304.00,'Completada'),(19,11,8,'2026-04-14 23:38:07',67.20,'Completada'),(20,11,8,'2026-04-15 23:53:34',80.00,'Completada'),(21,11,8,'2026-04-16 00:00:39',179.00,'Completada'),(22,13,8,'2026-04-16 00:01:30',660.00,'Completada'),(23,11,8,'2026-04-16 00:04:13',630.00,'Completada'),(24,11,8,'2026-04-16 00:07:42',50.00,'Completada'),(25,11,8,'2026-04-16 00:28:25',80.00,'Completada'),(26,13,8,'2026-04-16 00:33:05',430.00,'Completada'),(27,12,8,'2026-04-16 00:34:00',50.00,'Completada'),(28,11,8,'2026-04-16 00:42:53',156.00,'Completada'),(29,11,8,'2026-04-16 00:43:57',60.00,'Completada'),(30,12,8,'2026-04-16 00:44:38',120.00,'Completada'),(31,11,8,'2026-04-16 00:46:05',54.90,'Completada'),(32,12,8,'2026-04-16 01:03:02',480.00,'Completada'),(33,11,8,'2026-04-16 01:07:33',90.00,'Completada'),(34,13,8,'2026-04-16 01:08:26',160.00,'Completada'),(35,11,8,'2026-04-16 11:55:14',34.00,'Completada'),(36,11,8,'2026-04-16 16:40:06',40.00,'Completada'),(37,11,8,'2026-04-16 16:42:44',40.00,'Completada'),(38,11,8,'2026-04-16 16:44:46',30.00,'Completada'),(39,11,8,'2026-04-16 16:45:45',40.00,'Completada'),(40,11,8,'2026-04-16 16:47:37',40.00,'Completada'),(41,11,8,'2026-04-16 16:54:06',40.00,'Completada'),(42,13,8,'2026-04-16 16:54:32',100.00,'Completada'),(43,11,8,'2026-04-16 16:56:22',302.40,'Completada'),(44,12,8,'2026-04-16 16:56:48',100.00,'Completada'),(45,11,14,'2026-04-16 19:46:31',60.00,'Cancelada'),(46,11,14,'2026-04-16 19:50:09',230.00,'Completada'),(47,12,14,'2026-04-16 19:58:47',37.00,'Completada');
/*!40000 ALTER TABLE `compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversion_unidades_insumo`
--

DROP TABLE IF EXISTS `conversion_unidades_insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversion_unidades_insumo` (
  `id_conversion` int NOT NULL AUTO_INCREMENT,
  `id_insumo` int NOT NULL,
  `id_unidad_compra` int NOT NULL,
  `cantidad_equivalente_base` decimal(12,4) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_conversion`),
  UNIQUE KEY `uq_conversion_insumo_unidad` (`id_insumo`,`id_unidad_compra`),
  KEY `fk_conversion_unidad` (`id_unidad_compra`),
  CONSTRAINT `fk_conversion_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`),
  CONSTRAINT `fk_conversion_unidad` FOREIGN KEY (`id_unidad_compra`) REFERENCES `unidades_medida` (`id_unidad_medida`),
  CONSTRAINT `chk_conversion_equivalencia` CHECK ((`cantidad_equivalente_base` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversion_unidades_insumo`
--

LOCK TABLES `conversion_unidades_insumo` WRITE;
/*!40000 ALTER TABLE `conversion_unidades_insumo` DISABLE KEYS */;
INSERT INTO `conversion_unidades_insumo` VALUES (9,15,7,20.0000,1),(10,16,6,500.0000,1),(11,19,6,10.0000,1),(12,20,6,12.0000,1),(13,23,6,1000.0000,1),(14,24,7,18.0000,1),(15,25,6,15.0000,1),(16,18,6,50.0000,1);
/*!40000 ALTER TABLE `conversion_unidades_insumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuenta`
--

DROP TABLE IF EXISTS `cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuenta` (
  `id_cuenta` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `num_cuenta` varchar(20) NOT NULL,
  `pin` char(4) NOT NULL,
  `saldo` decimal(12,2) NOT NULL DEFAULT '0.00',
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_cuenta`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  UNIQUE KEY `num_cuenta` (`num_cuenta`),
  CONSTRAINT `fk_cuenta_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `chk_cuenta_saldo` CHECK ((`saldo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuenta`
--

LOCK TABLES `cuenta` WRITE;
/*!40000 ALTER TABLE `cuenta` DISABLE KEYS */;
INSERT INTO `cuenta` VALUES (1,1,'1122334455667788','1234',4165.00,1),(2,7,'1234567890123456','1234',1670.10,1);
/*!40000 ALTER TABLE `cuenta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_combos`
--

DROP TABLE IF EXISTS `detalle_combos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_combos` (
  `id_detalle_combo` int NOT NULL AUTO_INCREMENT,
  `id_combo` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_detalle_combo`),
  KEY `id_combo` (`id_combo`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `detalle_combos_ibfk_1` FOREIGN KEY (`id_combo`) REFERENCES `combos` (`id_combo`) ON DELETE CASCADE,
  CONSTRAINT `detalle_combos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `chk_cantidad_detalle` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_combos`
--

LOCK TABLES `detalle_combos` WRITE;
/*!40000 ALTER TABLE `detalle_combos` DISABLE KEYS */;
INSERT INTO `detalle_combos` VALUES (3,1,1,2),(4,1,2,1),(7,2,3,1),(8,2,5,1),(9,2,6,1);
/*!40000 ALTER TABLE `detalle_combos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_compras`
--

DROP TABLE IF EXISTS `detalle_compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_compras` (
  `id_detalle_compra` int NOT NULL AUTO_INCREMENT,
  `id_compra` int NOT NULL,
  `id_insumo` int NOT NULL,
  `cantidad_comprada` decimal(10,4) NOT NULL,
  `id_unidad_medida` int NOT NULL,
  `costo_unitario` decimal(10,2) NOT NULL,
  `costo_subtotal` decimal(10,2) GENERATED ALWAYS AS ((`cantidad_comprada` * `costo_unitario`)) STORED,
  `cantidad_base` decimal(12,4) DEFAULT NULL,
  `costo_unitario_base` decimal(12,6) DEFAULT NULL,
  PRIMARY KEY (`id_detalle_compra`),
  UNIQUE KEY `uq_detalle_compras` (`id_compra`,`id_insumo`),
  KEY `fk_detalle_compras_insumo` (`id_insumo`),
  KEY `fk_detalle_compras_unidad` (`id_unidad_medida`),
  CONSTRAINT `fk_detalle_compras_compra` FOREIGN KEY (`id_compra`) REFERENCES `compras` (`id_compra`),
  CONSTRAINT `fk_detalle_compras_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`),
  CONSTRAINT `fk_detalle_compras_unidad` FOREIGN KEY (`id_unidad_medida`) REFERENCES `unidades_medida` (`id_unidad_medida`),
  CONSTRAINT `chk_detalle_compras_cantidad` CHECK ((`cantidad_comprada` > 0)),
  CONSTRAINT `chk_detalle_compras_costo` CHECK ((`costo_unitario` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_compras`
--

LOCK TABLES `detalle_compras` WRITE;
/*!40000 ALTER TABLE `detalle_compras` DISABLE KEYS */;
INSERT INTO `detalle_compras` (`id_detalle_compra`, `id_compra`, `id_insumo`, `cantidad_comprada`, `id_unidad_medida`, `costo_unitario`, `cantidad_base`, `costo_unitario_base`) VALUES (3,3,2,2400.0000,2,0.06,2400.0000,0.060000),(4,4,11,1.0000,3,17.00,1.0000,17.000000),(5,5,10,1000.0000,2,0.00,1000.0000,0.000000),(6,6,13,1000.0000,2,0.00,1000.0000,0.000000),(7,7,13,1000.0000,2,0.00,1000.0000,0.000000),(8,8,13,1000.0000,2,0.05,1000.0000,0.050000),(9,9,10,1000.0000,2,0.04,1000.0000,0.040000),(10,10,1,18.0000,5,5.63,18.0000,5.630000),(11,11,11,2.0000,3,17.00,2.0000,17.000000),(12,12,11,1.0000,3,17.00,1.0000,17.000000),(13,13,11,1.0000,3,17.00,1.0000,17.000000),(14,14,11,1.0000,3,17.00,1.0000,17.000000),(15,15,13,1000.0000,2,0.04,1000.0000,0.040000),(16,16,6,8.0000,5,5.88,8.0000,5.880000),(17,17,7,1000.0000,2,0.10,1000.0000,0.100000),(18,18,8,2900.0000,2,0.06,2900.0000,0.060000),(19,18,17,1000.0000,2,0.07,1000.0000,0.070000),(20,18,59,1000.0000,2,0.02,1000.0000,0.020000),(21,18,5,1000.0000,2,0.04,1000.0000,0.040000),(22,19,40,960.0000,2,0.07,960.0000,0.070000),(23,20,29,4000.0000,2,0.02,4000.0000,0.020000),(24,21,56,1.0000,1,39.00,1.0000,39.000000),(25,21,36,2000.0000,2,0.07,2000.0000,0.070000),(26,22,49,3000.0000,2,0.22,3000.0000,0.220000),(27,23,39,3000.0000,2,0.09,3000.0000,0.090000),(28,23,48,2000.0000,2,0.18,2000.0000,0.180000),(29,24,56,1000.0000,2,0.05,1000.0000,0.050000),(30,25,35,2000.0000,2,0.04,2000.0000,0.040000),(31,26,36,1000.0000,2,0.43,1000.0000,0.430000),(32,27,17,1000.0000,4,0.05,1000.0000,0.050000),(33,28,34,2000.0000,2,0.04,2000.0000,0.040000),(34,28,61,2.0000,1,38.00,2.0000,38.000000),(35,29,5,1000.0000,2,0.04,1000.0000,0.040000),(36,29,4,1000.0000,2,0.02,1000.0000,0.020000),(37,30,60,1000.0000,2,0.12,1000.0000,0.120000),(38,31,19,30.0000,5,1.83,30.0000,1.830000),(39,32,21,3000.0000,2,0.16,3000.0000,0.160000),(40,33,37,20.0000,5,4.50,20.0000,4.500000),(41,34,20,1000.0000,2,0.16,1000.0000,0.160000),(42,35,11,2.0000,3,17.00,2.0000,17.000000),(43,36,23,1000.0000,4,0.04,1000.0000,0.040000),(44,37,23,1000.0000,4,0.04,1000.0000,0.040000),(45,38,22,1000.0000,2,0.03,1000.0000,0.030000),(46,39,22,1000.0000,2,0.04,1000.0000,0.040000),(47,40,24,1000.0000,2,0.04,1000.0000,0.040000),(48,41,22,1000.0000,2,0.04,1000.0000,0.040000),(49,42,7,1000.0000,2,0.10,1000.0000,0.100000),(50,43,32,3780.0000,4,0.08,3780.0000,0.080000),(51,44,46,1000.0000,2,0.10,1000.0000,0.100000),(52,45,16,1000.0000,2,0.06,1000.0000,0.060000),(53,46,16,1000.0000,2,0.06,1000.0000,0.060000),(54,46,25,1000.0000,2,0.03,1000.0000,0.030000),(55,46,26,1000.0000,2,0.09,1000.0000,0.090000),(56,46,28,1000.0000,4,0.03,1000.0000,0.030000),(57,46,10,1000.0000,2,0.02,1000.0000,0.020000),(58,47,18,1.0000,3,37.00,1.0000,37.000000);
/*!40000 ALTER TABLE `detalle_compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_ventas`
--

DROP TABLE IF EXISTS `detalle_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_ventas` (
  `id_detalle` int NOT NULL AUTO_INCREMENT,
  `id_venta` int NOT NULL,
  `id_producto` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) GENERATED ALWAYS AS ((`cantidad` * `precio_unitario`)) STORED,
  `estado_cocina` enum('Pendiente','Preparando','Listo','Entregado') NOT NULL DEFAULT 'Pendiente',
  `id_combo` int DEFAULT NULL,
  PRIMARY KEY (`id_detalle`),
  UNIQUE KEY `uq_detalle_ventas` (`id_venta`,`id_producto`),
  KEY `fk_detalle_ventas_producto` (`id_producto`),
  KEY `fk_dv_combo` (`id_combo`),
  CONSTRAINT `fk_detalle_ventas_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `fk_detalle_ventas_venta` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `fk_dv_combo` FOREIGN KEY (`id_combo`) REFERENCES `combos` (`id_combo`),
  CONSTRAINT `chk_detalle_ventas_cantidad` CHECK ((`cantidad` > 0)),
  CONSTRAINT `chk_detalle_ventas_precio` CHECK ((`precio_unitario` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_ventas`
--

LOCK TABLES `detalle_ventas` WRITE;
/*!40000 ALTER TABLE `detalle_ventas` DISABLE KEYS */;
INSERT INTO `detalle_ventas` (`id_detalle`, `id_venta`, `id_producto`, `cantidad`, `precio_unitario`, `estado_cocina`, `id_combo`) VALUES (1,17,6,1,45.00,'Listo',NULL),(2,18,6,1,45.00,'Listo',NULL),(3,19,6,1,45.00,'Listo',NULL),(4,20,6,1,45.00,'Listo',NULL),(5,21,6,1,45.00,'Listo',NULL),(6,22,6,2,45.00,'Listo',NULL),(7,23,6,2,45.00,'Listo',NULL),(8,24,6,1,45.00,'Listo',NULL),(9,24,7,1,35.00,'Listo',NULL),(11,25,6,1,45.00,'Listo',NULL),(12,25,7,1,35.00,'Listo',NULL),(14,26,6,1,45.00,'Listo',NULL),(15,26,7,1,35.00,'Listo',NULL),(16,27,6,2,45.00,'Listo',NULL),(17,27,7,1,35.00,'Listo',NULL),(19,28,6,1,45.00,'Listo',NULL),(20,28,7,1,35.00,'Listo',NULL),(22,29,3,1,60.00,'Listo',NULL),(23,29,7,1,35.00,'Listo',NULL),(24,29,8,1,40.00,'Listo',NULL),(25,29,10,1,83.00,'Listo',NULL),(29,30,6,1,45.00,'Listo',NULL),(30,30,8,1,40.00,'Listo',NULL),(31,30,10,1,83.00,'Listo',NULL),(32,30,12,1,140.00,'Listo',NULL),(36,31,3,1,60.00,'Listo',NULL),(37,31,12,1,140.00,'Listo',NULL),(39,32,7,1,35.00,'Listo',NULL),(40,32,12,1,140.00,'Listo',NULL),(42,33,1,1,180.00,'Listo',NULL),(43,34,1,1,180.00,'Listo',NULL),(44,35,1,1,180.00,'Listo',NULL),(45,36,1,1,180.00,'Listo',NULL),(46,37,7,1,35.00,'Listo',NULL),(47,38,6,1,45.00,'Listo',NULL),(48,38,8,1,40.00,'Listo',NULL),(50,39,13,1,90.00,'Pendiente',NULL),(51,40,5,1,60.00,'Listo',NULL),(52,40,7,1,35.00,'Listo',NULL);
/*!40000 ALTER TABLE `detalle_ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_ventas_borrador`
--

DROP TABLE IF EXISTS `detalle_ventas_borrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_ventas_borrador` (
  `id_detalle_borrador` bigint NOT NULL AUTO_INCREMENT,
  `id_venta_borrador` bigint NOT NULL,
  `id_producto` int DEFAULT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `precio_unitario` decimal(10,2) NOT NULL,
  `descuento_unitario` decimal(10,2) NOT NULL DEFAULT '0.00',
  `id_combo` int DEFAULT NULL,
  PRIMARY KEY (`id_detalle_borrador`),
  UNIQUE KEY `uq_dvb` (`id_venta_borrador`,`id_producto`),
  KEY `fk_dvb_producto` (`id_producto`),
  KEY `fk_dvb_combo` (`id_combo`),
  CONSTRAINT `fk_dvb_borrador` FOREIGN KEY (`id_venta_borrador`) REFERENCES `ventas_borrador` (`id_venta_borrador`),
  CONSTRAINT `fk_dvb_combo` FOREIGN KEY (`id_combo`) REFERENCES `combos` (`id_combo`),
  CONSTRAINT `fk_dvb_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `chk_dvb_cantidad` CHECK ((`cantidad` > 0)),
  CONSTRAINT `chk_dvb_descuento` CHECK ((`descuento_unitario` >= 0)),
  CONSTRAINT `chk_dvb_precio` CHECK ((`precio_unitario` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_ventas_borrador`
--

LOCK TABLES `detalle_ventas_borrador` WRITE;
/*!40000 ALTER TABLE `detalle_ventas_borrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_ventas_borrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_precios_insumos`
--

DROP TABLE IF EXISTS `historial_precios_insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_precios_insumos` (
  `id_historial` int NOT NULL AUTO_INCREMENT,
  `id_insumo` int NOT NULL,
  `precio_anterior` decimal(10,2) DEFAULT NULL,
  `precio_nuevo` decimal(10,2) DEFAULT NULL,
  `accion` enum('NUEVO','MODIFICACION','ELIMINADO') NOT NULL,
  `fecha_cambio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id_historial`),
  KEY `fk_historial_insumo` (`id_insumo`),
  KEY `fk_historial_usuario` (`id_usuario`),
  CONSTRAINT `fk_historial_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`),
  CONSTRAINT `fk_historial_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_precios_insumos`
--

LOCK TABLES `historial_precios_insumos` WRITE;
/*!40000 ALTER TABLE `historial_precios_insumos` DISABLE KEYS */;
/*!40000 ALTER TABLE `historial_precios_insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `id_insumo` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `id_unidad_medida` int NOT NULL,
  `costo_unitario` decimal(10,2) NOT NULL,
  `porcentaje_merma` decimal(5,2) NOT NULL DEFAULT '0.00',
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_insumo`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `fk_insumos_unidad` (`id_unidad_medida`),
  KEY `idx_insumos_nombre` (`nombre`),
  KEY `idx_insumos_activo` (`activo`),
  CONSTRAINT `fk_insumos_unidad` FOREIGN KEY (`id_unidad_medida`) REFERENCES `unidades_medida` (`id_unidad_medida`),
  CONSTRAINT `chk_insumos_costo_unitario` CHECK ((`costo_unitario` >= 0)),
  CONSTRAINT `chk_insumos_porcentaje_merma` CHECK (((`porcentaje_merma` >= 0) and (`porcentaje_merma` <= 100)))
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
INSERT INTO `insumos` VALUES (1,'Pan para hamburguesa',5,5.63,0.02,1),(2,'Carne para hamburguesa',2,0.06,0.10,1),(3,'Queso amarillo',2,0.22,0.05,1),(4,'Lechuga',2,0.02,0.15,1),(5,'Jitomate',2,0.04,0.12,1),(6,'Pan para hot dog',5,5.88,0.02,1),(7,'Salchicha',2,0.10,0.03,1),(8,'Mostaza',2,0.06,0.01,1),(9,'Catsup',4,0.02,0.01,1),(10,'Azucar',2,0.02,0.02,1),(11,'Agua',3,17.00,0.00,1),(12,'Pulpa de fresa',2,0.14,0.08,1),(13,'Limon',2,0.02,0.15,1),(14,'Flor de jamaica',2,0.12,0.10,1),(15,'Pulpa de tamarindo',2,0.13,0.08,1),(16,'Fresa',2,0.06,0.12,1),(17,'Crema',4,0.06,0.05,1),(18,'Lechera',3,37.00,0.03,1),(19,'Tortilla de harina',5,1.83,0.02,1),(20,'Jamon',2,0.16,0.05,1),(21,'Queso Oaxaca',2,0.16,0.05,1),(22,'Papa',2,0.04,0.20,1),(23,'Aceite Vegetal',4,0.04,0.10,1),(24,'Sal',2,0.04,0.01,1),(25,'Platano',2,0.03,0.15,1),(26,'Granola',2,0.09,0.03,1),(27,'Cafe molido',2,0.25,0.02,1),(28,'Leche',4,0.03,0.03,1),(29,'Lechuga romana',2,0.02,0.15,1),(30,'Pepino',2,0.07,0.10,1),(31,'Zanahoria',2,0.05,0.08,1),(32,'Aderezo',4,0.08,0.02,1),(33,'Tortilla grande',1,3.50,0.02,1),(34,'Frijol Negro',2,0.04,0.05,1),(35,'Arroz',2,0.04,0.05,1),(36,'Carne deshebrada',2,0.19,0.10,1),(37,'Bolillo',5,4.50,0.02,1),(38,'Milanesa',2,0.18,0.10,1),(39,'Aguacate',2,0.09,0.20,1),(40,'Mayonesa',2,0.07,0.02,1),(41,'Pan brioche',1,6.50,0.02,1),(42,'Pan artesanal integral',1,7.00,0.02,1),(43,'Carne Angus',2,0.28,0.08,1),(44,'Carne BBQ',2,0.26,0.08,1),(45,'Pechuga de pollo empanizada',2,0.22,0.06,1),(46,'Queso cheddar',2,0.10,0.04,1),(47,'Queso suizo',2,0.26,0.04,1),(48,'Queso azul',2,0.18,0.05,1),(49,'Tocino',2,0.22,0.05,1),(50,'Cebolla caramelizada',2,0.18,0.10,1),(51,'Champiñones',2,0.16,0.12,1),(52,'Pepinillos',2,0.12,0.05,1),(53,'Salsa BBQ',4,0.05,0.02,1),(54,'Salsa chipotle',3,0.06,0.02,1),(55,'Aderezo especial',3,0.07,0.02,1),(56,'Huevo',2,0.09,0.02,1),(57,'Aros de cebolla',2,0.15,0.08,1),(58,'Coca Cola',5,25.00,5.00,1),(59,'Cebolla',2,0.02,5.00,1),(60,'Queso Rallado',2,0.12,2.00,1),(61,'Frijol Peruano',1,38.00,2.00,1);
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_insumos`
--

DROP TABLE IF EXISTS `inventario_insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_insumos` (
  `id_inventario_insumo` int NOT NULL AUTO_INCREMENT,
  `id_lote` int NOT NULL,
  `nivel_minimo` decimal(10,4) DEFAULT NULL,
  `ubicacion_pasillo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_inventario_insumo`),
  UNIQUE KEY `id_lote` (`id_lote`),
  CONSTRAINT `fk_inventario_lote` FOREIGN KEY (`id_lote`) REFERENCES `lotes_insumo` (`id_lote`) ON DELETE CASCADE,
  CONSTRAINT `chk_inventario_insumos_nivel` CHECK (((`nivel_minimo` is null) or (`nivel_minimo` >= 0)))
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_insumos`
--

LOCK TABLES `inventario_insumos` WRITE;
/*!40000 ALTER TABLE `inventario_insumos` DISABLE KEYS */;
INSERT INTO `inventario_insumos` VALUES (1,3,NULL,NULL),(2,4,NULL,NULL),(3,5,NULL,NULL),(4,6,NULL,NULL),(5,7,NULL,NULL),(6,8,NULL,NULL),(7,9,NULL,NULL),(8,10,NULL,NULL),(9,11,NULL,NULL),(10,12,NULL,NULL),(11,13,NULL,NULL),(12,14,NULL,NULL),(13,15,NULL,NULL),(14,16,NULL,NULL),(15,17,NULL,NULL),(16,18,NULL,NULL),(17,19,NULL,NULL),(18,20,NULL,NULL),(19,21,NULL,NULL),(20,22,NULL,NULL),(21,23,NULL,NULL),(22,24,NULL,NULL),(23,25,NULL,NULL),(24,26,NULL,NULL),(25,27,NULL,NULL),(26,28,NULL,NULL),(27,29,NULL,NULL),(28,30,NULL,NULL),(29,31,NULL,NULL),(30,32,NULL,NULL),(31,33,NULL,NULL),(32,34,NULL,NULL),(33,35,NULL,NULL),(34,36,NULL,NULL),(35,37,NULL,NULL),(36,38,NULL,NULL),(37,39,NULL,NULL),(38,40,NULL,NULL),(39,41,NULL,NULL),(40,42,NULL,NULL),(41,43,NULL,NULL),(42,44,NULL,NULL),(43,45,NULL,NULL),(44,46,NULL,NULL),(45,47,NULL,NULL),(46,48,NULL,NULL),(47,49,NULL,NULL),(48,50,NULL,NULL),(49,51,NULL,NULL),(50,52,NULL,NULL),(51,53,NULL,NULL),(52,54,NULL,NULL),(53,55,NULL,NULL),(54,56,NULL,NULL),(55,57,NULL,NULL),(56,58,NULL,NULL);
/*!40000 ALTER TABLE `inventario_insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario_productos`
--

DROP TABLE IF EXISTS `inventario_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario_productos` (
  `id_inventario_prod` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `stock_actual` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_inventario_prod`),
  UNIQUE KEY `uq_inventario_productos` (`id_producto`),
  CONSTRAINT `fk_inventario_productos_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `chk_inventario_productos_stock` CHECK ((`stock_actual` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario_productos`
--

LOCK TABLES `inventario_productos` WRITE;
/*!40000 ALTER TABLE `inventario_productos` DISABLE KEYS */;
INSERT INTO `inventario_productos` VALUES (1,6,0);
/*!40000 ALTER TABLE `inventario_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lotes_insumo`
--

DROP TABLE IF EXISTS `lotes_insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lotes_insumo` (
  `id_lote` int NOT NULL AUTO_INCREMENT,
  `id_insumo` int DEFAULT NULL,
  `id_detalle_compra` int DEFAULT NULL,
  `cantidad_inicial` decimal(10,4) DEFAULT NULL,
  `cantidad_disponible` decimal(10,4) DEFAULT NULL,
  `fecha_caducidad` date DEFAULT NULL,
  `fecha_ingreso` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_lote`),
  KEY `id_detalle_compra` (`id_detalle_compra`),
  KEY `idx_lotes_insumo` (`id_insumo`),
  KEY `idx_lotes_caducidad` (`fecha_caducidad`),
  CONSTRAINT `lotes_insumo_ibfk_1` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`),
  CONSTRAINT `lotes_insumo_ibfk_2` FOREIGN KEY (`id_detalle_compra`) REFERENCES `detalle_compras` (`id_detalle_compra`),
  CONSTRAINT `lotes_insumo_chk_1` CHECK ((`cantidad_inicial` >= 0)),
  CONSTRAINT `lotes_insumo_chk_2` CHECK ((`cantidad_disponible` >= 0)),
  CONSTRAINT `lotes_insumo_chk_3` CHECK ((`cantidad_disponible` <= `cantidad_inicial`))
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lotes_insumo`
--

LOCK TABLES `lotes_insumo` WRITE;
/*!40000 ALTER TABLE `lotes_insumo` DISABLE KEYS */;
INSERT INTO `lotes_insumo` VALUES (3,2,3,2400.0000,2400.0000,'2026-04-20','2026-04-13 19:29:54'),(4,11,4,1.0000,0.0000,'2026-04-30','2026-04-13 19:30:24'),(5,10,5,1000.0000,0.0000,'2026-11-18','2026-04-13 19:31:10'),(6,13,6,1000.0000,0.0000,'2026-04-20','2026-04-13 19:31:58'),(7,13,7,1000.0000,0.0000,'2026-04-20','2026-04-13 19:33:01'),(8,13,8,1000.0000,0.0000,'2026-04-20','2026-04-13 19:38:29'),(9,10,9,1000.0000,450.0000,'2026-07-13','2026-04-13 19:43:04'),(10,1,10,18.0000,13.0000,'2026-04-27','2026-04-13 20:07:18'),(11,11,11,2.0000,0.0000,'2026-04-24','2026-04-14 01:38:03'),(12,11,12,1.0000,0.0000,'2026-04-29','2026-04-14 02:23:17'),(13,11,13,1.0000,0.0000,'2026-04-21','2026-04-14 02:24:29'),(14,11,14,1.0000,0.0000,'2026-04-23','2026-04-14 02:27:55'),(15,13,15,1000.0000,500.0000,'2026-04-21','2026-04-14 02:30:04'),(16,6,16,8.0000,1.0000,'2026-04-28','2026-04-14 17:14:23'),(17,7,17,1000.0000,700.0000,'2026-04-21','2026-04-14 17:45:49'),(18,8,18,2900.0000,2795.0000,'2026-04-30','2026-04-14 18:00:18'),(19,17,19,1000.0000,955.0000,'2026-04-30','2026-04-14 18:00:18'),(20,59,20,1000.0000,605.0000,'2026-04-21','2026-04-14 18:00:18'),(21,5,21,1000.0000,850.0000,'2026-04-30','2026-04-14 18:00:18'),(22,40,22,960.0000,825.0000,'2026-04-30','2026-04-14 23:38:07'),(23,29,23,4000.0000,3700.0000,'2026-04-22','2026-04-15 23:53:34'),(24,56,24,1.0000,0.0000,'2026-04-22','2026-04-16 00:00:39'),(25,36,25,2000.0000,1480.0000,'2026-04-20','2026-04-16 00:00:39'),(26,49,26,3000.0000,2940.0000,'2026-04-20','2026-04-16 00:01:30'),(27,39,27,3000.0000,2700.0000,'2026-04-19','2026-04-16 00:04:13'),(28,48,28,2000.0000,1940.0000,'2026-04-22','2026-04-16 00:04:13'),(29,56,29,1000.0000,821.0000,'2026-04-23','2026-04-16 00:07:42'),(30,35,30,2000.0000,1620.0000,'2026-04-30','2026-04-16 00:28:25'),(31,36,31,1000.0000,1000.0000,'2026-04-24','2026-04-16 00:33:05'),(32,17,32,1000.0000,870.0000,'2026-04-23','2026-04-16 00:34:00'),(33,34,33,2000.0000,1900.0000,'2026-04-23','2026-04-16 00:42:53'),(34,61,34,2.0000,2.0000,'2026-04-23','2026-04-16 00:42:53'),(35,5,35,1000.0000,670.0000,'2026-04-23','2026-04-16 00:43:57'),(36,4,36,1000.0000,900.0000,'2026-04-23','2026-04-16 00:43:57'),(37,60,37,1000.0000,940.0000,'2026-04-25','2026-04-16 00:44:38'),(38,19,38,30.0000,25.0000,'2026-05-06','2026-04-16 00:46:05'),(39,21,39,3000.0000,2750.0000,'2026-04-30','2026-04-16 01:03:02'),(40,37,40,20.0000,18.0000,'2026-04-18','2026-04-16 01:07:33'),(41,20,41,1000.0000,720.0000,'2026-04-27','2026-04-16 01:08:26'),(42,11,42,2.0000,1.8000,'2026-04-30','2026-04-16 11:55:14'),(43,23,43,1000.0000,1000.0000,'2026-06-16','2026-04-16 16:40:06'),(44,23,44,1000.0000,950.0000,'2026-04-26','2026-04-16 16:42:44'),(45,22,45,1000.0000,1000.0000,'2026-04-23','2026-04-16 16:44:46'),(46,22,46,1000.0000,1000.0000,'2026-04-23','2026-04-16 16:45:45'),(47,24,47,1000.0000,995.0000,'2027-05-16','2026-04-16 16:47:37'),(48,22,48,1000.0000,850.0000,'2026-04-18','2026-04-16 16:54:06'),(49,7,49,1000.0000,950.0000,'2026-04-18','2026-04-16 16:54:32'),(50,32,50,3780.0000,3780.0000,'2026-04-23','2026-04-16 16:56:22'),(51,46,51,1000.0000,1000.0000,'2026-04-22','2026-04-16 16:56:48'),(52,16,52,1000.0000,0.0000,'2026-04-22','2026-04-16 19:46:31'),(53,16,53,1000.0000,1000.0000,'2026-04-22','2026-04-16 19:50:09'),(54,25,54,1000.0000,1000.0000,'2026-04-27','2026-04-16 19:50:09'),(55,26,55,1000.0000,1000.0000,'2026-04-21','2026-04-16 19:50:09'),(56,28,56,1000.0000,1000.0000,'2026-04-28','2026-04-16 19:50:09'),(57,10,57,1000.0000,1000.0000,'2026-04-30','2026-04-16 19:50:09'),(58,18,58,1.0000,1.0000,'2026-04-28','2026-04-16 19:58:47');
/*!40000 ALTER TABLE `lotes_insumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mermas_log`
--

DROP TABLE IF EXISTS `mermas_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mermas_log` (
  `id_merma` int NOT NULL AUTO_INCREMENT,
  `id_insumo` int NOT NULL,
  `cantidad` decimal(10,4) NOT NULL,
  `fecha_baja` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `motivo` varchar(255) NOT NULL,
  `id_usuario` int NOT NULL,
  `id_lote` int DEFAULT NULL,
  PRIMARY KEY (`id_merma`),
  KEY `fk_mermas_insumo` (`id_insumo`),
  KEY `fk_mermas_usuario` (`id_usuario`),
  KEY `fk_mermas_lote` (`id_lote`),
  KEY `idx_mermas_fecha` (`fecha_baja`),
  CONSTRAINT `fk_mermas_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`),
  CONSTRAINT `fk_mermas_lote` FOREIGN KEY (`id_lote`) REFERENCES `lotes_insumo` (`id_lote`),
  CONSTRAINT `fk_mermas_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `chk_mermas_cantidad` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mermas_log`
--

LOCK TABLES `mermas_log` WRITE;
/*!40000 ALTER TABLE `mermas_log` DISABLE KEYS */;
INSERT INTO `mermas_log` VALUES (1,11,0.1000,'2026-04-14 17:09:09','Se contamino el agua ',8,13),(2,35,100.0000,'2026-04-16 19:51:08','contamino',14,30);
/*!40000 ALTER TABLE `mermas_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metodos_pago`
--

DROP TABLE IF EXISTS `metodos_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metodos_pago` (
  `id_metodo_pago` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  PRIMARY KEY (`id_metodo_pago`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metodos_pago`
--

LOCK TABLES `metodos_pago` WRITE;
/*!40000 ALTER TABLE `metodos_pago` DISABLE KEYS */;
INSERT INTO `metodos_pago` VALUES (1,'Efectivo'),(2,'Tarjeta');
/*!40000 ALTER TABLE `metodos_pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_caja`
--

DROP TABLE IF EXISTS `movimientos_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_caja` (
  `id_movimiento_caja` int NOT NULL AUTO_INCREMENT,
  `id_caja` int NOT NULL,
  `id_venta` int DEFAULT NULL,
  `id_usuario` int NOT NULL,
  `tipo_movimiento` enum('FONDO_INICIAL','ENTRADA_VENTA','SALIDA_CAMBIO','SALIDA_GASTO','AJUSTE') NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `saldo_anterior` decimal(12,2) NOT NULL,
  `saldo_nuevo` decimal(12,2) NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `fecha_movimiento` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_movimiento_caja`),
  KEY `fk_mov_caja_caja` (`id_caja`),
  KEY `fk_mov_caja_venta` (`id_venta`),
  KEY `fk_mov_caja_usuario` (`id_usuario`),
  KEY `idx_mov_caja_fecha` (`fecha_movimiento`),
  KEY `idx_mov_caja_tipo` (`tipo_movimiento`),
  CONSTRAINT `fk_mov_caja_caja` FOREIGN KEY (`id_caja`) REFERENCES `caja` (`id_caja`),
  CONSTRAINT `fk_mov_caja_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `fk_mov_caja_venta` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `chk_mov_caja_monto` CHECK ((`monto` > 0)),
  CONSTRAINT `chk_mov_caja_saldo_anterior` CHECK ((`saldo_anterior` >= 0)),
  CONSTRAINT `chk_mov_caja_saldo_nuevo` CHECK ((`saldo_nuevo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_caja`
--

LOCK TABLES `movimientos_caja` WRITE;
/*!40000 ALTER TABLE `movimientos_caja` DISABLE KEYS */;
INSERT INTO `movimientos_caja` VALUES (1,1,17,8,'ENTRADA_VENTA',100.00,1742.40,1842.40,'Pago recibido venta #17','2026-04-14 01:32:39'),(2,1,17,8,'SALIDA_CAMBIO',55.00,1842.40,1787.40,'Cambio entregado venta #17','2026-04-14 01:32:39'),(3,1,18,8,'ENTRADA_VENTA',50.00,1787.40,1837.40,'Pago recibido venta #18','2026-04-14 01:56:44'),(4,1,18,8,'SALIDA_CAMBIO',5.00,1837.40,1832.40,'Cambio entregado venta #18','2026-04-14 01:56:44'),(5,1,19,8,'ENTRADA_VENTA',50.00,1832.40,1882.40,'Pago recibido venta #19','2026-04-14 02:22:05'),(6,1,19,8,'SALIDA_CAMBIO',5.00,1882.40,1877.40,'Cambio entregado venta #19','2026-04-14 02:22:05'),(7,1,20,8,'ENTRADA_VENTA',50.00,1877.40,1927.40,'Pago recibido venta #20','2026-04-14 02:27:22'),(8,1,20,8,'SALIDA_CAMBIO',5.00,1927.40,1922.40,'Cambio entregado venta #20','2026-04-14 02:27:22'),(9,1,21,8,'ENTRADA_VENTA',50.00,1922.40,1972.40,'Pago recibido venta #21','2026-04-14 18:04:42'),(10,1,21,8,'SALIDA_CAMBIO',5.00,1972.40,1967.40,'Cambio entregado venta #21','2026-04-14 18:04:42'),(11,1,22,8,'ENTRADA_VENTA',100.00,1967.40,2067.40,'Pago recibido venta #22','2026-04-14 23:39:58'),(12,1,22,8,'SALIDA_CAMBIO',10.00,2067.40,2057.40,'Cambio entregado venta #22','2026-04-14 23:39:58'),(13,1,23,8,'ENTRADA_VENTA',100.00,2057.40,2157.40,'Pago recibido venta #23','2026-04-14 23:46:30'),(14,1,23,8,'SALIDA_CAMBIO',10.00,2157.40,2147.40,'Cambio entregado venta #23','2026-04-14 23:46:30'),(15,1,24,8,'ENTRADA_VENTA',100.00,2147.40,2247.40,'Pago recibido venta #24','2026-04-15 00:17:21'),(16,1,24,8,'SALIDA_CAMBIO',20.00,2247.40,2227.40,'Cambio entregado venta #24','2026-04-15 00:17:21'),(17,1,25,8,'ENTRADA_VENTA',100.00,2227.40,2327.40,'Pago recibido venta #25','2026-04-15 00:41:57'),(18,1,25,8,'SALIDA_CAMBIO',20.00,2327.40,2307.40,'Cambio entregado venta #25','2026-04-15 00:41:57'),(19,1,26,8,'ENTRADA_VENTA',100.00,2307.40,2407.40,'Pago recibido venta #26','2026-04-15 01:29:08'),(20,1,26,8,'SALIDA_CAMBIO',20.00,2407.40,2387.40,'Cambio entregado venta #26','2026-04-15 01:29:08'),(21,1,27,8,'ENTRADA_VENTA',150.00,2387.40,2537.40,'Pago recibido venta #27','2026-04-15 21:49:43'),(22,1,27,8,'SALIDA_CAMBIO',25.00,2537.40,2512.40,'Cambio entregado venta #27','2026-04-15 21:49:43'),(23,1,28,8,'ENTRADA_VENTA',100.00,2512.40,2612.40,'Pago recibido venta #28','2026-04-15 21:52:35'),(24,1,28,8,'SALIDA_CAMBIO',20.00,2612.40,2592.40,'Cambio entregado venta #28','2026-04-15 21:52:35'),(25,1,29,8,'ENTRADA_VENTA',250.00,2592.40,2842.40,'Pago recibido venta #29','2026-04-16 01:00:02'),(26,1,29,8,'SALIDA_CAMBIO',32.00,2842.40,2810.40,'Cambio entregado venta #29','2026-04-16 01:00:02'),(27,1,30,8,'ENTRADA_VENTA',320.00,2810.40,3130.40,'Pago recibido venta #30','2026-04-16 01:23:47'),(28,1,30,8,'SALIDA_CAMBIO',12.00,3130.40,3118.40,'Cambio entregado venta #30','2026-04-16 01:23:47'),(29,1,31,8,'ENTRADA_VENTA',200.00,3118.40,3318.40,'Pago recibido venta #31','2026-04-16 03:02:52'),(30,1,NULL,8,'AJUSTE',726.00,3318.40,2592.40,'Corte de caja - Efectivo retirado del 16/04/2026','2026-04-16 10:58:36'),(31,1,39,15,'ENTRADA_VENTA',100.00,2592.40,2692.40,'Pago recibido venta #39','2026-04-16 19:56:15'),(32,1,39,15,'SALIDA_CAMBIO',10.00,2692.40,2682.40,'Cambio entregado venta #39','2026-04-16 19:56:15'),(33,1,40,15,'ENTRADA_VENTA',100.00,2682.40,2782.40,'Pago recibido venta #40','2026-04-16 20:01:16'),(34,1,40,15,'SALIDA_CAMBIO',5.00,2782.40,2777.40,'Cambio entregado venta #40','2026-04-16 20:01:16');
/*!40000 ALTER TABLE `movimientos_caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_cuenta`
--

DROP TABLE IF EXISTS `movimientos_cuenta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_cuenta` (
  `id_movimiento_cuenta` int NOT NULL AUTO_INCREMENT,
  `id_cuenta` int NOT NULL,
  `id_venta` int DEFAULT NULL,
  `tipo_movimiento` enum('ABONO','CARGO','REVERSO','AJUSTE') NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `saldo_anterior` decimal(12,2) NOT NULL,
  `saldo_nuevo` decimal(12,2) NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `fecha_movimiento` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_movimiento_cuenta`),
  KEY `fk_mov_cta_cuenta` (`id_cuenta`),
  KEY `fk_mov_cta_venta` (`id_venta`),
  CONSTRAINT `fk_mov_cta_cuenta` FOREIGN KEY (`id_cuenta`) REFERENCES `cuenta` (`id_cuenta`),
  CONSTRAINT `fk_mov_cta_venta` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `chk_mov_cta_monto` CHECK ((`monto` > 0)),
  CONSTRAINT `chk_mov_cta_saldo_anterior` CHECK ((`saldo_anterior` >= 0)),
  CONSTRAINT `chk_mov_cta_saldo_nuevo` CHECK ((`saldo_nuevo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_cuenta`
--

LOCK TABLES `movimientos_cuenta` WRITE;
/*!40000 ALTER TABLE `movimientos_cuenta` DISABLE KEYS */;
INSERT INTO `movimientos_cuenta` VALUES (1,1,32,'CARGO',175.00,5000.00,4825.00,'Venta #32','2026-04-16 03:07:33'),(2,1,33,'CARGO',180.00,4825.00,4645.00,'Venta #33','2026-04-16 03:08:47'),(3,1,34,'CARGO',180.00,4645.00,4465.00,'Venta #34','2026-04-16 03:10:36'),(4,2,35,'CARGO',180.00,1850.10,1670.10,'Venta #35','2026-04-16 03:21:55'),(5,1,36,'CARGO',180.00,4465.00,4285.00,'Venta #36','2026-04-16 03:24:37'),(6,1,37,'CARGO',35.00,4285.00,4250.00,'Venta #37','2026-04-16 03:25:31'),(7,1,38,'CARGO',85.00,4250.00,4165.00,'Venta #38','2026-04-16 11:59:45');
/*!40000 ALTER TABLE `movimientos_cuenta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_inventario_insumos`
--

DROP TABLE IF EXISTS `movimientos_inventario_insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_inventario_insumos` (
  `id_movimiento_insumo` int NOT NULL AUTO_INCREMENT,
  `id_insumo` int NOT NULL,
  `tipo_movimiento` enum('ENTRADA_COMPRA','SALIDA_PRODUCCION','SALIDA_MERMA','AJUSTE_MANUAL','REVERSO_COMPRA') NOT NULL,
  `cantidad` decimal(12,4) NOT NULL,
  `stock_anterior` decimal(12,4) NOT NULL,
  `stock_nuevo` decimal(12,4) NOT NULL,
  `referencia_tabla` varchar(50) DEFAULT NULL,
  `referencia_id` int DEFAULT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `id_usuario` int NOT NULL,
  `id_lote` int DEFAULT NULL,
  `fecha_movimiento` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_movimiento_insumo`),
  KEY `fk_mov_insumo_insumo` (`id_insumo`),
  KEY `fk_mov_insumo_usuario` (`id_usuario`),
  KEY `fk_mov_lote` (`id_lote`),
  KEY `idx_mov_insumos_fecha` (`fecha_movimiento`),
  KEY `idx_mov_insumos_tipo` (`tipo_movimiento`),
  CONSTRAINT `fk_mov_insumo_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`),
  CONSTRAINT `fk_mov_insumo_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `fk_mov_lote` FOREIGN KEY (`id_lote`) REFERENCES `lotes_insumo` (`id_lote`),
  CONSTRAINT `chk_mov_insumo_cantidad` CHECK ((`cantidad` > 0)),
  CONSTRAINT `chk_mov_insumo_stock_anterior` CHECK ((`stock_anterior` >= 0)),
  CONSTRAINT `chk_mov_insumo_stock_nuevo` CHECK ((`stock_nuevo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=215 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_inventario_insumos`
--

LOCK TABLES `movimientos_inventario_insumos` WRITE;
/*!40000 ALTER TABLE `movimientos_inventario_insumos` DISABLE KEYS */;
INSERT INTO `movimientos_inventario_insumos` VALUES (1,2,'ENTRADA_COMPRA',2400.0000,0.0000,2400.0000,'compras',3,NULL,8,3,'2026-04-13 19:29:54'),(2,11,'ENTRADA_COMPRA',1.0000,0.0000,1.0000,'compras',4,NULL,8,4,'2026-04-13 19:30:24'),(3,10,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',5,NULL,8,5,'2026-04-13 19:31:10'),(4,13,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',6,NULL,8,6,'2026-04-13 19:31:58'),(5,10,'REVERSO_COMPRA',1000.0000,1000.0000,0.0000,'compras',5,'Auditoria: Cancelacion de compra #5',8,5,'2026-04-13 19:32:20'),(6,13,'REVERSO_COMPRA',1000.0000,1000.0000,0.0000,'compras',6,'Auditoria: Cancelacion de compra #6',8,6,'2026-04-13 19:32:23'),(7,13,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',7,NULL,8,7,'2026-04-13 19:33:01'),(8,13,'REVERSO_COMPRA',1000.0000,1000.0000,0.0000,'compras',7,'Auditoria: Cancelacion de compra #7',8,7,'2026-04-13 19:35:34'),(9,13,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',8,NULL,8,8,'2026-04-13 19:38:29'),(10,10,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',9,NULL,8,9,'2026-04-13 19:43:04'),(11,1,'ENTRADA_COMPRA',18.0000,0.0000,18.0000,'compras',10,NULL,8,10,'2026-04-13 20:07:18'),(12,11,'ENTRADA_COMPRA',2.0000,0.4000,2.4000,'compras',11,NULL,8,11,'2026-04-14 01:38:03'),(13,11,'ENTRADA_COMPRA',1.0000,0.6000,1.6000,'compras',12,NULL,8,12,'2026-04-14 02:23:17'),(14,11,'ENTRADA_COMPRA',1.0000,1.6000,2.6000,'compras',13,NULL,8,13,'2026-04-14 02:24:29'),(15,11,'ENTRADA_COMPRA',1.0000,2.0000,3.0000,'compras',14,NULL,8,14,'2026-04-14 02:27:55'),(16,13,'ENTRADA_COMPRA',1000.0000,250.0000,1250.0000,'compras',15,NULL,8,15,'2026-04-14 02:30:04'),(17,11,'SALIDA_MERMA',0.1000,3.0000,2.9000,'mermas_log',1,'Se contamino el agua ',8,13,'2026-04-14 17:09:09'),(18,11,'SALIDA_MERMA',0.1000,0.3000,0.2000,'mermas_log',NULL,'MERMA: Se contamino el agua ',8,13,'2026-04-14 17:09:09'),(19,6,'ENTRADA_COMPRA',8.0000,0.0000,8.0000,'compras',16,NULL,8,16,'2026-04-14 17:14:23'),(20,7,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',17,NULL,8,17,'2026-04-14 17:45:49'),(21,8,'ENTRADA_COMPRA',2900.0000,0.0000,2900.0000,'compras',18,NULL,8,18,'2026-04-14 18:00:18'),(22,17,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',18,NULL,8,19,'2026-04-14 18:00:18'),(23,59,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',18,NULL,8,20,'2026-04-14 18:00:18'),(24,5,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',18,NULL,8,21,'2026-04-14 18:00:18'),(25,40,'ENTRADA_COMPRA',960.0000,0.0000,960.0000,'compras',19,NULL,8,22,'2026-04-14 23:38:07'),(26,10,'SALIDA_PRODUCCION',110.0000,725.0000,615.0000,'detalle_ventas',16,'Despacho en cocina por orden de Venta',8,9,'2026-04-15 21:50:09'),(27,11,'SALIDA_PRODUCCION',0.2000,2.8000,2.6000,'detalle_ventas',16,'Despacho en cocina por orden de Venta',8,13,'2026-04-15 21:50:09'),(28,11,'SALIDA_PRODUCCION',1.0000,2.6000,1.6000,'detalle_ventas',16,'Despacho en cocina por orden de Venta',8,14,'2026-04-15 21:50:09'),(29,13,'SALIDA_PRODUCCION',250.0000,1250.0000,1000.0000,'detalle_ventas',16,'Despacho en cocina por orden de Venta',8,8,'2026-04-15 21:50:09'),(30,13,'SALIDA_PRODUCCION',50.0000,1000.0000,950.0000,'detalle_ventas',16,'Despacho en cocina por orden de Venta',8,15,'2026-04-15 21:50:09'),(31,5,'SALIDA_PRODUCCION',50.0000,1000.0000,950.0000,'detalle_ventas',15,'Despacho en cocina por orden de Venta',8,21,'2026-04-15 21:51:37'),(32,6,'SALIDA_PRODUCCION',1.0000,8.0000,7.0000,'detalle_ventas',15,'Despacho en cocina por orden de Venta',8,16,'2026-04-15 21:51:37'),(33,7,'SALIDA_PRODUCCION',50.0000,1000.0000,950.0000,'detalle_ventas',15,'Despacho en cocina por orden de Venta',8,17,'2026-04-15 21:51:37'),(34,8,'SALIDA_PRODUCCION',15.0000,2900.0000,2885.0000,'detalle_ventas',15,'Despacho en cocina por orden de Venta',8,18,'2026-04-15 21:51:37'),(35,17,'SALIDA_PRODUCCION',15.0000,1000.0000,985.0000,'detalle_ventas',15,'Despacho en cocina por orden de Venta',8,19,'2026-04-15 21:51:37'),(36,40,'SALIDA_PRODUCCION',15.0000,960.0000,945.0000,'detalle_ventas',15,'Despacho en cocina por orden de Venta',8,22,'2026-04-15 21:51:37'),(37,59,'SALIDA_PRODUCCION',50.0000,1000.0000,950.0000,'detalle_ventas',15,'Despacho en cocina por orden de Venta',8,20,'2026-04-15 21:51:37'),(38,5,'SALIDA_PRODUCCION',50.0000,950.0000,900.0000,'detalle_ventas',17,'Despacho en cocina por orden de Venta',8,21,'2026-04-15 21:51:39'),(39,6,'SALIDA_PRODUCCION',1.0000,7.0000,6.0000,'detalle_ventas',17,'Despacho en cocina por orden de Venta',8,16,'2026-04-15 21:51:39'),(40,7,'SALIDA_PRODUCCION',50.0000,950.0000,900.0000,'detalle_ventas',17,'Despacho en cocina por orden de Venta',8,17,'2026-04-15 21:51:39'),(41,8,'SALIDA_PRODUCCION',15.0000,2885.0000,2870.0000,'detalle_ventas',17,'Despacho en cocina por orden de Venta',8,18,'2026-04-15 21:51:39'),(42,17,'SALIDA_PRODUCCION',15.0000,985.0000,970.0000,'detalle_ventas',17,'Despacho en cocina por orden de Venta',8,19,'2026-04-15 21:51:39'),(43,40,'SALIDA_PRODUCCION',15.0000,945.0000,930.0000,'detalle_ventas',17,'Despacho en cocina por orden de Venta',8,22,'2026-04-15 21:51:39'),(44,59,'SALIDA_PRODUCCION',50.0000,950.0000,900.0000,'detalle_ventas',17,'Despacho en cocina por orden de Venta',8,20,'2026-04-15 21:51:39'),(45,10,'SALIDA_PRODUCCION',55.0000,615.0000,560.0000,'detalle_ventas',19,'Despacho en cocina por orden de Venta',8,9,'2026-04-15 21:52:51'),(46,11,'SALIDA_PRODUCCION',0.2000,1.6000,1.4000,'detalle_ventas',19,'Despacho en cocina por orden de Venta',8,11,'2026-04-15 21:52:51'),(47,11,'SALIDA_PRODUCCION',0.4000,1.4000,1.0000,'detalle_ventas',19,'Despacho en cocina por orden de Venta',8,12,'2026-04-15 21:52:51'),(48,13,'SALIDA_PRODUCCION',150.0000,950.0000,800.0000,'detalle_ventas',19,'Despacho en cocina por orden de Venta',8,15,'2026-04-15 21:52:51'),(49,5,'SALIDA_PRODUCCION',50.0000,900.0000,850.0000,'detalle_ventas',20,'Despacho en cocina por orden de Venta',8,21,'2026-04-15 21:52:57'),(50,6,'SALIDA_PRODUCCION',1.0000,6.0000,5.0000,'detalle_ventas',20,'Despacho en cocina por orden de Venta',8,16,'2026-04-15 21:52:57'),(51,7,'SALIDA_PRODUCCION',50.0000,900.0000,850.0000,'detalle_ventas',20,'Despacho en cocina por orden de Venta',8,17,'2026-04-15 21:52:57'),(52,8,'SALIDA_PRODUCCION',15.0000,2870.0000,2855.0000,'detalle_ventas',20,'Despacho en cocina por orden de Venta',8,18,'2026-04-15 21:52:57'),(53,17,'SALIDA_PRODUCCION',15.0000,970.0000,955.0000,'detalle_ventas',20,'Despacho en cocina por orden de Venta',8,19,'2026-04-15 21:52:57'),(54,40,'SALIDA_PRODUCCION',15.0000,930.0000,915.0000,'detalle_ventas',20,'Despacho en cocina por orden de Venta',8,22,'2026-04-15 21:52:57'),(55,59,'SALIDA_PRODUCCION',50.0000,900.0000,850.0000,'detalle_ventas',20,'Despacho en cocina por orden de Venta',8,20,'2026-04-15 21:52:57'),(56,10,'SALIDA_PRODUCCION',55.0000,560.0000,505.0000,'ordenes_produccion',10,'Despacho en cocina por orden de Producción',8,9,'2026-04-15 21:58:02'),(57,11,'SALIDA_PRODUCCION',0.6000,1.0000,0.4000,'ordenes_produccion',10,'Despacho en cocina por orden de Producción',8,12,'2026-04-15 21:58:02'),(58,13,'SALIDA_PRODUCCION',150.0000,800.0000,650.0000,'ordenes_produccion',10,'Despacho en cocina por orden de Producción',8,15,'2026-04-15 21:58:02'),(59,29,'ENTRADA_COMPRA',4000.0000,0.0000,4000.0000,'compras',20,NULL,8,23,'2026-04-15 23:53:34'),(60,56,'ENTRADA_COMPRA',1.0000,0.0000,1.0000,'compras',21,NULL,8,24,'2026-04-16 00:00:39'),(61,36,'ENTRADA_COMPRA',2000.0000,0.0000,2000.0000,'compras',21,NULL,8,25,'2026-04-16 00:00:39'),(62,49,'ENTRADA_COMPRA',3000.0000,0.0000,3000.0000,'compras',22,NULL,8,26,'2026-04-16 00:01:30'),(63,39,'ENTRADA_COMPRA',3000.0000,0.0000,3000.0000,'compras',23,NULL,8,27,'2026-04-16 00:04:13'),(64,48,'ENTRADA_COMPRA',2000.0000,0.0000,2000.0000,'compras',23,NULL,8,28,'2026-04-16 00:04:13'),(65,56,'ENTRADA_COMPRA',1000.0000,1.0000,1001.0000,'compras',24,NULL,8,29,'2026-04-16 00:07:42'),(66,35,'ENTRADA_COMPRA',2000.0000,0.0000,2000.0000,'compras',25,NULL,8,30,'2026-04-16 00:28:25'),(67,36,'ENTRADA_COMPRA',1000.0000,2000.0000,3000.0000,'compras',26,NULL,8,31,'2026-04-16 00:33:05'),(68,17,'ENTRADA_COMPRA',1000.0000,955.0000,1955.0000,'compras',27,NULL,8,32,'2026-04-16 00:34:00'),(69,34,'ENTRADA_COMPRA',2000.0000,0.0000,2000.0000,'compras',28,NULL,8,33,'2026-04-16 00:42:53'),(70,61,'ENTRADA_COMPRA',2.0000,0.0000,2.0000,'compras',28,NULL,8,34,'2026-04-16 00:42:53'),(71,5,'ENTRADA_COMPRA',1000.0000,850.0000,1850.0000,'compras',29,NULL,8,35,'2026-04-16 00:43:57'),(72,4,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',29,NULL,8,36,'2026-04-16 00:43:57'),(73,60,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',30,NULL,8,37,'2026-04-16 00:44:38'),(74,19,'ENTRADA_COMPRA',30.0000,0.0000,30.0000,'compras',31,NULL,8,38,'2026-04-16 00:46:05'),(79,4,'SALIDA_PRODUCCION',20.0000,1000.0000,980.0000,'detalle_ventas',22,'Despacho en cocina por orden de Venta',8,36,'2026-04-16 01:00:17'),(80,5,'SALIDA_PRODUCCION',20.0000,1850.0000,1830.0000,'detalle_ventas',22,'Despacho en cocina por orden de Venta',8,35,'2026-04-16 01:00:17'),(81,17,'SALIDA_PRODUCCION',25.0000,1955.0000,1930.0000,'detalle_ventas',22,'Despacho en cocina por orden de Venta',8,32,'2026-04-16 01:00:17'),(82,19,'SALIDA_PRODUCCION',1.0000,30.0000,29.0000,'detalle_ventas',22,'Despacho en cocina por orden de Venta',8,38,'2026-04-16 01:00:17'),(83,34,'SALIDA_PRODUCCION',50.0000,2000.0000,1950.0000,'detalle_ventas',22,'Despacho en cocina por orden de Venta',8,33,'2026-04-16 01:00:17'),(84,35,'SALIDA_PRODUCCION',90.0000,2000.0000,1910.0000,'detalle_ventas',22,'Despacho en cocina por orden de Venta',8,30,'2026-04-16 01:00:17'),(85,36,'SALIDA_PRODUCCION',110.0000,3000.0000,2890.0000,'detalle_ventas',22,'Despacho en cocina por orden de Venta',8,25,'2026-04-16 01:00:17'),(86,60,'SALIDA_PRODUCCION',30.0000,1000.0000,970.0000,'detalle_ventas',22,'Despacho en cocina por orden de Venta',8,37,'2026-04-16 01:00:17'),(87,5,'SALIDA_PRODUCCION',50.0000,1830.0000,1780.0000,'detalle_ventas',23,'Despacho en cocina por orden de Venta',8,35,'2026-04-16 01:00:19'),(88,6,'SALIDA_PRODUCCION',1.0000,5.0000,4.0000,'detalle_ventas',23,'Despacho en cocina por orden de Venta',8,16,'2026-04-16 01:00:19'),(89,7,'SALIDA_PRODUCCION',50.0000,850.0000,800.0000,'detalle_ventas',23,'Despacho en cocina por orden de Venta',8,17,'2026-04-16 01:00:19'),(90,8,'SALIDA_PRODUCCION',15.0000,2855.0000,2840.0000,'detalle_ventas',23,'Despacho en cocina por orden de Venta',8,18,'2026-04-16 01:00:19'),(91,17,'SALIDA_PRODUCCION',10.0000,1930.0000,1920.0000,'detalle_ventas',23,'Despacho en cocina por orden de Venta',8,32,'2026-04-16 01:00:19'),(92,40,'SALIDA_PRODUCCION',15.0000,915.0000,900.0000,'detalle_ventas',23,'Despacho en cocina por orden de Venta',8,22,'2026-04-16 01:00:19'),(93,59,'SALIDA_PRODUCCION',50.0000,850.0000,800.0000,'detalle_ventas',23,'Despacho en cocina por orden de Venta',8,20,'2026-04-16 01:00:19'),(94,21,'ENTRADA_COMPRA',3000.0000,0.0000,3000.0000,'compras',32,NULL,8,39,'2026-04-16 01:03:02'),(99,37,'ENTRADA_COMPRA',20.0000,0.0000,20.0000,'compras',33,NULL,8,40,'2026-04-16 01:07:33'),(100,20,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',34,NULL,8,41,'2026-04-16 01:08:26'),(101,17,'SALIDA_PRODUCCION',20.0000,1920.0000,1900.0000,'detalle_ventas',25,'Despacho en cocina por orden de Venta',8,32,'2026-04-16 01:08:32'),(102,20,'SALIDA_PRODUCCION',80.0000,1000.0000,920.0000,'detalle_ventas',25,'Despacho en cocina por orden de Venta',8,41,'2026-04-16 01:08:32'),(103,21,'SALIDA_PRODUCCION',50.0000,3000.0000,2950.0000,'detalle_ventas',25,'Despacho en cocina por orden de Venta',8,39,'2026-04-16 01:08:32'),(104,29,'SALIDA_PRODUCCION',30.0000,4000.0000,3970.0000,'detalle_ventas',25,'Despacho en cocina por orden de Venta',8,23,'2026-04-16 01:08:32'),(105,37,'SALIDA_PRODUCCION',1.0000,20.0000,19.0000,'detalle_ventas',25,'Despacho en cocina por orden de Venta',8,40,'2026-04-16 01:08:32'),(106,39,'SALIDA_PRODUCCION',60.0000,3000.0000,2940.0000,'detalle_ventas',25,'Despacho en cocina por orden de Venta',8,27,'2026-04-16 01:08:32'),(107,40,'SALIDA_PRODUCCION',15.0000,900.0000,885.0000,'detalle_ventas',25,'Despacho en cocina por orden de Venta',8,22,'2026-04-16 01:08:32'),(108,4,'SALIDA_PRODUCCION',20.0000,980.0000,960.0000,'detalle_ventas',24,'Despacho en cocina por orden de Venta',8,36,'2026-04-16 01:08:34'),(109,5,'SALIDA_PRODUCCION',30.0000,1780.0000,1750.0000,'detalle_ventas',24,'Despacho en cocina por orden de Venta',8,35,'2026-04-16 01:08:34'),(110,19,'SALIDA_PRODUCCION',1.0000,29.0000,28.0000,'detalle_ventas',24,'Despacho en cocina por orden de Venta',8,38,'2026-04-16 01:08:34'),(111,20,'SALIDA_PRODUCCION',40.0000,920.0000,880.0000,'detalle_ventas',24,'Despacho en cocina por orden de Venta',8,41,'2026-04-16 01:08:34'),(112,21,'SALIDA_PRODUCCION',50.0000,2950.0000,2900.0000,'detalle_ventas',24,'Despacho en cocina por orden de Venta',8,39,'2026-04-16 01:08:34'),(113,59,'SALIDA_PRODUCCION',15.0000,800.0000,785.0000,'detalle_ventas',24,'Despacho en cocina por orden de Venta',8,20,'2026-04-16 01:08:34'),(114,4,'SALIDA_PRODUCCION',20.0000,960.0000,940.0000,'detalle_ventas',30,'Despacho en cocina por orden de Venta',8,36,'2026-04-16 01:34:27'),(115,5,'SALIDA_PRODUCCION',30.0000,1750.0000,1720.0000,'detalle_ventas',30,'Despacho en cocina por orden de Venta',8,35,'2026-04-16 01:34:27'),(116,19,'SALIDA_PRODUCCION',1.0000,28.0000,27.0000,'detalle_ventas',30,'Despacho en cocina por orden de Venta',8,38,'2026-04-16 01:34:27'),(117,20,'SALIDA_PRODUCCION',40.0000,880.0000,840.0000,'detalle_ventas',30,'Despacho en cocina por orden de Venta',8,41,'2026-04-16 01:34:27'),(118,21,'SALIDA_PRODUCCION',50.0000,2900.0000,2850.0000,'detalle_ventas',30,'Despacho en cocina por orden de Venta',8,39,'2026-04-16 01:34:27'),(119,59,'SALIDA_PRODUCCION',15.0000,785.0000,770.0000,'detalle_ventas',30,'Despacho en cocina por orden de Venta',8,20,'2026-04-16 01:34:27'),(120,17,'SALIDA_PRODUCCION',20.0000,1900.0000,1880.0000,'detalle_ventas',31,'Despacho en cocina por orden de Venta',8,32,'2026-04-16 01:34:27'),(121,20,'SALIDA_PRODUCCION',80.0000,840.0000,760.0000,'detalle_ventas',31,'Despacho en cocina por orden de Venta',8,41,'2026-04-16 01:34:27'),(122,21,'SALIDA_PRODUCCION',50.0000,2850.0000,2800.0000,'detalle_ventas',31,'Despacho en cocina por orden de Venta',8,39,'2026-04-16 01:34:27'),(123,29,'SALIDA_PRODUCCION',30.0000,3970.0000,3940.0000,'detalle_ventas',31,'Despacho en cocina por orden de Venta',8,23,'2026-04-16 01:34:27'),(124,37,'SALIDA_PRODUCCION',1.0000,19.0000,18.0000,'detalle_ventas',31,'Despacho en cocina por orden de Venta',8,40,'2026-04-16 01:34:27'),(125,39,'SALIDA_PRODUCCION',60.0000,2940.0000,2880.0000,'detalle_ventas',31,'Despacho en cocina por orden de Venta',8,27,'2026-04-16 01:34:27'),(126,40,'SALIDA_PRODUCCION',15.0000,885.0000,870.0000,'detalle_ventas',31,'Despacho en cocina por orden de Venta',8,22,'2026-04-16 01:34:27'),(127,29,'SALIDA_PRODUCCION',80.0000,3940.0000,3860.0000,'detalle_ventas',32,'Despacho en cocina por orden de Venta',8,23,'2026-04-16 01:34:28'),(128,36,'SALIDA_PRODUCCION',100.0000,2890.0000,2790.0000,'detalle_ventas',32,'Despacho en cocina por orden de Venta',8,25,'2026-04-16 01:34:28'),(129,39,'SALIDA_PRODUCCION',60.0000,2880.0000,2820.0000,'detalle_ventas',32,'Despacho en cocina por orden de Venta',8,27,'2026-04-16 01:34:28'),(130,48,'SALIDA_PRODUCCION',20.0000,2000.0000,1980.0000,'detalle_ventas',32,'Despacho en cocina por orden de Venta',8,28,'2026-04-16 01:34:28'),(131,49,'SALIDA_PRODUCCION',20.0000,3000.0000,2980.0000,'detalle_ventas',32,'Despacho en cocina por orden de Venta',8,26,'2026-04-16 01:34:28'),(132,56,'SALIDA_PRODUCCION',1.0000,1001.0000,1000.0000,'detalle_ventas',32,'Despacho en cocina por orden de Venta',8,24,'2026-04-16 01:34:28'),(133,56,'SALIDA_PRODUCCION',59.0000,1000.0000,941.0000,'detalle_ventas',32,'Despacho en cocina por orden de Venta',8,29,'2026-04-16 01:34:28'),(134,4,'SALIDA_PRODUCCION',20.0000,940.0000,920.0000,'detalle_ventas',36,'Despacho en cocina por orden de Venta',8,36,'2026-04-16 03:03:01'),(135,5,'SALIDA_PRODUCCION',20.0000,1720.0000,1700.0000,'detalle_ventas',36,'Despacho en cocina por orden de Venta',8,35,'2026-04-16 03:03:01'),(136,17,'SALIDA_PRODUCCION',25.0000,1880.0000,1855.0000,'detalle_ventas',36,'Despacho en cocina por orden de Venta',8,32,'2026-04-16 03:03:01'),(137,19,'SALIDA_PRODUCCION',1.0000,27.0000,26.0000,'detalle_ventas',36,'Despacho en cocina por orden de Venta',8,38,'2026-04-16 03:03:01'),(138,34,'SALIDA_PRODUCCION',50.0000,1950.0000,1900.0000,'detalle_ventas',36,'Despacho en cocina por orden de Venta',8,33,'2026-04-16 03:03:01'),(139,35,'SALIDA_PRODUCCION',90.0000,1910.0000,1820.0000,'detalle_ventas',36,'Despacho en cocina por orden de Venta',8,30,'2026-04-16 03:03:01'),(140,36,'SALIDA_PRODUCCION',110.0000,2790.0000,2680.0000,'detalle_ventas',36,'Despacho en cocina por orden de Venta',8,25,'2026-04-16 03:03:01'),(141,60,'SALIDA_PRODUCCION',30.0000,970.0000,940.0000,'detalle_ventas',36,'Despacho en cocina por orden de Venta',8,37,'2026-04-16 03:03:01'),(142,29,'SALIDA_PRODUCCION',80.0000,3860.0000,3780.0000,'detalle_ventas',37,'Despacho en cocina por orden de Venta',8,23,'2026-04-16 03:03:03'),(143,36,'SALIDA_PRODUCCION',100.0000,2680.0000,2580.0000,'detalle_ventas',37,'Despacho en cocina por orden de Venta',8,25,'2026-04-16 03:03:03'),(144,39,'SALIDA_PRODUCCION',60.0000,2820.0000,2760.0000,'detalle_ventas',37,'Despacho en cocina por orden de Venta',8,27,'2026-04-16 03:03:03'),(145,48,'SALIDA_PRODUCCION',20.0000,1980.0000,1960.0000,'detalle_ventas',37,'Despacho en cocina por orden de Venta',8,28,'2026-04-16 03:03:03'),(146,49,'SALIDA_PRODUCCION',20.0000,2980.0000,2960.0000,'detalle_ventas',37,'Despacho en cocina por orden de Venta',8,26,'2026-04-16 03:03:03'),(147,56,'SALIDA_PRODUCCION',60.0000,941.0000,881.0000,'detalle_ventas',37,'Despacho en cocina por orden de Venta',8,29,'2026-04-16 03:03:03'),(148,5,'SALIDA_PRODUCCION',50.0000,1700.0000,1650.0000,'detalle_ventas',39,'Despacho en cocina por orden de Venta',8,35,'2026-04-16 03:08:32'),(149,6,'SALIDA_PRODUCCION',1.0000,4.0000,3.0000,'detalle_ventas',39,'Despacho en cocina por orden de Venta',8,16,'2026-04-16 03:08:32'),(150,7,'SALIDA_PRODUCCION',50.0000,800.0000,750.0000,'detalle_ventas',39,'Despacho en cocina por orden de Venta',8,17,'2026-04-16 03:08:32'),(151,8,'SALIDA_PRODUCCION',15.0000,2840.0000,2825.0000,'detalle_ventas',39,'Despacho en cocina por orden de Venta',8,18,'2026-04-16 03:08:32'),(152,17,'SALIDA_PRODUCCION',10.0000,1855.0000,1845.0000,'detalle_ventas',39,'Despacho en cocina por orden de Venta',8,32,'2026-04-16 03:08:32'),(153,40,'SALIDA_PRODUCCION',15.0000,870.0000,855.0000,'detalle_ventas',39,'Despacho en cocina por orden de Venta',8,22,'2026-04-16 03:08:32'),(154,59,'SALIDA_PRODUCCION',50.0000,770.0000,720.0000,'detalle_ventas',39,'Despacho en cocina por orden de Venta',8,20,'2026-04-16 03:08:32'),(155,29,'SALIDA_PRODUCCION',80.0000,3780.0000,3700.0000,'detalle_ventas',40,'Despacho en cocina por orden de Venta',8,23,'2026-04-16 03:08:34'),(156,36,'SALIDA_PRODUCCION',100.0000,2580.0000,2480.0000,'detalle_ventas',40,'Despacho en cocina por orden de Venta',8,25,'2026-04-16 03:08:34'),(157,39,'SALIDA_PRODUCCION',60.0000,2760.0000,2700.0000,'detalle_ventas',40,'Despacho en cocina por orden de Venta',8,27,'2026-04-16 03:08:34'),(158,48,'SALIDA_PRODUCCION',20.0000,1960.0000,1940.0000,'detalle_ventas',40,'Despacho en cocina por orden de Venta',8,28,'2026-04-16 03:08:34'),(159,49,'SALIDA_PRODUCCION',20.0000,2960.0000,2940.0000,'detalle_ventas',40,'Despacho en cocina por orden de Venta',8,26,'2026-04-16 03:08:34'),(160,56,'SALIDA_PRODUCCION',60.0000,881.0000,821.0000,'detalle_ventas',40,'Despacho en cocina por orden de Venta',8,29,'2026-04-16 03:08:34'),(161,1,'SALIDA_PRODUCCION',1.0000,17.0000,16.0000,'detalle_ventas',42,'Despacho en cocina por orden de Venta',8,10,'2026-04-16 03:10:24'),(162,1,'SALIDA_PRODUCCION',1.0000,16.0000,15.0000,'detalle_ventas',43,'Despacho en cocina por orden de Venta',8,10,'2026-04-16 03:24:50'),(163,1,'SALIDA_PRODUCCION',1.0000,15.0000,14.0000,'detalle_ventas',44,'Despacho en cocina por orden de Venta',8,10,'2026-04-16 03:24:50'),(164,1,'SALIDA_PRODUCCION',1.0000,14.0000,13.0000,'detalle_ventas',45,'Despacho en cocina por orden de Venta',8,10,'2026-04-16 03:24:51'),(165,5,'SALIDA_PRODUCCION',50.0000,1650.0000,1600.0000,'detalle_ventas',46,'Despacho en cocina por orden de Venta',8,35,'2026-04-16 03:25:46'),(166,6,'SALIDA_PRODUCCION',1.0000,3.0000,2.0000,'detalle_ventas',46,'Despacho en cocina por orden de Venta',8,16,'2026-04-16 03:25:46'),(167,7,'SALIDA_PRODUCCION',50.0000,750.0000,700.0000,'detalle_ventas',46,'Despacho en cocina por orden de Venta',8,17,'2026-04-16 03:25:46'),(168,8,'SALIDA_PRODUCCION',15.0000,2825.0000,2810.0000,'detalle_ventas',46,'Despacho en cocina por orden de Venta',8,18,'2026-04-16 03:25:46'),(169,17,'SALIDA_PRODUCCION',10.0000,1845.0000,1835.0000,'detalle_ventas',46,'Despacho en cocina por orden de Venta',8,32,'2026-04-16 03:25:46'),(170,40,'SALIDA_PRODUCCION',15.0000,855.0000,840.0000,'detalle_ventas',46,'Despacho en cocina por orden de Venta',8,22,'2026-04-16 03:25:46'),(171,59,'SALIDA_PRODUCCION',50.0000,720.0000,670.0000,'detalle_ventas',46,'Despacho en cocina por orden de Venta',8,20,'2026-04-16 03:25:46'),(172,11,'ENTRADA_COMPRA',2.0000,0.4000,2.4000,'compras',35,NULL,8,42,'2026-04-16 11:55:14'),(173,10,'SALIDA_PRODUCCION',55.0000,505.0000,450.0000,'detalle_ventas',47,'Despacho en cocina por orden de Venta',8,9,'2026-04-16 12:00:24'),(174,11,'SALIDA_PRODUCCION',0.4000,2.4000,2.0000,'detalle_ventas',47,'Despacho en cocina por orden de Venta',8,4,'2026-04-16 12:00:24'),(175,11,'SALIDA_PRODUCCION',0.2000,2.0000,1.8000,'detalle_ventas',47,'Despacho en cocina por orden de Venta',8,42,'2026-04-16 12:00:24'),(176,13,'SALIDA_PRODUCCION',150.0000,650.0000,500.0000,'detalle_ventas',47,'Despacho en cocina por orden de Venta',8,15,'2026-04-16 12:00:24'),(177,4,'SALIDA_PRODUCCION',20.0000,920.0000,900.0000,'detalle_ventas',48,'Despacho en cocina por orden de Venta',8,36,'2026-04-16 12:00:36'),(178,5,'SALIDA_PRODUCCION',30.0000,1600.0000,1570.0000,'detalle_ventas',48,'Despacho en cocina por orden de Venta',8,35,'2026-04-16 12:00:36'),(179,19,'SALIDA_PRODUCCION',1.0000,26.0000,25.0000,'detalle_ventas',48,'Despacho en cocina por orden de Venta',8,38,'2026-04-16 12:00:36'),(180,20,'SALIDA_PRODUCCION',40.0000,760.0000,720.0000,'detalle_ventas',48,'Despacho en cocina por orden de Venta',8,41,'2026-04-16 12:00:36'),(181,21,'SALIDA_PRODUCCION',50.0000,2800.0000,2750.0000,'detalle_ventas',48,'Despacho en cocina por orden de Venta',8,39,'2026-04-16 12:00:36'),(182,59,'SALIDA_PRODUCCION',15.0000,670.0000,655.0000,'detalle_ventas',48,'Despacho en cocina por orden de Venta',8,20,'2026-04-16 12:00:36'),(183,23,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',36,NULL,8,43,'2026-04-16 16:40:06'),(184,23,'ENTRADA_COMPRA',1000.0000,1000.0000,2000.0000,'compras',37,NULL,8,44,'2026-04-16 16:42:44'),(185,22,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',38,NULL,8,45,'2026-04-16 16:44:46'),(186,22,'ENTRADA_COMPRA',1000.0000,1000.0000,2000.0000,'compras',39,NULL,8,46,'2026-04-16 16:45:45'),(187,24,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',40,NULL,8,47,'2026-04-16 16:47:37'),(188,22,'ENTRADA_COMPRA',1000.0000,2000.0000,3000.0000,'compras',41,NULL,8,48,'2026-04-16 16:54:06'),(189,7,'ENTRADA_COMPRA',1000.0000,700.0000,1700.0000,'compras',42,NULL,8,49,'2026-04-16 16:54:32'),(190,32,'ENTRADA_COMPRA',3780.0000,0.0000,3780.0000,'compras',43,NULL,8,50,'2026-04-16 16:56:22'),(191,46,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',44,NULL,8,51,'2026-04-16 16:56:48'),(192,16,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',45,NULL,14,52,'2026-04-16 19:46:31'),(193,16,'REVERSO_COMPRA',1000.0000,1000.0000,0.0000,'compras',45,'Auditoria: Cancelacion de compra #45',14,52,'2026-04-16 19:46:58'),(194,16,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',46,NULL,14,53,'2026-04-16 19:50:09'),(195,25,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',46,NULL,14,54,'2026-04-16 19:50:09'),(196,26,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',46,NULL,14,55,'2026-04-16 19:50:09'),(197,28,'ENTRADA_COMPRA',1000.0000,0.0000,1000.0000,'compras',46,NULL,14,56,'2026-04-16 19:50:09'),(198,10,'ENTRADA_COMPRA',1000.0000,450.0000,1450.0000,'compras',46,NULL,14,57,'2026-04-16 19:50:09'),(199,35,'SALIDA_MERMA',100.0000,1820.0000,1720.0000,'mermas_log',2,'contamino',14,30,'2026-04-16 19:51:08'),(200,35,'SALIDA_MERMA',100.0000,1720.0000,1620.0000,'mermas_log',NULL,'MERMA: contamino',14,30,'2026-04-16 19:51:08'),(202,18,'ENTRADA_COMPRA',1.0000,0.0000,1.0000,'compras',47,NULL,14,58,'2026-04-16 19:58:47'),(205,22,'SALIDA_PRODUCCION',150.0000,3000.0000,2850.0000,'detalle_ventas',51,'Despacho en cocina por orden de Venta',12,48,'2026-04-16 20:01:57'),(206,23,'SALIDA_PRODUCCION',50.0000,2000.0000,1950.0000,'detalle_ventas',51,'Despacho en cocina por orden de Venta',12,44,'2026-04-16 20:01:57'),(207,24,'SALIDA_PRODUCCION',5.0000,1000.0000,995.0000,'detalle_ventas',51,'Despacho en cocina por orden de Venta',12,47,'2026-04-16 20:01:57'),(208,5,'SALIDA_PRODUCCION',50.0000,1570.0000,1520.0000,'detalle_ventas',52,'Despacho en cocina por orden de Venta',12,35,'2026-04-16 20:02:00'),(209,6,'SALIDA_PRODUCCION',1.0000,2.0000,1.0000,'detalle_ventas',52,'Despacho en cocina por orden de Venta',12,16,'2026-04-16 20:02:00'),(210,7,'SALIDA_PRODUCCION',50.0000,1700.0000,1650.0000,'detalle_ventas',52,'Despacho en cocina por orden de Venta',12,49,'2026-04-16 20:02:00'),(211,8,'SALIDA_PRODUCCION',15.0000,2810.0000,2795.0000,'detalle_ventas',52,'Despacho en cocina por orden de Venta',12,18,'2026-04-16 20:02:00'),(212,17,'SALIDA_PRODUCCION',10.0000,1835.0000,1825.0000,'detalle_ventas',52,'Despacho en cocina por orden de Venta',12,32,'2026-04-16 20:02:00'),(213,40,'SALIDA_PRODUCCION',15.0000,840.0000,825.0000,'detalle_ventas',52,'Despacho en cocina por orden de Venta',12,22,'2026-04-16 20:02:00'),(214,59,'SALIDA_PRODUCCION',50.0000,655.0000,605.0000,'detalle_ventas',52,'Despacho en cocina por orden de Venta',12,20,'2026-04-16 20:02:00');
/*!40000 ALTER TABLE `movimientos_inventario_insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_inventario_productos`
--

DROP TABLE IF EXISTS `movimientos_inventario_productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_inventario_productos` (
  `id_movimiento_producto` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `tipo_movimiento` enum('ENTRADA_PRODUCCION','SALIDA_VENTA','SALIDA_COMBO','REVERSO_VENTA','AJUSTE_MANUAL') NOT NULL,
  `cantidad` int NOT NULL,
  `stock_anterior` int NOT NULL,
  `stock_nuevo` int NOT NULL,
  `referencia_tabla` varchar(50) DEFAULT NULL,
  `referencia_id` int DEFAULT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `id_usuario` int NOT NULL,
  `fecha_movimiento` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_movimiento_producto`),
  KEY `fk_mov_prod_producto` (`id_producto`),
  KEY `fk_mov_prod_usuario` (`id_usuario`),
  KEY `idx_mov_prod_fecha` (`fecha_movimiento`),
  KEY `idx_mov_prod_tipo` (`tipo_movimiento`),
  CONSTRAINT `fk_mov_prod_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `fk_mov_prod_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `chk_mov_prod_cantidad` CHECK ((`cantidad` > 0)),
  CONSTRAINT `chk_mov_prod_stock_anterior` CHECK ((`stock_anterior` >= 0)),
  CONSTRAINT `chk_mov_prod_stock_nuevo` CHECK ((`stock_nuevo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_inventario_productos`
--

LOCK TABLES `movimientos_inventario_productos` WRITE;
/*!40000 ALTER TABLE `movimientos_inventario_productos` DISABLE KEYS */;
INSERT INTO `movimientos_inventario_productos` VALUES (1,6,'SALIDA_VENTA',1,1,0,'detalle_ventas',29,'Despacho total desde stock pre-producido',8,'2026-04-16 01:34:25');
/*!40000 ALTER TABLE `movimientos_inventario_productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordenes_produccion`
--

DROP TABLE IF EXISTS `ordenes_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordenes_produccion` (
  `id_orden_produccion` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `id_usuario_crea` int NOT NULL,
  `id_usuario_responsable` int DEFAULT NULL,
  `cantidad_programada` int NOT NULL,
  `cantidad_producida` int NOT NULL DEFAULT '0',
  `estado` enum('Pendiente','En Proceso','Completada','Cancelada') NOT NULL DEFAULT 'Pendiente',
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_inicio` datetime DEFAULT NULL,
  `fecha_finalizacion` datetime DEFAULT NULL,
  `observaciones` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_orden_produccion`),
  KEY `fk_op_producto` (`id_producto`),
  KEY `fk_op_usuario_crea` (`id_usuario_crea`),
  KEY `fk_op_usuario_responsable` (`id_usuario_responsable`),
  KEY `idx_op_estado` (`estado`),
  KEY `idx_op_fecha_creacion` (`fecha_creacion`),
  CONSTRAINT `fk_op_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `fk_op_usuario_crea` FOREIGN KEY (`id_usuario_crea`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `fk_op_usuario_responsable` FOREIGN KEY (`id_usuario_responsable`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `chk_op_cantidad_producida` CHECK ((`cantidad_producida` >= 0)),
  CONSTRAINT `chk_op_cantidad_programada` CHECK ((`cantidad_programada` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_produccion`
--

LOCK TABLES `ordenes_produccion` WRITE;
/*!40000 ALTER TABLE `ordenes_produccion` DISABLE KEYS */;
INSERT INTO `ordenes_produccion` VALUES (1,4,2,2,2,2,'Completada','2026-04-06 05:26:35','2026-04-06 05:26:43','2026-04-06 05:26:48','2'),(2,4,4,4,1,1,'Completada','2026-04-10 18:18:38',NULL,'2026-04-12 12:33:31',NULL),(3,3,4,2,12,12,'Completada','2026-04-10 18:27:08','2026-04-10 18:27:25','2026-04-10 18:27:35',NULL),(4,3,4,4,12,12,'Completada','2026-04-11 08:43:10',NULL,'2026-04-11 20:18:19',NULL),(5,7,4,4,1,1,'Completada','2026-04-11 09:07:21',NULL,'2026-04-12 12:33:32',NULL),(6,2,4,4,1,1,'Completada','2026-04-11 09:07:41',NULL,'2026-04-12 12:33:36',NULL),(7,6,8,8,1,1,'Completada','2026-04-14 01:32:39',NULL,'2026-04-14 02:22:31','Venta #17'),(8,6,8,8,1,1,'Completada','2026-04-14 01:56:44',NULL,'2026-04-14 02:22:33','Venta #18'),(9,1,8,8,1,1,'Completada','2026-04-14 02:09:53',NULL,'2026-04-14 02:22:34',NULL),(10,6,8,8,1,1,'Completada','2026-04-15 21:57:53',NULL,'2026-04-15 21:58:02',NULL);
/*!40000 ALTER TABLE `ordenes_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona`
--

DROP TABLE IF EXISTS `persona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persona` (
  `id_persona` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellido_pa` varchar(50) NOT NULL,
  `apellido_ma` varchar(50) NOT NULL,
  `fecha_nac` date DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id_persona`),
  UNIQUE KEY `telefono` (`telefono`),
  KEY `idx_persona_nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES (1,'Cliente','Transacciones','Prueba',NULL,'4770001122'),(2,'Diego','Gonzalez','Gaytan','1999-08-12','4771010101'),(3,'Mariana','Lopez','Torres','1994-03-25','4771010102'),(4,'Carlos','Ramirez','Soto','1997-11-08','4771010103'),(5,'Fernanda','Martinez','Ruiz','1998-01-14','4771010104'),(6,'Jorge','Hernandez','Mora','1995-06-30','4771010105'),(7,'Ana','Castillo','Vega','2000-09-19','4771010106'),(9,'Cajero','Demo','Sistema',NULL,'2220001111'),(11,'Administrador','Full','Sistema',NULL,'9998887766'),(13,'Gerente','pacos','cas',NULL,'3220001111'),(17,'Chef','Monster','Eats',NULL,'2220005555'),(19,'Demo','Demo','Demo',NULL,'2220009999'),(20,'Usuario','Prueba','Monster','2000-01-01','5551234567'),(21,'Christopher','Rivera','Valderrama',NULL,'4771800650'),(23,'SUPER','GERENTE','Martinez',NULL,'4771800597'),(24,'Cliente','Demo','Usuario',NULL,'4770000000'),(25,'Uriel','Hernandez','Camacho','2005-11-15','4772546118'),(26,'Axel','Rodriguez','Rocha','2005-12-17','4778124210'),(30,'Christopher Isaac','Rivera','Martinez','2005-12-01','4779992222'),(31,'Ojeda Daniel','Luna','Martinez','2005-02-01','4776663333');
/*!40000 ALTER TABLE `persona` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `id_categoria` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `imagen` varchar(255) DEFAULT 'default_product.png',
  `descripcion` text,
  `precio_venta` decimal(10,2) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_producto`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `fk_productos_categoria` (`id_categoria`),
  KEY `idx_productos_nombre` (`nombre`),
  KEY `idx_productos_activo` (`activo`),
  CONSTRAINT `fk_productos_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`),
  CONSTRAINT `chk_productos_precio` CHECK ((`precio_venta` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,4,'Hamburguesa jujutsu','Hamburguesa_jujutsu_hamburguesa.png',NULL,180.00,1),(2,9,'Papas Sukuna','Papas_Sukuna_Jujutsu.png',NULL,170.00,1),(3,10,'Burrito','Burrito_burrito.png',NULL,60.00,1),(5,9,'Papas Sencillas','Papas_Sencillas_papas.png',NULL,60.00,1),(6,1,'Agua de limon (600ml)','Agua_de_limon_600ml_agua_de_limon.png','Limonada artesanal elaborada con fruta natural. Servida bien fría.',45.00,1),(7,5,'Hot dog Monstruoso','Hot_dog_Monstruoso_Hochis.png','Una explosión de sabor con jitomate fresquecito, cebolla picada y nuestra combinación especial de mayonesa y crema que le da una cremosidad inigualable. Sencillo, pero con un sabor monstruosamente bueno.',35.00,1),(8,10,'Sincronizada','Sincronizada_sincronizada.png','Una tortilla de harina, jamón y queso fundido. Acompañada de lechuga, jitomate y cebolla.\r\nLa clásica que nunca falla.',40.00,1),(9,1,'Agua de Jamaica (600ml)','Agua_de_Jamaica_agua_jamiaca.png','100% natural y siempre fría. El acompañamiento ideal para tu comida.',45.00,1),(10,10,'Monster Torta','Monster_Torta_Torta.png','Torta de bolillo crujiente, rellena de jamón, queso Oaxaca derretido, aguacate, crema, lechuga y un toque de mayonesa. Acompañada de papas a la francesa.',83.00,1),(11,4,'Monster Burger','Monster_Burger_hamburfuesa.png','Prueba la deliciosa Monster Burger Clásica',90.00,1),(12,10,'Monster Ensalada','Monster_Ensalada_ensalada.png','Ensalada fresca con base de lechuga romana, pollo deshebrado, tocino crujiente, huevo, aguacate, queso azul y aderezo de la casa. Ideal para un almuerzo ligero pero sustancioso.',140.00,1),(13,6,'Mostudie','Mostudie_imagen_smudio.png','Esmudie',90.00,1);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre_empresa` varchar(100) NOT NULL,
  `nombre_contacto` varchar(50) NOT NULL,
  `apellido_pa` varchar(50) NOT NULL,
  `apellido_ma` varchar(50) DEFAULT NULL,
  `telefono` varchar(16) NOT NULL,
  `email` varchar(80) NOT NULL,
  `rfc` varchar(15) DEFAULT NULL,
  `direccion` varchar(255) NOT NULL,
  `id_categoria_proveedor` int NOT NULL,
  `fecha_registro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_proveedor`),
  UNIQUE KEY `nombre_empresa` (`nombre_empresa`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `rfc` (`rfc`),
  KEY `fk_proveedores_categoria` (`id_categoria_proveedor`),
  KEY `idx_proveedores_nombre_empresa` (`nombre_empresa`),
  KEY `idx_proveedores_activo` (`activo`),
  CONSTRAINT `fk_proveedores_categoria` FOREIGN KEY (`id_categoria_proveedor`) REFERENCES `categorias_proveedor` (`id_categoria_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (11,'Abarrotes del Bajio SA de CV','Luis','Navarro','Campos','4772010001','ventas@abarrotesbajio.com','ABJ230101A11','Blvd. Delta 1450, Leon, Gto.',1,'2026-02-21 09:00:00',1),(12,'Lacteos San Miguel','Patricia','Reyes','Lozano','4772010002','contacto@lacteossanmiguel.com','LSM230101B22','Av. Tecnologico 804, Leon, Gto.',2,'2026-02-21 09:10:00',1),(13,'Carnes Selectas del Centro','Rafael','Mendoza','Lara','4772010003','pedidos@carnescentro.com','CSC230101C33','Calle Industrial 220, Leon, Gto.',3,'2026-02-21 09:20:00',1),(14,'Bebidas y Refrescos del Norte','Miriam','Salas','Ortega','4772010004','ventas@bebidasnorte.com','BRN230101D44','Av. Transportistas 88, Leon, Gto.',4,'2026-02-21 09:30:00',1),(15,'Empaques y Desechables Plus','Oscar','Ibarra','Mejia','4772010005','compras@desechablesplus.com','EDP230101E55','Calle Comercio 511, Leon, Gto.',5,'2026-02-21 09:40:00',1);
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recetas`
--

DROP TABLE IF EXISTS `recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recetas` (
  `id_receta` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `id_insumo` int NOT NULL,
  `cantidad_requerida` decimal(10,4) NOT NULL,
  PRIMARY KEY (`id_receta`),
  UNIQUE KEY `uq_recetas` (`id_producto`,`id_insumo`),
  KEY `fk_recetas_insumo` (`id_insumo`),
  CONSTRAINT `fk_recetas_insumo` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`),
  CONSTRAINT `fk_recetas_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `chk_recetas_cantidad` CHECK ((`cantidad_requerida` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (4,6,11,0.6000),(6,6,13,150.0000),(7,6,10,55.0000),(8,1,1,1.0000),(9,7,6,1.0000),(10,7,5,50.0000),(12,7,7,50.0000),(13,7,59,50.0000),(14,7,40,15.0000),(16,7,8,15.0000),(17,8,19,1.0000),(18,8,21,50.0000),(19,8,5,30.0000),(20,8,59,15.0000),(21,8,4,20.0000),(22,8,20,40.0000),(24,9,14,15.0000),(25,9,10,40.0000),(26,9,11,0.6000),(27,12,29,80.0000),(28,12,36,100.0000),(29,12,49,20.0000),(31,12,39,60.0000),(32,12,48,20.0000),(33,10,37,1.0000),(34,10,20,80.0000),(35,10,21,50.0000),(36,10,39,60.0000),(37,7,17,10.0000),(38,10,17,20.0000),(39,10,29,30.0000),(40,10,40,15.0000),(42,12,56,60.0000),(43,3,19,1.0000),(44,3,36,110.0000),(45,3,34,50.0000),(46,3,60,30.0000),(47,3,17,25.0000),(48,3,5,20.0000),(49,3,4,20.0000),(50,3,35,90.0000),(51,11,2,150.0000),(52,11,1,1.0000),(53,11,3,20.0000),(54,11,4,15.0000),(55,11,5,30.0000),(56,11,59,15.0000),(57,11,40,10.0000),(58,11,8,10.0000),(59,11,9,15.0000),(60,5,22,150.0000),(61,5,23,50.0000),(62,5,24,5.0000),(63,2,22,350.0000),(64,2,7,150.0000),(65,2,46,100.0000),(67,2,53,33.0000),(68,2,32,33.0000),(69,13,16,120.0000),(70,13,25,120.0000),(71,13,18,40.0000);
/*!40000 ALTER TABLE `recetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  PRIMARY KEY (`id_rol`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'administrador','Acceso total al sistema'),(2,'gerente','Supervisa operaciones y reportes'),(3,'cajero','Gestiona ventas y cobros'),(4,'cocina','Visualiza y prepara pedidos'),(5,'cliente','Solicitudes de producción'),(6,'cocinero','Preparación de platos');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salidas_efectivo`
--

DROP TABLE IF EXISTS `salidas_efectivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salidas_efectivo` (
  `id_salida` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `fecha_salida` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_salida`),
  KEY `fk_salidas_usuario` (`id_usuario`),
  CONSTRAINT `fk_salidas_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `chk_salidas_monto` CHECK ((`monto` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salidas_efectivo`
--

LOCK TABLES `salidas_efectivo` WRITE;
/*!40000 ALTER TABLE `salidas_efectivo` DISABLE KEYS */;
INSERT INTO `salidas_efectivo` VALUES (1,4,2.00,'Para la pobreza','2026-04-06 18:29:26');
/*!40000 ALTER TABLE `salidas_efectivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitudes_produccion`
--

DROP TABLE IF EXISTS `solicitudes_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solicitudes_produccion` (
  `id_solicitud_prod` int NOT NULL AUTO_INCREMENT,
  `id_usuario_solicita` int NOT NULL,
  `id_producto` int NOT NULL,
  `id_orden_produccion` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  `estado` enum('Pendiente','En Proceso','Completada','Cancelada') NOT NULL DEFAULT 'Pendiente',
  `fecha_solicitud` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_completada` datetime DEFAULT NULL,
  `numero_orden` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_solicitud_prod`),
  KEY `fk_solicitudes_usuario` (`id_usuario_solicita`),
  KEY `fk_solicitudes_producto` (`id_producto`),
  KEY `idx_solicitudes_estado` (`estado`),
  KEY `idx_solicitudes_fecha` (`fecha_solicitud`),
  KEY `fk_solicitudes_orden` (`id_orden_produccion`),
  CONSTRAINT `fk_solicitudes_orden` FOREIGN KEY (`id_orden_produccion`) REFERENCES `ordenes_produccion` (`id_orden_produccion`),
  CONSTRAINT `fk_solicitudes_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  CONSTRAINT `fk_solicitudes_usuario` FOREIGN KEY (`id_usuario_solicita`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `chk_solicitudes_cantidad` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitudes_produccion`
--

LOCK TABLES `solicitudes_produccion` WRITE;
/*!40000 ALTER TABLE `solicitudes_produccion` DISABLE KEYS */;
INSERT INTO `solicitudes_produccion` VALUES (1,8,1,9,1,'En Proceso','2026-04-14 02:09:43',NULL,NULL),(2,8,6,10,1,'Completada','2026-04-15 21:57:30','2026-04-15 21:58:02',NULL);
/*!40000 ALTER TABLE `solicitudes_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `id_ticket` int NOT NULL AUTO_INCREMENT,
  `id_venta` int NOT NULL,
  `folio` varchar(20) NOT NULL,
  `fecha_emision` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `monto_pagado` decimal(10,2) NOT NULL,
  `leyenda` varchar(255) NOT NULL DEFAULT 'Gracias por comprar, pase por su producto en el mostrador',
  PRIMARY KEY (`id_ticket`),
  UNIQUE KEY `id_venta` (`id_venta`),
  UNIQUE KEY `folio` (`folio`),
  CONSTRAINT `fk_tickets_venta` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  CONSTRAINT `chk_tickets_monto` CHECK ((`monto_pagado` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

LOCK TABLES `tickets` WRITE;
/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (1,1,'TKT-00000001','2026-04-06 18:11:06',200.00,'Gracias por comprar, pase por su producto en el mostrador'),(2,2,'TKT-00000002','2026-04-06 18:20:17',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(3,3,'TKT-00000003','2026-04-06 18:28:42',149.90,'Gracias por comprar, pase por su producto en el mostrador'),(4,4,'TKT-00000004','2026-04-07 18:20:15',150.00,'Gracias por comprar, pase por su producto en el mostrador'),(5,5,'TKT-00000005','2026-04-08 19:16:06',50.00,'Gracias por comprar, pase por su producto en el mostrador'),(6,10,'TKT-00000010','2026-04-08 19:21:44',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(7,14,'TKT-00000014','2026-04-08 19:38:07',50.00,'Gracias por comprar, pase por su producto en el mostrador'),(8,15,'TKT-00000015','2026-04-08 20:07:26',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(9,16,'TKT-00000016','2026-04-10 17:37:03',500.00,'Gracias por comprar, pase por su producto en el mostrador'),(10,17,'TKT-00000017','2026-04-14 01:32:39',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(11,18,'TKT-00000018','2026-04-14 01:56:44',50.00,'Gracias por comprar, pase por su producto en el mostrador'),(12,19,'TKT-00000019','2026-04-14 02:22:05',50.00,'Gracias por comprar, pase por su producto en el mostrador'),(13,20,'TKT-00000020','2026-04-14 02:27:22',50.00,'Gracias por comprar, pase por su producto en el mostrador'),(14,21,'TKT-00000021','2026-04-14 18:04:42',50.00,'Gracias por comprar, pase por su producto en el mostrador'),(15,22,'TKT-00000022','2026-04-14 23:39:58',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(16,23,'TKT-00000023','2026-04-14 23:46:30',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(17,24,'TKT-00000024','2026-04-15 00:17:21',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(18,25,'TKT-00000025','2026-04-15 00:41:57',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(19,26,'TKT-00000026','2026-04-15 01:29:08',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(20,27,'TKT-00000027','2026-04-15 21:49:43',150.00,'Gracias por comprar, pase por su producto en el mostrador'),(21,28,'TKT-00000028','2026-04-15 21:52:35',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(22,29,'TKT-00000029','2026-04-16 01:00:02',250.00,'Gracias por comprar, pase por su producto en el mostrador'),(23,30,'TKT-00000030','2026-04-16 01:23:47',320.00,'Gracias por comprar, pase por su producto en el mostrador'),(24,31,'TKT-00000031','2026-04-16 03:02:52',200.00,'Gracias por comprar, pase por su producto en el mostrador'),(25,32,'TKT-00000032','2026-04-16 03:07:33',175.00,'Gracias por comprar, pase por su producto en el mostrador'),(26,33,'TKT-00000033','2026-04-16 03:08:47',180.00,'Gracias por comprar, pase por su producto en el mostrador'),(27,34,'TKT-00000034','2026-04-16 03:10:36',180.00,'Gracias por comprar, pase por su producto en el mostrador'),(29,35,'TKT-00000035','2026-04-16 03:21:55',180.00,'Gracias por comprar, pase por su producto en el mostrador'),(31,36,'TKT-00000036','2026-04-16 03:24:37',180.00,'Gracias por comprar, pase por su producto en el mostrador'),(33,37,'TKT-00000037','2026-04-16 03:25:31',35.00,'Gracias por comprar, pase por su producto en el mostrador'),(35,38,'TKT-00000038','2026-04-16 11:59:45',85.00,'Gracias por comprar, pase por su producto en el mostrador'),(37,39,'TKT-00000039','2026-04-16 19:56:15',100.00,'Gracias por comprar, pase por su producto en el mostrador'),(38,40,'TKT-00000040','2026-04-16 20:01:16',100.00,'Gracias por comprar, pase por su producto en el mostrador');
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidades_medida`
--

DROP TABLE IF EXISTS `unidades_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidades_medida` (
  `id_unidad_medida` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `abreviatura` varchar(10) NOT NULL,
  PRIMARY KEY (`id_unidad_medida`),
  UNIQUE KEY `nombre` (`nombre`),
  UNIQUE KEY `abreviatura` (`abreviatura`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_medida`
--

LOCK TABLES `unidades_medida` WRITE;
/*!40000 ALTER TABLE `unidades_medida` DISABLE KEYS */;
INSERT INTO `unidades_medida` VALUES (1,'Kilogramo','kg'),(2,'Gramo','g'),(3,'Litro','l'),(4,'Mililitro','ml'),(5,'Unidad','pz'),(6,'Caja','caja'),(7,'Bulto','bulto');
/*!40000 ALTER TABLE `unidades_medida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `id_persona` int NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(256) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `fs_uniquifier` varchar(255) NOT NULL,
  `fecha_registro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `bloqueado_hasta` datetime DEFAULT NULL,
  `intentos_fallidos` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `id_persona` (`id_persona`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `fs_uniquifier` (`fs_uniquifier`),
  KEY `idx_usuarios_active` (`active`),
  CONSTRAINT `fk_usuarios_persona` FOREIGN KEY (`id_persona`) REFERENCES `persona` (`id_persona`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,1,'transacciones@monstereats.com','pbkdf2:sha256:dummyhash',1,'uuid-transacciones-001','2026-04-04 23:09:21',NULL,0),(2,9,'cajero.demo@monstereats.com','scrypt:32768:8:1$cRBedI5z9KLeBWip$2a940672494ba38310cfc89edc035713ef18bdaf45560e9fc4d477adbc6ca8bc8940d87645727672aa92269c15076ef13d709ce98efdef0c542f63db623b431f',1,'8874a976bbae4f05bfb93f8e8100ddf1','2026-04-04 23:41:50',NULL,0),(3,11,'admin@monstereats.com','scrypt:32768:8:1$3XtReVxI5AA701M2$95544e470d97bd3a44fa110720dbd9899350284f35bf67d419800f3595ef7c1ab101e2ac38cbaa8afdac0b11864275acbdaf4e44370c8184be9f460d9c6c002e',1,'4dc0da36c3c74256b3712ce50f701b07','2026-04-04 23:45:09',NULL,0),(4,13,'gerente@monstereats.com','scrypt:32768:8:1$1yr8cDnDimWeBlDG$c42443e627209165736e27e2e746189ee242c5efd1cc393156364efb4c2833335e0735e5a59412f52996a4798ca1eb0b7315f6e48b2858637c295ac0059c4e77',1,'b26e44f689884d029b0e62b04dcb909c','2026-04-04 23:48:56',NULL,0),(5,17,'cocina@monstereats.com','scrypt:32768:8:1$EgyaR2PbMfpb4eT8$63dc23f1c62515e371aa7f1903adddc0f741516d9edaf4df80b7372b7339ce089d62a7f4ab6968a72a17249379d802dbaac226f4f543fd80f4909ef7e105b9c0',1,'fdd1d1261728452580b87470ecf4a1ce','2026-04-06 01:21:41',NULL,0),(6,19,'demo@monstereats.com','scrypt:32768:8:1$PawqA075wRaBJ02H$447164f8783c3553463bf9eb516c6f5ee4c67bf3954f5cd401572ad2c35f04b83d1ea25453524137858036ef1f1ff21094ad66bbbbc2cbf9934552b1812af2f2',1,'67b56f23bef541a4bfdab164516578a7','2026-04-06 01:29:42',NULL,0),(7,20,'test@monstereats.com','password123',1,'unique-test-user-001','2026-04-06 18:27:12',NULL,0),(8,21,'christoferriveravalderrama@gmail.com','pbkdf2:sha256:600000$ctWBnoMhlNb0REbG$796e4b6d460ec7cc00abcd482ea40957ca5835c337fbd14175ed9d94dd7b6ada',1,'e77b768ff4314d7689309f0ce2c426cd','2026-04-12 20:44:35',NULL,0),(10,24,'fitforrberts@gmail.com','scrypt:32768:8:1$by5f5ESy5tBfXIWR$1db4804500adc01585bf802dd5ee7af04102abfe14dc94b3f67e61af56b9d278c855356f27abf8ad6352c78749e7586c00937325b953a23b9cfeaf0f0dbd51fe',1,'9287ab88581c4f77b83131fbbcb2d2ee','2026-04-13 00:42:50',NULL,0),(11,25,'urielhenandez123@gmail.com','pbkdf2:sha256:600000$qWoO9NZedrP0zc65$ca11afbbfc8573a536519508f7b22910f0fbffbd68f7c6321309ca1d377c4435',1,'be25720266d14725b29a8f2af7cf57b5','2026-04-16 01:40:38',NULL,0),(12,26,'kevin.axel.rr12@gmail.com','scrypt:32768:8:1$cWSsRS33Nkq1aYVI$f84005a1ad5cd50c321d2f4ec3c6de3a36ad96c7b6fb053242a4792f1ab7ca7a630fdd369bd99e07fe23585a564861c58bcdfb3eb186c64a8a1cc840ff7eb3fd',1,'cf96079e-4363-4946-b839-e002d93a75c7','2026-04-16 17:21:01',NULL,0),(14,30,'arcadegonz@gmail.com','pbkdf2:sha256:600000$3ocJWor841Pt789O$f63f45ade86a08629f0339957da257aaa6386ee0d68ac28f2b0f44e9a5f3da2e',1,'3d76a28f8fc94882aaa6581b2e84de99','2026-04-16 17:59:44',NULL,0),(15,31,'kevax2021@gmail.com','pbkdf2:sha256:600000$Dtf1GNDcUxH3XQZd$afeb878d255b83830a33d5241320503b76bc219a78a6e1fedf2cff5c86e462fc',1,'6d4feed0997b42eea3dc80e323958fc3','2026-04-16 18:15:33',NULL,0);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_roles`
--

DROP TABLE IF EXISTS `usuarios_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_roles` (
  `id_usuario` int NOT NULL,
  `id_rol` int NOT NULL,
  PRIMARY KEY (`id_usuario`,`id_rol`),
  KEY `fk_ur_rol` (`id_rol`),
  CONSTRAINT `fk_ur_rol` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`),
  CONSTRAINT `fk_ur_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_roles`
--

LOCK TABLES `usuarios_roles` WRITE;
/*!40000 ALTER TABLE `usuarios_roles` DISABLE KEYS */;
INSERT INTO `usuarios_roles` VALUES (3,2),(4,2),(14,2),(2,3),(3,3),(4,3),(15,3),(3,4),(4,4),(5,4),(6,4),(12,4),(3,5),(4,5),(7,5),(10,5),(11,5);
/*!40000 ALTER TABLE `usuarios_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `v_historial_compras`
--

DROP TABLE IF EXISTS `v_historial_compras`;
/*!50001 DROP VIEW IF EXISTS `v_historial_compras`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_historial_compras` AS SELECT 
 1 AS `id_compra`,
 1 AS `fecha_compra`,
 1 AS `estado_compra`,
 1 AS `total`,
 1 AS `id_detalle_compra`,
 1 AS `cantidad_comprada`,
 1 AS `costo_unitario`,
 1 AS `costo_subtotal`,
 1 AS `insumo`,
 1 AS `unidad`,
 1 AS `id_usuario`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_insumos_completo`
--

DROP TABLE IF EXISTS `v_insumos_completo`;
/*!50001 DROP VIEW IF EXISTS `v_insumos_completo`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_insumos_completo` AS SELECT 
 1 AS `id_insumo`,
 1 AS `nombre`,
 1 AS `costo_unitario`,
 1 AS `merma_teorica`,
 1 AS `stock_actual`,
 1 AS `total_comprado`,
 1 AS `total_merma`,
 1 AS `merma_real`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_merma_por_mes`
--

DROP TABLE IF EXISTS `v_merma_por_mes`;
/*!50001 DROP VIEW IF EXISTS `v_merma_por_mes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_merma_por_mes` AS SELECT 
 1 AS `id_insumo`,
 1 AS `nombre`,
 1 AS `periodo`,
 1 AS `total_comprado`,
 1 AS `merma_teorica`,
 1 AS `merma_real`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_mermas_detallado`
--

DROP TABLE IF EXISTS `v_mermas_detallado`;
/*!50001 DROP VIEW IF EXISTS `v_mermas_detallado`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_mermas_detallado` AS SELECT 
 1 AS `id_merma`,
 1 AS `fecha`,
 1 AS `hora`,
 1 AS `insumo`,
 1 AS `cantidad`,
 1 AS `motivo`,
 1 AS `id_lote`,
 1 AS `fecha_caducidad`,
 1 AS `id_usuario`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_ordenesproduccion`
--

DROP TABLE IF EXISTS `v_ordenesproduccion`;
/*!50001 DROP VIEW IF EXISTS `v_ordenesproduccion`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_ordenesproduccion` AS SELECT 
 1 AS `id_orden_produccion`,
 1 AS `id_producto`,
 1 AS `producto`,
 1 AS `precio_venta`,
 1 AS `cantidad_programada`,
 1 AS `cantidad_producida`,
 1 AS `estado`,
 1 AS `fecha_creacion`,
 1 AS `fecha_inicio`,
 1 AS `fecha_finalizacion`,
 1 AS `observaciones`,
 1 AS `creado_por`,
 1 AS `responsable`,
 1 AS `validacion_stock`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_receta_detalle`
--

DROP TABLE IF EXISTS `v_receta_detalle`;
/*!50001 DROP VIEW IF EXISTS `v_receta_detalle`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_receta_detalle` AS SELECT 
 1 AS `id_producto`,
 1 AS `producto`,
 1 AS `descripcion`,
 1 AS `precio_venta`,
 1 AS `producto_activo`,
 1 AS `id_categoria`,
 1 AS `categoria`,
 1 AS `id_insumo`,
 1 AS `insumo`,
 1 AS `id_unidad_medida`,
 1 AS `unidad_medida`,
 1 AS `abreviatura`,
 1 AS `cantidad_requerida`,
 1 AS `costo_unitario`,
 1 AS `costo_parcial`,
 1 AS `porcentaje_merma`,
 1 AS `insumo_activo`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_recetas_listado`
--

DROP TABLE IF EXISTS `v_recetas_listado`;
/*!50001 DROP VIEW IF EXISTS `v_recetas_listado`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_recetas_listado` AS SELECT 
 1 AS `id_producto`,
 1 AS `producto`,
 1 AS `categoria`,
 1 AS `imagen`,
 1 AS `descripcion`,
 1 AS `precio_venta`,
 1 AS `activo`,
 1 AS `total_insumos`,
 1 AS `costo_produccion`,
 1 AS `utilidad`,
 1 AS `estado_receta`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_usuarios_detalle`
--

DROP TABLE IF EXISTS `v_usuarios_detalle`;
/*!50001 DROP VIEW IF EXISTS `v_usuarios_detalle`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_usuarios_detalle` AS SELECT 
 1 AS `id_usuario`,
 1 AS `email`,
 1 AS `active`,
 1 AS `fecha_registro`,
 1 AS `intentos_fallidos`,
 1 AS `id_persona`,
 1 AS `nombre`,
 1 AS `apellido_pa`,
 1 AS `apellido_ma`,
 1 AS `fecha_nac`,
 1 AS `telefono`,
 1 AS `id_rol`,
 1 AS `nombre_rol`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `v_ventas_pagadas`
--

DROP TABLE IF EXISTS `v_ventas_pagadas`;
/*!50001 DROP VIEW IF EXISTS `v_ventas_pagadas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `v_ventas_pagadas` AS SELECT 
 1 AS `id_venta`,
 1 AS `id_usuario`,
 1 AS `fecha_corte`,
 1 AS `fecha_hora`,
 1 AS `total`,
 1 AS `metodo`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `fecha_venta` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total` decimal(10,2) NOT NULL DEFAULT '0.00',
  `monto_recibido` decimal(10,2) DEFAULT NULL,
  `cambio` decimal(10,2) NOT NULL DEFAULT '0.00',
  `id_metodo_pago` int NOT NULL,
  `referencia_pago` varchar(50) DEFAULT NULL,
  `estado_venta` enum('Pendiente','Pagado','Cancelado') NOT NULL DEFAULT 'Pendiente',
  PRIMARY KEY (`id_venta`),
  KEY `fk_ventas_usuario` (`id_usuario`),
  KEY `fk_ventas_metodo_pago` (`id_metodo_pago`),
  KEY `idx_ventas_fecha` (`fecha_venta`),
  KEY `idx_ventas_estado` (`estado_venta`),
  CONSTRAINT `fk_ventas_metodo_pago` FOREIGN KEY (`id_metodo_pago`) REFERENCES `metodos_pago` (`id_metodo_pago`),
  CONSTRAINT `fk_ventas_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  CONSTRAINT `chk_ventas_total` CHECK ((`total` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,4,'2026-04-06 18:11:06',149.90,200.00,50.10,1,'EFECTIVO','Pagado'),(2,4,'2026-04-06 18:20:17',49.90,100.00,50.10,1,'EFECTIVO','Pagado'),(3,4,'2026-04-06 18:28:42',149.90,NULL,0.00,2,'1234567890123456','Pagado'),(4,4,'2026-04-07 18:20:15',149.90,150.00,0.10,1,'EFECTIVO','Pagado'),(5,4,'2026-04-08 19:16:06',49.90,50.00,0.10,1,'EFECTIVO','Pagado'),(10,4,'2026-04-08 19:21:44',74.90,100.00,25.10,1,'EFECTIVO','Pagado'),(14,4,'2026-04-08 19:38:07',49.90,50.00,0.10,1,'EFECTIVO','Pagado'),(15,4,'2026-04-08 20:07:26',89.90,100.00,10.10,1,'EFECTIVO','Pagado'),(16,4,'2026-04-10 17:37:03',329.90,500.00,170.10,1,'EFECTIVO','Pagado'),(17,8,'2026-04-14 01:32:39',45.00,100.00,55.00,1,'EFECTIVO','Pagado'),(18,8,'2026-04-14 01:56:44',45.00,50.00,5.00,1,'EFECTIVO','Pagado'),(19,8,'2026-04-14 02:22:05',45.00,50.00,5.00,1,'EFECTIVO','Pagado'),(20,8,'2026-04-14 02:27:22',45.00,50.00,5.00,1,'EFECTIVO','Pagado'),(21,8,'2026-04-14 18:04:41',45.00,50.00,5.00,1,'EFECTIVO','Pagado'),(22,8,'2026-04-14 23:39:58',90.00,100.00,10.00,1,'EFECTIVO','Pagado'),(23,8,'2026-04-14 23:46:30',90.00,100.00,10.00,1,'EFECTIVO','Pagado'),(24,8,'2026-04-15 00:17:21',80.00,100.00,20.00,1,'EFECTIVO','Pagado'),(25,8,'2026-04-15 00:41:57',80.00,100.00,20.00,1,'EFECTIVO','Pagado'),(26,8,'2026-04-15 01:29:08',80.00,100.00,20.00,1,'EFECTIVO','Pagado'),(27,8,'2026-04-15 21:49:43',125.00,150.00,25.00,1,'EFECTIVO','Pagado'),(28,8,'2026-04-15 21:52:35',80.00,100.00,20.00,1,'EFECTIVO','Pagado'),(29,8,'2026-04-16 01:00:02',218.00,250.00,32.00,1,'EFECTIVO','Pagado'),(30,8,'2026-04-16 01:23:47',308.00,320.00,12.00,1,'EFECTIVO','Pagado'),(31,8,'2026-04-16 03:02:52',200.00,200.00,0.00,1,'EFECTIVO','Pagado'),(32,8,'2026-04-16 03:07:33',175.00,NULL,0.00,2,'1122334455667788','Pagado'),(33,8,'2026-04-16 03:08:47',180.00,NULL,0.00,2,'1122334455667788','Pagado'),(34,8,'2026-04-16 03:10:36',180.00,NULL,0.00,2,'1122334455667788','Pagado'),(35,8,'2026-04-16 03:21:55',180.00,NULL,0.00,2,'1234567890123456','Pagado'),(36,8,'2026-04-16 03:24:37',180.00,NULL,0.00,2,'1122334455667788','Pagado'),(37,8,'2026-04-16 03:25:31',35.00,NULL,0.00,2,'1122334455667788','Pagado'),(38,8,'2026-04-16 11:59:45',85.00,NULL,0.00,2,'1122334455667788','Pagado'),(39,15,'2026-04-16 19:56:15',90.00,100.00,10.00,1,'EFECTIVO','Pagado'),(40,15,'2026-04-16 20:01:16',95.00,100.00,5.00,1,'EFECTIVO','Pagado');
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas_borrador`
--

DROP TABLE IF EXISTS `ventas_borrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_borrador` (
  `id_venta_borrador` bigint NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `descuento_global` decimal(10,2) NOT NULL DEFAULT '0.00',
  `estado` enum('ABIERTA','PROCESADA','CANCELADA') NOT NULL DEFAULT 'ABIERTA',
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_venta_borrador`),
  KEY `fk_vb_usuario` (`id_usuario`),
  CONSTRAINT `fk_vb_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_borrador`
--

LOCK TABLES `ventas_borrador` WRITE;
/*!40000 ALTER TABLE `ventas_borrador` DISABLE KEYS */;
INSERT INTO `ventas_borrador` VALUES (1,4,0.00,'PROCESADA','2026-04-06 17:47:49','2026-04-06 18:11:06'),(2,4,0.00,'PROCESADA','2026-04-06 18:20:03','2026-04-06 18:20:17'),(3,4,0.00,'PROCESADA','2026-04-06 18:22:57','2026-04-06 18:28:42'),(4,4,0.00,'PROCESADA','2026-04-07 17:44:04','2026-04-07 18:20:15'),(5,4,0.00,'PROCESADA','2026-04-08 17:44:36','2026-04-08 19:16:06'),(6,4,0.00,'PROCESADA','2026-04-08 19:20:21','2026-04-08 19:21:44'),(7,4,0.00,'PROCESADA','2026-04-08 19:21:55','2026-04-08 19:38:07'),(8,4,0.00,'PROCESADA','2026-04-08 20:07:02','2026-04-08 20:07:26'),(9,4,0.00,'PROCESADA','2026-04-08 23:57:06','2026-04-10 17:37:03'),(10,8,0.00,'PROCESADA','2026-04-14 00:47:46','2026-04-14 01:32:39'),(11,8,0.00,'PROCESADA','2026-04-14 01:56:36','2026-04-14 01:56:44'),(12,8,0.00,'PROCESADA','2026-04-14 02:21:39','2026-04-14 02:22:05'),(13,8,0.00,'PROCESADA','2026-04-14 02:26:11','2026-04-14 02:27:22'),(14,8,0.00,'PROCESADA','2026-04-14 18:03:48','2026-04-14 18:04:42'),(15,8,0.00,'PROCESADA','2026-04-14 18:28:08','2026-04-14 23:39:58'),(16,8,0.00,'PROCESADA','2026-04-14 23:45:10','2026-04-14 23:46:30'),(17,8,0.00,'PROCESADA','2026-04-15 00:16:24','2026-04-15 00:17:21'),(18,8,0.00,'PROCESADA','2026-04-15 00:41:48','2026-04-15 00:41:57'),(19,8,0.00,'PROCESADA','2026-04-15 01:27:55','2026-04-15 01:29:08'),(20,8,0.00,'PROCESADA','2026-04-15 01:41:05','2026-04-15 21:49:43'),(21,8,0.00,'PROCESADA','2026-04-15 21:51:42','2026-04-15 21:52:35'),(22,8,0.00,'PROCESADA','2026-04-16 00:46:54','2026-04-16 01:00:02'),(23,8,0.00,'PROCESADA','2026-04-16 01:01:06','2026-04-16 01:23:47'),(24,8,0.00,'PROCESADA','2026-04-16 03:02:44','2026-04-16 03:02:52'),(27,8,0.00,'PROCESADA','2026-04-16 03:07:33','2026-04-16 03:07:33'),(28,8,0.00,'PROCESADA','2026-04-16 03:08:47','2026-04-16 03:08:47'),(29,8,0.00,'PROCESADA','2026-04-16 03:10:36','2026-04-16 03:10:36'),(30,8,0.00,'PROCESADA','2026-04-16 03:21:55','2026-04-16 03:21:55'),(31,8,0.00,'PROCESADA','2026-04-16 03:24:37','2026-04-16 03:24:37'),(32,8,0.00,'PROCESADA','2026-04-16 03:25:31','2026-04-16 03:25:31'),(34,8,0.00,'PROCESADA','2026-04-16 11:59:45','2026-04-16 11:59:45'),(35,15,0.00,'PROCESADA','2026-04-16 19:55:38','2026-04-16 19:56:15'),(36,15,0.00,'PROCESADA','2026-04-16 20:01:05','2026-04-16 20:01:16');
/*!40000 ALTER TABLE `ventas_borrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vista_proveedores`
--

DROP TABLE IF EXISTS `vista_proveedores`;
/*!50001 DROP VIEW IF EXISTS `vista_proveedores`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_proveedores` AS SELECT 
 1 AS `id_proveedor`,
 1 AS `nombre_empresa`,
 1 AS `nombre_contacto`,
 1 AS `apellido_pa`,
 1 AS `apellido_ma`,
 1 AS `contacto_completo`,
 1 AS `telefono`,
 1 AS `email`,
 1 AS `rfc`,
 1 AS `direccion`,
 1 AS `activo`,
 1 AS `id_categoria_proveedor`,
 1 AS `nombre_categoria`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_carrito_detalle`
--

DROP TABLE IF EXISTS `vw_carrito_detalle`;
/*!50001 DROP VIEW IF EXISTS `vw_carrito_detalle`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_carrito_detalle` AS SELECT 
 1 AS `id_usuario`,
 1 AS `id_item`,
 1 AS `nombre`,
 1 AS `categoria`,
 1 AS `tipo_item`,
 1 AS `cantidad`,
 1 AS `precio_unitario`,
 1 AS `descuento_unitario`,
 1 AS `subtotal_linea`,
 1 AS `descuento_linea`,
 1 AS `total_linea`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_carrito_resumen`
--

DROP TABLE IF EXISTS `vw_carrito_resumen`;
/*!50001 DROP VIEW IF EXISTS `vw_carrito_resumen`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_carrito_resumen` AS SELECT 
 1 AS `id_usuario`,
 1 AS `subtotal`,
 1 AS `descuento`,
 1 AS `total`,
 1 AS `total_piezas`,
 1 AS `lineas`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_costo_combos`
--

DROP TABLE IF EXISTS `vw_costo_combos`;
/*!50001 DROP VIEW IF EXISTS `vw_costo_combos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_costo_combos` AS SELECT 
 1 AS `id_combo`,
 1 AS `nombre`,
 1 AS `precio_venta`,
 1 AS `activo`,
 1 AS `costo_produccion`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_costo_productos`
--

DROP TABLE IF EXISTS `vw_costo_productos`;
/*!50001 DROP VIEW IF EXISTS `vw_costo_productos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_costo_productos` AS SELECT 
 1 AS `id_producto`,
 1 AS `nombre`,
 1 AS `precio_venta`,
 1 AS `activo`,
 1 AS `costo_produccion`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_costo_utilidad`
--

DROP TABLE IF EXISTS `vw_costo_utilidad`;
/*!50001 DROP VIEW IF EXISTS `vw_costo_utilidad`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_costo_utilidad` AS SELECT 
 1 AS `id_producto`,
 1 AS `nombre`,
 1 AS `tipo`,
 1 AS `precio_venta`,
 1 AS `costo_produccion`,
 1 AS `utilidad`,
 1 AS `margen_ganancia`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_historial_caja`
--

DROP TABLE IF EXISTS `vw_historial_caja`;
/*!50001 DROP VIEW IF EXISTS `vw_historial_caja`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_historial_caja` AS SELECT 
 1 AS `id_movimiento_caja`,
 1 AS `fecha_movimiento`,
 1 AS `tipo_movimiento`,
 1 AS `monto`,
 1 AS `saldo_anterior`,
 1 AS `saldo_nuevo`,
 1 AS `referencia`,
 1 AS `atendido_por`,
 1 AS `id_venta`,
 1 AS `estado_venta`,
 1 AS `metodo_pago`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_inventario_productos`
--

DROP TABLE IF EXISTS `vw_inventario_productos`;
/*!50001 DROP VIEW IF EXISTS `vw_inventario_productos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_inventario_productos` AS SELECT 
 1 AS `id_producto`,
 1 AS `nombre`,
 1 AS `precio_venta`,
 1 AS `activo`,
 1 AS `stock_actual`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_kds_cocina`
--

DROP TABLE IF EXISTS `vw_kds_cocina`;
/*!50001 DROP VIEW IF EXISTS `vw_kds_cocina`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_kds_cocina` AS SELECT 
 1 AS `id_detalle`,
 1 AS `numero_orden`,
 1 AS `fecha_venta`,
 1 AS `id_producto`,
 1 AS `platillo`,
 1 AS `cantidad`,
 1 AS `estado_cocina`,
 1 AS `cajero`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_kds_unificado`
--

DROP TABLE IF EXISTS `vw_kds_unificado`;
/*!50001 DROP VIEW IF EXISTS `vw_kds_unificado`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_kds_unificado` AS SELECT 
 1 AS `id_tarea`,
 1 AS `id_origen`,
 1 AS `origen`,
 1 AS `folio`,
 1 AS `fecha_hora`,
 1 AS `id_producto`,
 1 AS `platillo`,
 1 AS `cantidad`,
 1 AS `estado`,
 1 AS `solicitante`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_productos_produccion`
--

DROP TABLE IF EXISTS `vw_productos_produccion`;
/*!50001 DROP VIEW IF EXISTS `vw_productos_produccion`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_productos_produccion` AS SELECT 
 1 AS `id_producto`,
 1 AS `nombre_producto`,
 1 AS `categoria`,
 1 AS `stock_actual`,
 1 AS `stock_minimo`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_productos_ventas`
--

DROP TABLE IF EXISTS `vw_productos_ventas`;
/*!50001 DROP VIEW IF EXISTS `vw_productos_ventas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_productos_ventas` AS SELECT 
 1 AS `id_item`,
 1 AS `nombre`,
 1 AS `categoria`,
 1 AS `precio_venta`,
 1 AS `activo`,
 1 AS `imagen`,
 1 AS `stock`,
 1 AS `tipo_item`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_salidas_efectivo`
--

DROP TABLE IF EXISTS `vw_salidas_efectivo`;
/*!50001 DROP VIEW IF EXISTS `vw_salidas_efectivo`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_salidas_efectivo` AS SELECT 
 1 AS `id`,
 1 AS `fecha_hora`,
 1 AS `monto`,
 1 AS `motivo`,
 1 AS `atendido_por`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_tablero_cocina`
--

DROP TABLE IF EXISTS `vw_tablero_cocina`;
/*!50001 DROP VIEW IF EXISTS `vw_tablero_cocina`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_tablero_cocina` AS SELECT 
 1 AS `id_solicitud_prod`,
 1 AS `cantidad`,
 1 AS `estado`,
 1 AS `fecha_solicitud`,
 1 AS `nombre_producto`,
 1 AS `tipo_orden`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_ticket_cabecera`
--

DROP TABLE IF EXISTS `vw_ticket_cabecera`;
/*!50001 DROP VIEW IF EXISTS `vw_ticket_cabecera`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_ticket_cabecera` AS SELECT 
 1 AS `id_venta`,
 1 AS `folio`,
 1 AS `fecha_emision`,
 1 AS `leyenda`,
 1 AS `total`,
 1 AS `monto_recibido`,
 1 AS `cambio`,
 1 AS `metodo_pago`,
 1 AS `cajero`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_ticket_detalle`
--

DROP TABLE IF EXISTS `vw_ticket_detalle`;
/*!50001 DROP VIEW IF EXISTS `vw_ticket_detalle`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_ticket_detalle` AS SELECT 
 1 AS `id_venta`,
 1 AS `id_producto`,
 1 AS `producto`,
 1 AS `tipo_item`,
 1 AS `cantidad`,
 1 AS `precio_unitario`,
 1 AS `subtotal`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_ticket_encabezado`
--

DROP TABLE IF EXISTS `vw_ticket_encabezado`;
/*!50001 DROP VIEW IF EXISTS `vw_ticket_encabezado`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_ticket_encabezado` AS SELECT 
 1 AS `id_ticket`,
 1 AS `id_venta`,
 1 AS `folio`,
 1 AS `fecha_emision`,
 1 AS `cajero`,
 1 AS `metodo_pago`,
 1 AS `total`,
 1 AS `monto_recibido`,
 1 AS `cambio`,
 1 AS `referencia_pago`,
 1 AS `monto_pagado`,
 1 AS `leyenda`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_ticket_impresion`
--

DROP TABLE IF EXISTS `vw_ticket_impresion`;
/*!50001 DROP VIEW IF EXISTS `vw_ticket_impresion`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_ticket_impresion` AS SELECT 
 1 AS `id_ticket`,
 1 AS `id_venta`,
 1 AS `folio`,
 1 AS `fecha_emision`,
 1 AS `cajero`,
 1 AS `metodo_pago`,
 1 AS `total`,
 1 AS `monto_recibido`,
 1 AS `cambio`,
 1 AS `referencia_pago`,
 1 AS `monto_pagado`,
 1 AS `leyenda`,
 1 AS `id_producto`,
 1 AS `producto`,
 1 AS `tipo_item`,
 1 AS `cantidad`,
 1 AS `precio_unitario`,
 1 AS `subtotal`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_utilidad_diaria`
--

DROP TABLE IF EXISTS `vw_utilidad_diaria`;
/*!50001 DROP VIEW IF EXISTS `vw_utilidad_diaria`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_utilidad_diaria` AS SELECT 
 1 AS `fecha`,
 1 AS `transacciones_ventas`,
 1 AS `total_ventas`,
 1 AS `costo_produccion`,
 1 AS `registros_salidas`,
 1 AS `total_salidas`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'monster_eats_db'
--
/*!50106 SET @save_time_zone= @@TIME_ZONE */ ;
/*!50106 DROP EVENT IF EXISTS `ev_backup_full` */;
DELIMITER ;;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;;
/*!50003 SET character_set_client  = utf8mb4 */ ;;
/*!50003 SET character_set_results = utf8mb4 */ ;;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;;
/*!50003 SET @saved_time_zone      = @@time_zone */ ;;
/*!50003 SET time_zone             = 'SYSTEM' */ ;;
/*!50106 CREATE*/ /*!50117 DEFINER=`Gerente`@`localhost`*/ /*!50106 EVENT `ev_backup_full` ON SCHEDULE EVERY 1 DAY STARTS '2026-04-14 03:00:00' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN

    DECLARE done INT DEFAULT 0;
    DECLARE v_name VARCHAR(255);

    DECLARE cur_tables CURSOR FOR 
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'monster_eats_db'
          AND table_type = 'BASE TABLE';

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur_tables;

    tablas_loop: LOOP
        FETCH cur_tables INTO v_name;
        IF done THEN LEAVE tablas_loop; END IF;

        SET @drop_sql = CONCAT(
            'DROP TABLE IF EXISTS monster_eats_backup.', v_name
        );
        PREPARE stmt FROM @drop_sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

        SET @create_sql = CONCAT(
            'CREATE TABLE monster_eats_backup.', v_name,
            ' SELECT * FROM monster_eats_db.', v_name
        );
        PREPARE stmt FROM @create_sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

    END LOOP;

    CLOSE cur_tables;

    SET done = 0;

    DELETE FROM monster_eats_backup.backup_vistas;

    INSERT INTO monster_eats_backup.backup_vistas (nombre, definicion)
    SELECT table_name, view_definition
    FROM information_schema.views
    WHERE table_schema = 'monster_eats_db';

    DELETE FROM monster_eats_backup.backup_procedures;

    INSERT INTO monster_eats_backup.backup_procedures (nombre, definicion)
    SELECT routine_name, routine_definition
    FROM information_schema.routines
    WHERE routine_schema = 'monster_eats_db'
      AND routine_type = 'PROCEDURE';

    DELETE FROM monster_eats_backup.backup_triggers;

    INSERT INTO monster_eats_backup.backup_triggers (nombre, definicion)
    SELECT trigger_name, action_statement
    FROM information_schema.triggers
    WHERE trigger_schema = 'monster_eats_db';

END */ ;;
/*!50003 SET time_zone             = @saved_time_zone */ ;;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;;
/*!50003 SET character_set_client  = @saved_cs_client */ ;;
/*!50003 SET character_set_results = @saved_cs_results */ ;;
/*!50003 SET collation_connection  = @saved_col_connection */ ;;
DELIMITER ;
/*!50106 SET TIME_ZONE= @save_time_zone */ ;

--
-- Dumping routines for database 'monster_eats_db'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_actualizar_categoria_proveedor` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_actualizar_categoria_proveedor`(
    IN p_id INT,
    IN p_nombre VARCHAR(50)
)
BEGIN
    DECLARE v_existe INT DEFAULT 0;

    -- Validamos si el NUEVO nombre ya lo tiene OTRA categoría diferente
    SELECT COUNT(*) INTO v_existe
    FROM categorias_proveedor
    WHERE LOWER(TRIM(nombre)) = LOWER(TRIM(p_nombre))
      AND id_categoria_proveedor != p_id;

    IF v_existe > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Ya existe otra categoría con ese nombre.';
    ELSE
        UPDATE categorias_proveedor
        SET nombre = TRIM(p_nombre)
        WHERE id_categoria_proveedor = p_id;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_actualizar_proveedor` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_actualizar_proveedor`(
    IN p_id INT,
    IN p_empresa VARCHAR(100),
    IN p_contacto VARCHAR(100),
    IN p_apellido_pa VARCHAR(100),
    IN p_apellido_ma VARCHAR(100),
    IN p_telefono VARCHAR(20),
    IN p_email VARCHAR(100),
    IN p_rfc VARCHAR(20),
    IN p_direccion VARCHAR(255),
    IN p_id_categoria INT
)
BEGIN
    DECLARE v_existe_empresa INT DEFAULT 0;
    DECLARE v_existe_rfc INT DEFAULT 0;

    -- 1. Validar empresa (que no choque con otro ID distinto)
    SELECT COUNT(*) INTO v_existe_empresa 
    FROM proveedores 
    WHERE LOWER(TRIM(nombre_empresa)) = LOWER(TRIM(p_empresa)) 
      AND id_proveedor != p_id;
      
    IF v_existe_empresa > 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Error: Otra empresa ya está usando ese nombre.';
    END IF;

    -- 2. Validar RFC (que no choque con otro ID distinto)
    IF p_rfc IS NOT NULL AND TRIM(p_rfc) != '' THEN
        SELECT COUNT(*) INTO v_existe_rfc 
        FROM proveedores 
        WHERE UPPER(TRIM(rfc)) = UPPER(TRIM(p_rfc)) 
          AND id_proveedor != p_id;
          
        IF v_existe_rfc > 0 THEN
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Error: El RFC ingresado ya pertenece a otro proveedor.';
        END IF;
    END IF;

    -- 3. Hacemos el Update
    UPDATE proveedores
    SET nombre_empresa = TRIM(p_empresa),
        nombre_contacto = TRIM(p_contacto),
        apellido_pa = TRIM(p_apellido_pa),
        apellido_ma = TRIM(p_apellido_ma),
        telefono = TRIM(p_telefono),
        email = TRIM(p_email),
        rfc = UPPER(TRIM(p_rfc)),
        direccion = TRIM(p_direccion),
        id_categoria_proveedor = p_id_categoria
    WHERE id_proveedor = p_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_ajustar_stock_producto` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_ajustar_stock_producto`(
    IN p_id_producto INT,
    IN p_cantidad_ajuste INT,
    IN p_motivo VARCHAR(255),
    IN p_id_usuario INT
)
BEGIN
    DECLARE v_stock_anterior INT;
    DECLARE v_stock_nuevo INT;
    
    -- Manejador de Errores: Si algo falla, deshace la transacción
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL; 
    END;

    -- Inicia la transacción blindada
    START TRANSACTION;
    
    -- Bloqueamos la fila (FOR UPDATE) para que nadie más la edite al mismo tiempo
    SELECT stock_actual INTO v_stock_anterior 
    FROM inventario_productos 
    WHERE id_producto = p_id_producto FOR UPDATE;
    
    SET v_stock_nuevo = v_stock_anterior + p_cantidad_ajuste;
    
    -- Validamos directo en BD que no quede negativo
    IF v_stock_nuevo < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error_Stock_Negativo';
    END IF;

    -- Actualizamos inventario
    UPDATE inventario_productos 
    SET stock_actual = v_stock_nuevo 
    WHERE id_producto = p_id_producto;

    -- Insertamos el historial
    INSERT INTO movimientos_inventario_productos 
    (id_producto, tipo_movimiento, cantidad, stock_anterior, stock_nuevo, motivo, id_usuario, fecha_movimiento)
    VALUES 
    (p_id_producto, 'AJUSTE_MANUAL', ABS(p_cantidad_ajuste), v_stock_anterior, v_stock_nuevo, p_motivo, p_id_usuario, NOW());

    -- Confirmamos los cambios
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_cancelar_compra` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_cancelar_compra`(
    IN p_id_compra INT,
    IN p_id_usuario INT
)
BEGIN

    -- VARIABLES
    DECLARE v_id_insumo INT;
    DECLARE v_id_lote INT;
    DECLARE v_cantidad DECIMAL(12,4);
    DECLARE v_cantidad_inicial DECIMAL(12,4);

    DECLARE v_stock_anterior DECIMAL(12,4);
    DECLARE v_stock_nuevo DECIMAL(12,4);

    DECLARE done INT DEFAULT 0;

    --  CURSOR PROTEGIDO CONTRA NULL
    DECLARE cur_detalle CURSOR FOR
        SELECT 
            dc.id_insumo, 
            li.id_lote, 
            IFNULL(li.cantidad_disponible, 0),
            IFNULL(li.cantidad_inicial, 0)
        FROM detalle_compras dc
        JOIN lotes_insumo li 
            ON li.id_detalle_compra = dc.id_detalle_compra
        WHERE dc.id_compra = p_id_compra;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- MANEJO DE ERRORES
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- VALIDAR EXISTENCIA
    IF NOT EXISTS (SELECT 1 FROM compras WHERE id_compra = p_id_compra) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La compra no existe';
    END IF;

    -- VALIDAR ESTADO
    IF (SELECT estado_compra FROM compras WHERE id_compra = p_id_compra) = 'Cancelada' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La compra ya esta cancelada';
    END IF;

    OPEN cur_detalle;

    read_loop: LOOP

        FETCH cur_detalle INTO v_id_insumo, v_id_lote, v_cantidad, v_cantidad_inicial;

        IF done THEN
            LEAVE read_loop;
        END IF;

        --  PROTECCIÓN EXTRA (por si algo raro pasa)
        SET v_cantidad = IFNULL(v_cantidad, 0);
        SET v_cantidad_inicial = IFNULL(v_cantidad_inicial, 0);

        -- IGNORAR LOTES EN 0
        IF v_cantidad <= 0 THEN
            ITERATE read_loop;
        END IF;

        -- VALIDAR SI YA FUE CONSUMIDO
        IF v_cantidad < v_cantidad_inicial THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No se puede cancelar, el lote ya fue consumido';
        END IF;

        -- STOCK GLOBAL
        SELECT IFNULL(SUM(cantidad_disponible),0)
        INTO v_stock_anterior
        FROM lotes_insumo
        WHERE id_insumo = v_id_insumo;

        SET v_stock_nuevo = v_stock_anterior - v_cantidad;

        -- ACTUALIZAR LOTE
        UPDATE lotes_insumo
        SET cantidad_disponible = 0
        WHERE id_lote = v_id_lote;

        -- MOVIMIENTO REVERSO CON MOTIVO
        INSERT INTO movimientos_inventario_insumos (
            id_insumo,
            tipo_movimiento,
            cantidad,
            stock_anterior,
            stock_nuevo,
            referencia_tabla,
            referencia_id,
            id_usuario,
            id_lote,
            motivo
        )
        VALUES (
            v_id_insumo,
            'REVERSO_COMPRA',
            v_cantidad,
            v_stock_anterior,
            v_stock_nuevo,
            'compras',
            p_id_compra,
            p_id_usuario,
            v_id_lote,
            CONCAT('Auditoria: Cancelacion de compra #', p_id_compra)
        );

    END LOOP;

    CLOSE cur_detalle;

    -- CANCELAR COMPRA
    UPDATE compras
    SET estado_compra = 'Cancelada'
    WHERE id_compra = p_id_compra;

    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_carrito_agregar` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_carrito_agregar`(
    IN p_id_usuario INT,
    IN p_id_item INT,
    IN p_tipo_item VARCHAR(50),
    IN p_cantidad INT
)
BEGIN
    DECLARE v_id_borrador BIGINT;
    DECLARE v_precio DECIMAL(10,2);
    DECLARE v_cantidad INT DEFAULT 1;

    DECLARE v_stock INT DEFAULT 0;
    DECLARE v_cantidad_actual INT DEFAULT 0;
    DECLARE v_msg TEXT;

    -- =========================
    -- VALIDAR CANTIDAD
    -- =========================
    IF p_cantidad IS NOT NULL AND p_cantidad > 0 THEN
        SET v_cantidad = p_cantidad;
    END IF;

    -- =========================
    -- OBTENER CARRITO
    -- =========================
    SELECT id_venta_borrador INTO v_id_borrador
    FROM ventas_borrador
    WHERE id_usuario = p_id_usuario AND estado = 'ABIERTA'
    LIMIT 1;

    IF v_id_borrador IS NULL THEN
        INSERT INTO ventas_borrador (id_usuario, estado)
        VALUES (p_id_usuario, 'ABIERTA');

        SET v_id_borrador = LAST_INSERT_ID();
    END IF;

    -- =========================
    -- PRECIO
    -- =========================
    IF UPPER(p_tipo_item) = 'COMBO' THEN
        SELECT precio_venta INTO v_precio
        FROM combos
        WHERE id_combo = p_id_item AND activo = 1
        LIMIT 1;
    ELSE
        SELECT precio_venta INTO v_precio
        FROM productos
        WHERE id_producto = p_id_item AND activo = 1
        LIMIT 1;
    END IF;

    IF v_precio IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El artículo no está disponible.';
    END IF;

    -- =========================
    -- STOCK DISPONIBLE (SEGURA)
    -- =========================
    SELECT COALESCE(stock, 0) INTO v_stock
    FROM vw_productos_ventas
    WHERE id_item = p_id_item
      AND tipo_item = 
        CASE 
            WHEN UPPER(p_tipo_item) = 'COMBO' THEN 'Combo'
            ELSE 'Producto'
        END
    LIMIT 1;

    -- Si no encontró fila
    IF v_stock IS NULL THEN
        SET v_stock = 0;
    END IF;

    -- =========================
    -- CANTIDAD ACTUAL (SEGURA)
    -- =========================
    IF UPPER(p_tipo_item) = 'COMBO' THEN
        SELECT COALESCE(cantidad, 0) INTO v_cantidad_actual
        FROM detalle_ventas_borrador
        WHERE id_venta_borrador = v_id_borrador
          AND id_combo = p_id_item
        LIMIT 1;
    ELSE
        SELECT COALESCE(cantidad, 0) INTO v_cantidad_actual
        FROM detalle_ventas_borrador
        WHERE id_venta_borrador = v_id_borrador
          AND id_producto = p_id_item
        LIMIT 1;
    END IF;

    -- Si no existe registro
    IF v_cantidad_actual IS NULL THEN
        SET v_cantidad_actual = 0;
    END IF;

    -- =========================
    -- VALIDACIÓN FINAL
    -- =========================
    IF (v_cantidad_actual + v_cantidad) > v_stock THEN

    SET v_msg = CONCAT(
        'Stock insuficiente. Disponible: ',
        GREATEST(v_stock - v_cantidad_actual, 0)
    );

    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = v_msg;

END IF;

    -- =========================
    -- INSERTAR / ACTUALIZAR
    -- =========================
    IF UPPER(p_tipo_item) = 'COMBO' THEN

        INSERT INTO detalle_ventas_borrador
            (id_venta_borrador, id_combo, id_producto, cantidad, precio_unitario, descuento_unitario)
        VALUES
            (v_id_borrador, p_id_item, NULL, v_cantidad, v_precio, 0.00)
        ON DUPLICATE KEY UPDATE
            cantidad = cantidad + v_cantidad,
            precio_unitario = v_precio;

    ELSE

        INSERT INTO detalle_ventas_borrador
            (id_venta_borrador, id_producto, id_combo, cantidad, precio_unitario, descuento_unitario)
        VALUES
            (v_id_borrador, p_id_item, NULL, v_cantidad, v_precio, 0.00)
        ON DUPLICATE KEY UPDATE
            cantidad = cantidad + v_cantidad,
            precio_unitario = v_precio;

    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_carrito_agregar_online` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_carrito_agregar_online`(
  IN p_id_usuario INT,
  IN p_id_item INT,
  IN p_tipo VARCHAR(16),
  IN p_cantidad INT
)
BEGIN
  DECLARE v_id_borrador BIGINT;
  DECLARE v_precio DECIMAL(10,2);

  START TRANSACTION;
  SELECT id_venta_borrador INTO v_id_borrador
    FROM ventas_borrador
    WHERE id_usuario = p_id_usuario AND estado = 'ABIERTA'
    LIMIT 1;

  IF v_id_borrador IS NULL THEN
    INSERT INTO ventas_borrador (id_usuario, descuento_global, estado) VALUES (p_id_usuario, 0.00, 'ABIERTA');
    SET v_id_borrador = LAST_INSERT_ID();
  END IF;

  IF LOWER(p_tipo) = 'producto' THEN
    SELECT precio_venta INTO v_precio FROM productos WHERE id_producto = p_id_item LIMIT 1;
    IF v_precio IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Producto inválido'; END IF;
    INSERT INTO detalle_ventas_borrador (id_venta_borrador, id_producto, cantidad, precio_unitario)
      VALUES (v_id_borrador, p_id_item, p_cantidad, v_precio)
    ON DUPLICATE KEY UPDATE cantidad = cantidad + p_cantidad, precio_unitario = VALUES(precio_unitario);
  ELSE
    SELECT precio_venta INTO v_precio FROM combos WHERE id_combo = p_id_item LIMIT 1;
    IF v_precio IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Combo inválido'; END IF;
    INSERT INTO detalle_ventas_borrador (id_venta_borrador, id_combo, cantidad, precio_unitario)
      VALUES (v_id_borrador, p_id_item, p_cantidad, v_precio)
    ON DUPLICATE KEY UPDATE cantidad = cantidad + p_cantidad, precio_unitario = VALUES(precio_unitario);
  END IF;

  COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_carrito_eliminar_producto` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_carrito_eliminar_producto`(
    IN p_id_usuario INT,
    IN p_id_item INT,
    IN p_tipo_item VARCHAR(20)
)
BEGIN
    DECLARE v_id_borrador BIGINT;

    SELECT id_venta_borrador INTO v_id_borrador FROM ventas_borrador
    WHERE id_usuario = p_id_usuario AND estado = 'ABIERTA' LIMIT 1;

    IF v_id_borrador IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe carrito activo.';
    END IF;

    IF p_tipo_item = 'Combo' THEN
        DELETE FROM detalle_ventas_borrador WHERE id_venta_borrador = v_id_borrador AND id_combo = p_id_item;
    ELSE
        DELETE FROM detalle_ventas_borrador WHERE id_venta_borrador = v_id_borrador AND id_producto = p_id_item;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_carrito_quitar_unidad` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_carrito_quitar_unidad`(
    IN p_id_usuario INT,
    IN p_id_item INT,
    IN p_tipo_item VARCHAR(20)
)
BEGIN
    DECLARE v_id_borrador BIGINT;
    DECLARE v_cantidad_actual INT;

    SELECT id_venta_borrador INTO v_id_borrador FROM ventas_borrador
    WHERE id_usuario = p_id_usuario AND estado = 'ABIERTA' LIMIT 1;

    IF v_id_borrador IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe carrito activo.';
    END IF;

    IF p_tipo_item = 'Combo' THEN
        SELECT cantidad INTO v_cantidad_actual FROM detalle_ventas_borrador
        WHERE id_venta_borrador = v_id_borrador AND id_combo = p_id_item;
    ELSE
        SELECT cantidad INTO v_cantidad_actual FROM detalle_ventas_borrador
        WHERE id_venta_borrador = v_id_borrador AND id_producto = p_id_item;
    END IF;

    IF v_cantidad_actual IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El artículo no está en el carrito.';
    END IF;

    IF v_cantidad_actual = 1 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Mínimo permitido. Usa el botón "Quitar" para eliminar.';
    END IF;

    IF p_tipo_item = 'Combo' THEN
        UPDATE detalle_ventas_borrador SET cantidad = cantidad - 1
        WHERE id_venta_borrador = v_id_borrador AND id_combo = p_id_item;
    ELSE
        UPDATE detalle_ventas_borrador SET cantidad = cantidad - 1
        WHERE id_venta_borrador = v_id_borrador AND id_producto = p_id_item;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_completar_solicitud` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_completar_solicitud`(IN p_id_solicitud INT)
BEGIN
    -- Manejador de errores para mantener la integridad (Rollback automático)
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL; 
    END;

    START TRANSACTION;
    
    -- Actualizamos el estado a 'Completada' y registramos la hora exacta de finalización
    UPDATE solicitudes_produccion
    SET estado = 'Completada', fecha_completada = NOW()
    WHERE id_solicitud_prod = p_id_solicitud;
    
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_crear_categoria_proveedor` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_crear_categoria_proveedor`(
	IN p_nombre_categoria VARCHAR(100)
)
BEGIN
	-- Declaramos la variable para saber si existe la categoria
    DECLARE v_existe INT DEFAULT 0;
    
    -- Buscamos si ya existe la categoria igual
    SELECT COUNT(*) INTO v_existe
    FROM categorias_proveedor
    WHERE LOWER(TRIM(nombre)) = LOWER(TRIM(p_nombre_categoria));
    
    -- Validacion
    IF v_existe > 0 THEN
		-- Si existe, mandamos un error que Flask pueda atrapar y guardarlo en los logs
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Ya existe un usuario con el mismo nombre de la categoria para el proveedor';
	ELSE
		-- Si no existe, hacemos el registro
        INSERT INTO categorias_proveedor (nombre) 
        VALUES (TRIM(p_nombre_categoria));
	END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_crear_combo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_crear_combo`(
    IN p_nombre VARCHAR(100),
    IN p_descripcion VARCHAR(255),
    IN p_precio_venta DECIMAL(10,2),
    IN p_imagen VARCHAR(255),
    OUT p_out_id INT
)
BEGIN
    INSERT INTO combos (nombre, descripcion, precio_venta, imagen, activo)
    VALUES (p_nombre, p_descripcion, p_precio_venta, p_imagen, 1);
    
    -- Atrapamos el ID que se acaba de crear para devolvérselo a Python
    SET p_out_id = LAST_INSERT_ID();
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_crear_proveedor` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_crear_proveedor`(
	IN p_empresa      VARCHAR (100),
    IN p_contacto     VARCHAR (100),
    IN p_apellido_pa  VARCHAR (100),
    IN p_apellido_ma  VARCHAR (100),
    IN p_telefono     VARCHAR (15),
    IN p_email        VARCHAR (100),
    IN p_rfc          VARCHAR (13),
    IN p_direccion    VARCHAR(255),
    IN p_id_categoria INT
)
BEGIN
	DECLARE v_exist_empresa INT DEFAULT 0;
    DECLARE v_exist_rfc INT DEFAULT 0;
    
    -- Validamos que la empresa no exista ignorando mayus/minusculas
    SELECT COUNT(*) INTO v_exist_empresa
    FROM proveedores
    WHERE LOWER(TRIM(nombre_empresa)) = LOWER(TRIM(p_empresa));
    
    IF v_exist_empresa > 0 THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Ya existe un proveedor con ese nombre de empresa';
	END IF;
    
    -- Validamos que el RFC no esté duplicado
    IF p_rfc IS NOT NULL AND TRIM(p_rfc) != '' THEN
		SELECT COUNT(*) INTO v_exist_rfc
        FROM proveedores
        WHERE UPPER(TRIM(rfc)) = UPPER(TRIM(p_rfc));
        
        IF v_exist_rfc > 0 THEN
			SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: El RFC ingresado ya esta registrado con otro proveedor';
		END IF;
	END IF;
    
    -- Insertamos 
    INSERT INTO proveedores (nombre_empresa, nombre_contacto, apellido_pa, apellido_ma, telefono, email, rfc, direccion, id_categoria_proveedor, activo, fecha_registro) 
    VALUES (
		TRIM(p_empresa), TRIM(p_contacto), TRIM(p_apellido_pa), TRIM(p_apellido_ma), 
        TRIM(p_telefono), TRIM(p_email), UPPER(TRIM(p_rfc)), TRIM(p_direccion), 
        p_id_categoria, 1, NOW()
        );
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Crear_Usuario` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Crear_Usuario`(
    IN p_nombre VARCHAR(50),
    IN p_apellido_pa VARCHAR(50),
    IN p_apellido_ma VARCHAR(50),
    IN p_fecha_nac DATE,
    IN p_telefono VARCHAR(16),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(256),
    IN p_fs_uniquifier VARCHAR(255),
    IN p_id_rol INT
)
BEGIN
    DECLARE v_id_persona INT;
    DECLARE v_id_usuario INT;
    
    -- Si hay un error, deshacemos todo (Rollback)
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    -- 1. Crear a la Persona
    INSERT INTO persona (nombre, apellido_pa, apellido_ma, fecha_nac, telefono)
    VALUES (p_nombre, p_apellido_pa, IFNULL(p_apellido_ma, ''), p_fecha_nac, p_telefono);
    
    -- Sacar el ID que se acaba de generar
    SET v_id_persona = LAST_INSERT_ID();

    -- 2. Crear al Usuario (el 1 es de active = True)
    INSERT INTO usuarios (id_persona, email, password, active, fs_uniquifier, fecha_registro, intentos_fallidos)
    VALUES (v_id_persona, p_email, p_password, 1, p_fs_uniquifier, NOW(), 0);
    
    SET v_id_usuario = LAST_INSERT_ID();

    -- 3. Asignar el Rol
    IF p_id_rol IS NOT NULL THEN
        INSERT INTO usuarios_roles (id_usuario, id_rol)
        VALUES (v_id_usuario, p_id_rol);
    END IF;

    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_editar_combo_detalle` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_editar_combo_detalle`(
    IN p_id_combo INT,
    IN p_id_producto INT,
    IN p_cantidad INT
)
BEGIN
    INSERT INTO detalle_combos (id_combo, id_producto, cantidad)
    VALUES (p_id_combo, p_id_producto, p_cantidad);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_editar_combo_info` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_editar_combo_info`(
    IN p_id_combo INT,
    IN p_nombre VARCHAR(100),
    IN p_descripcion VARCHAR(255),
    IN p_precio_venta DECIMAL(10,2),
    IN p_imagen VARCHAR(255)
)
BEGIN
    UPDATE combos 
    SET nombre = p_nombre, 
        descripcion = p_descripcion, 
        precio_venta = p_precio_venta, 
        imagen = p_imagen
    WHERE id_combo = p_id_combo;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Editar_Usuario` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Editar_Usuario`(
    IN p_id_usuario INT,
    IN p_nombre VARCHAR(50),
    IN p_apellido_pa VARCHAR(50),
    IN p_apellido_ma VARCHAR(50),
    IN p_fecha_nac DATE,
    IN p_telefono VARCHAR(16),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(256), -- Si no la cambian, mándala como NULL
    IN p_id_rol INT
)
BEGIN
    DECLARE v_id_persona INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    -- Sacamos el ID de la persona ligada a este usuario
    SELECT id_persona INTO v_id_persona FROM usuarios WHERE id_usuario = p_id_usuario;

    -- 1. Actualizar datos de la persona
    UPDATE persona 
    SET nombre = p_nombre, 
        apellido_pa = p_apellido_pa, 
        apellido_ma = IFNULL(p_apellido_ma, ''), 
        fecha_nac = p_fecha_nac, 
        telefono = p_telefono
    WHERE id_persona = v_id_persona;

    -- 2. Actualizar datos del usuario (validando la contraseña)
    IF p_password IS NOT NULL AND p_password != '' THEN
        UPDATE usuarios 
        SET email = p_email, password = p_password
        WHERE id_usuario = p_id_usuario;
    ELSE
        UPDATE usuarios 
        SET email = p_email
        WHERE id_usuario = p_id_usuario;
    END IF;

    -- 3. Actualizar el rol
    IF p_id_rol IS NOT NULL THEN
        -- Borramos el viejo y metemos el nuevo
        DELETE FROM usuarios_roles WHERE id_usuario = p_id_usuario;
        INSERT INTO usuarios_roles (id_usuario, id_rol) VALUES (p_id_usuario, p_id_rol);
    END IF;

    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_eliminar_categoria_proveedor` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_eliminar_categoria_proveedor`(
    IN p_id INT
)
BEGIN
    DECLARE v_en_uso INT DEFAULT 0;

    -- Validamos si hay proveedores que actualmente usan esta categoría
    SELECT COUNT(*) INTO v_en_uso
    FROM proveedores
    WHERE id_categoria_proveedor = p_id;

    IF v_en_uso > 0 THEN
        -- Si está en uso, bloqueamos el borrado
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No se puede eliminar la categoría porque hay proveedores usándola.';
    ELSE
        -- Si está libre, la borramos sin piedad
        DELETE FROM categorias_proveedor
        WHERE id_categoria_proveedor = p_id;
    END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_eliminar_proveedor` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_eliminar_proveedor`(
    IN p_id INT
)
BEGIN
    -- No lo borramos físicamente, solo lo desactivamos 
    UPDATE proveedores
    SET activo = 0
    WHERE id_proveedor = p_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_guardar_corte_caja` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_guardar_corte_caja`(IN p_fecha DATE, IN p_id_usuario INT)
BEGIN
    DECLARE v_total_efectivo DECIMAL(10,2) DEFAULT 0;
    DECLARE v_id_caja INT;
    DECLARE v_saldo_anterior DECIMAL(12,2) DEFAULT 0;
    DECLARE v_saldo_nuevo DECIMAL(12,2) DEFAULT 0;
    
    -- 1. VALIDACIÓN: Comprobar si ya existe un corte para este usuario hoy
    IF EXISTS (
        SELECT 1 FROM movimientos_caja 
        WHERE id_usuario = p_id_usuario 
          AND tipo_movimiento = 'AJUSTE' 
          AND DATE(fecha_movimiento) = p_fecha 
          AND referencia LIKE 'Corte de caja%'
    ) THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Ya has realizado el corte de caja el día de hoy.';
    END IF;

    -- 2. Calcular el efectivo del día
    SELECT COALESCE(SUM(total), 0) INTO v_total_efectivo
    FROM v_ventas_pagadas
    WHERE fecha_corte = p_fecha 
      AND id_usuario = p_id_usuario 
      AND metodo = 'Efectivo';
      
    -- 3. Si hay efectivo, hacer el movimiento
    IF v_total_efectivo > 0 THEN
        SELECT id_caja, saldo_actual INTO v_id_caja, v_saldo_anterior
        FROM caja
        WHERE activa = 1
        LIMIT 1;
        
        IF v_id_caja IS NOT NULL THEN
            SET v_saldo_nuevo = v_saldo_anterior - v_total_efectivo;
            
            INSERT INTO movimientos_caja (
                id_caja, id_usuario, tipo_movimiento, monto, 
                saldo_anterior, saldo_nuevo, referencia, fecha_movimiento
            ) VALUES (
                v_id_caja, p_id_usuario, 'AJUSTE', v_total_efectivo, 
                v_saldo_anterior, v_saldo_nuevo, 
                CONCAT('Corte de caja - Efectivo retirado del ', DATE_FORMAT(p_fecha, '%d/%m/%Y')), 
                NOW()
            );
            
            UPDATE caja 
            SET saldo_actual = v_saldo_nuevo 
            WHERE id_caja = v_id_caja;
        END IF;
    END IF;
    
    SELECT v_total_efectivo AS monto_retirado;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_KDS_Despachar` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_KDS_Despachar`(
    IN p_id_origen INT,
    IN p_origen VARCHAR(20),
    IN p_id_usuario INT
)
BEGIN
    DECLARE v_id_producto INT;
    DECLARE v_cantidad_pedida INT;
    DECLARE v_id_insumo INT;
    DECLARE v_cantidad_receta DECIMAL(10,4);
    DECLARE v_cantidad_total_descontar DECIMAL(10,4);
    DECLARE v_id_lote INT;
    DECLARE v_stock_producto_pre_hecho INT DEFAULT 0;
    DECLARE v_disponible_lote DECIMAL(10,4);
    
    -- Variables para el historial de movimientos
    DECLARE v_cantidad_descontada_este_lote DECIMAL(10,4);
    DECLARE v_stock_insumo_global DECIMAL(12,4);
    
    DECLARE done INT DEFAULT 0;

    -- Cursor para iterar sobre TODOS los ingredientes de la receta
    DECLARE cur_receta CURSOR FOR 
        SELECT id_insumo, cantidad_requerida 
        FROM recetas 
        WHERE id_producto = v_id_producto;
        
    -- Este handler SOLO debe dispararse cuando FETCH termine de leer toda la receta
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- En caso de error (como la alerta de falta de stock), deshacer todo
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- ========================================================
    -- 1. IDENTIFICAR EL ORIGEN Y DESCONTAR PRODUCTO TERMINADO
    -- ========================================================
    IF p_origen = 'Venta' THEN
        SELECT id_producto, cantidad INTO v_id_producto, v_cantidad_pedida
        FROM detalle_ventas WHERE id_detalle = p_id_origen FOR UPDATE;
        
        UPDATE detalle_ventas SET estado_cocina = 'Listo' WHERE id_detalle = p_id_origen;
        
        -- COALESCE(SUM()) es seguro y no dispara el NOT FOUND
        SELECT COALESCE(SUM(stock_actual), 0) INTO v_stock_producto_pre_hecho
        FROM inventario_productos WHERE id_producto = v_id_producto FOR UPDATE;
        
        -- Si hay stock del producto ya terminado, lo descontamos primero
        IF v_stock_producto_pre_hecho > 0 THEN
            IF v_stock_producto_pre_hecho >= v_cantidad_pedida THEN
                UPDATE inventario_productos 
                SET stock_actual = stock_actual - v_cantidad_pedida 
                WHERE id_producto = v_id_producto;
                
                INSERT INTO movimientos_inventario_productos (id_producto, tipo_movimiento, cantidad, stock_anterior, stock_nuevo, referencia_tabla, referencia_id, motivo, id_usuario)
                VALUES (v_id_producto, 'SALIDA_VENTA', v_cantidad_pedida, v_stock_producto_pre_hecho, v_stock_producto_pre_hecho - v_cantidad_pedida, 'detalle_ventas', p_id_origen, 'Despacho total desde stock pre-producido', p_id_usuario);
                
                SET v_cantidad_pedida = 0;
            ELSE
                UPDATE inventario_productos SET stock_actual = 0 WHERE id_producto = v_id_producto;
                
                INSERT INTO movimientos_inventario_productos (id_producto, tipo_movimiento, cantidad, stock_anterior, stock_nuevo, referencia_tabla, referencia_id, motivo, id_usuario)
                VALUES (v_id_producto, 'SALIDA_VENTA', v_stock_producto_pre_hecho, v_stock_producto_pre_hecho, 0, 'detalle_ventas', p_id_origen, 'Despacho parcial desde stock pre-producido', p_id_usuario);
                
                SET v_cantidad_pedida = v_cantidad_pedida - v_stock_producto_pre_hecho;
            END IF;
        END IF;

    ELSEIF p_origen = 'Producción' THEN
        SELECT id_producto, cantidad_programada INTO v_id_producto, v_cantidad_pedida
        FROM ordenes_produccion WHERE id_orden_produccion = p_id_origen FOR UPDATE;
        
        UPDATE ordenes_produccion 
        SET estado = 'Completada', 
            cantidad_producida = v_cantidad_pedida, 
            fecha_finalizacion = NOW(), 
            id_usuario_responsable = p_id_usuario
        WHERE id_orden_produccion = p_id_origen;

        UPDATE solicitudes_produccion 
        SET estado = 'Completada', 
            fecha_completada = NOW() 
        WHERE id_orden_produccion = p_id_origen;
        
        INSERT INTO inventario_productos (id_producto, stock_actual) 
        VALUES (v_id_producto, v_cantidad_pedida)
        ON DUPLICATE KEY UPDATE stock_actual = stock_actual + v_cantidad_pedida;
        
    END IF;

    -- ========================================================
    -- 2. DESCONTAR INSUMOS DE LA RECETA (Si quedó algo pendiente)
    -- ========================================================
    IF v_cantidad_pedida > 0 THEN
        SET done = 0; 
        
        OPEN cur_receta;
        read_loop: LOOP
            FETCH cur_receta INTO v_id_insumo, v_cantidad_receta;
            
            -- Si ya no hay ingredientes en la receta, salir del bucle
            IF done = 1 THEN LEAVE read_loop; END IF;

            SET v_cantidad_total_descontar = v_cantidad_receta * v_cantidad_pedida;

            WHILE v_cantidad_total_descontar > 0 DO
                
                -- ¡CORRECCIÓN!: Buscamos lotes VIGENTES (fecha_caducidad >= hoy)
                SET v_id_lote = (
                    SELECT id_lote 
                    FROM lotes_insumo 
                    WHERE id_insumo = v_id_insumo 
                      AND cantidad_disponible > 0 
                      AND fecha_caducidad >= CURRENT_DATE  -- <-- ESTA ES LA CLAVE
                    ORDER BY fecha_caducidad ASC 
                    LIMIT 1
                );
                
                IF v_id_lote IS NOT NULL THEN
                    
                    -- Volvemos a usar asignaciones seguras
                    SET v_disponible_lote = (SELECT cantidad_disponible FROM lotes_insumo WHERE id_lote = v_id_lote);
                    SET v_stock_insumo_global = (SELECT COALESCE(SUM(cantidad_disponible), 0) FROM lotes_insumo WHERE id_insumo = v_id_insumo);

                    -- Descuento de lotes
                    IF v_disponible_lote >= v_cantidad_total_descontar THEN
                        SET v_cantidad_descontada_este_lote = v_cantidad_total_descontar;
                        UPDATE lotes_insumo SET cantidad_disponible = cantidad_disponible - v_cantidad_total_descontar WHERE id_lote = v_id_lote;
                        SET v_cantidad_total_descontar = 0;
                    ELSE
                        SET v_cantidad_descontada_este_lote = v_disponible_lote;
                        UPDATE lotes_insumo SET cantidad_disponible = 0 WHERE id_lote = v_id_lote;
                        SET v_cantidad_total_descontar = v_cantidad_total_descontar - v_disponible_lote;
                    END IF;

                    -- Guardar el registro de movimiento contable
                    INSERT INTO movimientos_inventario_insumos (
                        id_insumo, tipo_movimiento, cantidad, stock_anterior, stock_nuevo, 
                        referencia_tabla, referencia_id, motivo, id_usuario, id_lote
                    ) VALUES (
                        v_id_insumo, 'SALIDA_PRODUCCION', v_cantidad_descontada_este_lote, 
                        v_stock_insumo_global, v_stock_insumo_global - v_cantidad_descontada_este_lote, 
                        IF(p_origen = 'Venta', 'detalle_ventas', 'ordenes_produccion'), 
                        p_id_origen, CONCAT('Despacho en cocina por orden de ', p_origen), p_id_usuario, v_id_lote
                    );

                ELSE
                    -- Si explota, te avisa si fue porque se acabó o porque está caducado
                    SIGNAL SQLSTATE '45000' 
                    SET MESSAGE_TEXT = 'Error: Stock insuficiente o caducado para uno de los insumos. Deseche la merma caducada y abastezca.';
                END IF;

            END WHILE;
        END LOOP read_loop;
        CLOSE cur_receta;
    END IF;

    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_KDS_MarcarListo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_KDS_MarcarListo`(
    IN p_id_detalle INT,
    IN p_id_usuario INT
)
BEGIN
    -- Manejo de errores de seguridad
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
 
    START TRANSACTION;
 
    -- ÚNICA ACCIÓN: Cambiar el estado a "Listo" para que desaparezca de la pantalla del cocinero
    -- y le aparezca al mesero/cajero para entregar.
    UPDATE detalle_ventas
    SET estado_cocina = 'Listo'
    WHERE id_detalle = p_id_detalle;
 
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Produccion_Cancelar` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Produccion_Cancelar`(
    IN p_id_orden INT,
    IN p_motivo VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    UPDATE ordenes_produccion
    SET estado = 'Cancelada',
        observaciones = CONCAT(COALESCE(observaciones, ''), ' | Cancelada: ', p_motivo)
    WHERE id_orden_produccion = p_id_orden;
    
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Produccion_CrearOrden` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Produccion_CrearOrden`(
    IN p_id_producto INT,
    IN p_id_usuario_crea INT,
    IN p_cantidad_programada INT,
    IN p_observaciones VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    INSERT INTO ordenes_produccion (
        id_producto, 
        id_usuario_crea, 
        cantidad_programada, 
        cantidad_producida,
        estado, 
        observaciones, 
        fecha_creacion
    ) VALUES (
        p_id_producto, 
        p_id_usuario_crea, 
        p_cantidad_programada,
        0,
        'Pendiente', 
        p_observaciones, 
        NOW()
    );
    
    COMMIT;
    
    SELECT LAST_INSERT_ID() AS id_orden;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Produccion_Finalizar` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Produccion_Finalizar`(
    IN p_id_orden INT,
    IN p_cantidad_producida INT,
    IN p_id_usuario INT
)
BEGIN
    DECLARE v_cantidad_programada INT;
    DECLARE v_id_producto INT;
    DECLARE v_merma INT;
    DECLARE v_stock_actual INT;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Obtener datos de la orden
    SELECT cantidad_programada, id_producto 
    INTO v_cantidad_programada, v_id_producto
    FROM ordenes_produccion 
    WHERE id_orden_produccion = p_id_orden;
    
    -- Validar que la orden esté en proceso
    IF (SELECT estado FROM ordenes_produccion WHERE id_orden_produccion = p_id_orden) != 'En Proceso' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La orden no está en estado "En Proceso"';
    END IF;
    
    -- Validar que la cantidad producida no exceda la programada
    IF p_cantidad_producida > v_cantidad_programada THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cantidad producida no puede exceder la cantidad programada';
    END IF;
    
    -- Calcular merma
    SET v_merma = v_cantidad_programada - p_cantidad_producida;
    
    -- Actualizar orden
    UPDATE ordenes_produccion
    SET estado = 'Completada',
        cantidad_producida = p_cantidad_producida,
        fecha_finalizacion = NOW()
    WHERE id_orden_produccion = p_id_orden;
    
    -- Registrar merma si la hay
    IF v_merma > 0 THEN
        INSERT INTO mermas_log (id_insumo, cantidad, motivo, id_usuario)
        SELECT 
            r.id_insumo,
            r.cantidad_requerida * v_merma,
            CONCAT('Merma en producción de orden ', p_id_orden, ' - Faltante de ', v_merma, ' unidades'),
            p_id_usuario
        FROM recetas r
        WHERE r.id_producto = v_id_producto;
    END IF;
    
    -- Obtener stock actual del producto
    SELECT COALESCE(stock_actual, 0) INTO v_stock_actual
    FROM inventario_productos 
    WHERE id_producto = v_id_producto;
    
    -- Agregar al inventario de productos terminados
    IF v_stock_actual > 0 THEN
        UPDATE inventario_productos
        SET stock_actual = stock_actual + p_cantidad_producida
        WHERE id_producto = v_id_producto;
    ELSE
        INSERT INTO inventario_productos (id_producto, stock_actual)
        VALUES (v_id_producto, p_cantidad_producida);
    END IF;
    
    -- Registrar movimiento de entrada de productos
    INSERT INTO movimientos_inventario_productos (
        id_producto, tipo_movimiento, cantidad, stock_anterior, stock_nuevo,
        referencia_tabla, referencia_id, motivo, id_usuario, fecha_movimiento
    ) VALUES (
        v_id_producto,
        'ENTRADA_PRODUCCION',
        p_cantidad_producida,
        v_stock_actual,
        v_stock_actual + p_cantidad_producida,
        'ordenes_produccion',
        p_id_orden,
        CONCAT('Producción finalizada de ', p_cantidad_producida, ' unidades de producto'),
        p_id_usuario,
        NOW()
    );
    
    COMMIT;
    
    SELECT p_cantidad_producida AS producido, v_merma AS merma;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Produccion_Iniciar` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Produccion_Iniciar`(
    IN p_id_orden INT,
    IN p_id_usuario_responsable INT
)
BEGIN
    DECLARE v_stock_suficiente BOOLEAN;
    DECLARE v_mensaje VARCHAR(255);
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Validar stock
    CALL SP_Produccion_ValidarStock(p_id_orden, v_stock_suficiente, v_mensaje);
    
    IF v_stock_suficiente = FALSE THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = v_mensaje;
    END IF;
    
    -- Actualizar estado de la orden
    UPDATE ordenes_produccion
    SET estado = 'En Proceso',
        id_usuario_responsable = p_id_usuario_responsable,
        fecha_inicio = NOW()
    WHERE id_orden_produccion = p_id_orden;
    
    -- Descontar insumos de lotes (usando FIFO - primero en expirar primero en salir)
    -- Esta es una versión simplificada
    UPDATE lotes_insumo li
    JOIN (
        SELECT 
            r.id_insumo,
            SUM(r.cantidad_requerida * op.cantidad_programada) AS cantidad_total
        FROM ordenes_produccion op
        JOIN recetas r ON op.id_producto = r.id_producto
        WHERE op.id_orden_produccion = p_id_orden
        GROUP BY r.id_insumo
    ) AS requerido ON li.id_insumo = requerido.id_insumo
    SET li.cantidad_disponible = li.cantidad_disponible - requerido.cantidad_total
    WHERE li.cantidad_disponible >= requerido.cantidad_total;
    
    -- Registrar movimientos
    INSERT INTO movimientos_inventario_insumos (
        id_insumo, tipo_movimiento, cantidad, stock_anterior, stock_nuevo,
        referencia_tabla, referencia_id, motivo, id_usuario, fecha_movimiento
    )
    SELECT 
        r.id_insumo,
        'SALIDA_PRODUCCION',
        r.cantidad_requerida * op.cantidad_programada,
        COALESCE(SUM(li.cantidad_disponible) + r.cantidad_requerida * op.cantidad_programada, 0),
        COALESCE(SUM(li.cantidad_disponible), 0),
        'ordenes_produccion',
        p_id_orden,
        CONCAT('Producción de ', op.cantidad_programada, ' unidades de ', p.nombre),
        p_id_usuario_responsable,
        NOW()
    FROM ordenes_produccion op
    JOIN productos p ON op.id_producto = p.id_producto
    JOIN recetas r ON op.id_producto = r.id_producto
    LEFT JOIN lotes_insumo li ON r.id_insumo = li.id_insumo
    WHERE op.id_orden_produccion = p_id_orden
    GROUP BY r.id_insumo, r.cantidad_requerida, op.cantidad_programada, p.nombre;
    
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Produccion_ValidarStock` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Produccion_ValidarStock`(
    IN p_id_orden INT,
    OUT p_stock_suficiente BOOLEAN,
    OUT p_mensaje VARCHAR(255)
)
BEGIN
    DECLARE v_faltante INT DEFAULT 0;
    
    SELECT COUNT(*) INTO v_faltante
    FROM ordenes_produccion op
    JOIN recetas r ON op.id_producto = r.id_producto
    LEFT JOIN (
        SELECT li.id_insumo, COALESCE(SUM(li.cantidad_disponible), 0) AS stock_total
        FROM lotes_insumo li
        GROUP BY li.id_insumo
    ) AS stock ON r.id_insumo = stock.id_insumo
    WHERE op.id_orden_produccion = p_id_orden
    AND (stock.stock_total IS NULL OR stock.stock_total < r.cantidad_requerida * op.cantidad_programada);
    
    IF v_faltante > 0 THEN
        SET p_stock_suficiente = FALSE;
        SET p_mensaje = 'No hay suficiente stock de materia prima para esta producción';
    ELSE
        SET p_stock_suficiente = TRUE;
        SET p_mensaje = 'Stock suficiente';
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Recetas_AgregarInsumo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Recetas_AgregarInsumo`(
    IN p_id_producto INT,
    IN p_id_insumo INT,
    IN p_cantidad_requerida DECIMAL(10,4)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Validar que el insumo exista y esté activo
    IF NOT EXISTS (SELECT 1 FROM insumos WHERE id_insumo = p_id_insumo AND activo = 1) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El insumo no existe o está inactivo';
    END IF;
    
    -- Validar que el producto exista y esté activo
    IF NOT EXISTS (SELECT 1 FROM productos WHERE id_producto = p_id_producto AND activo = 1) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto no existe o está inactivo';
    END IF;
    
    -- Validar cantidad positiva
    IF p_cantidad_requerida <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La cantidad requerida debe ser mayor a 0';
    END IF;
    
    -- Insertar o actualizar (si ya existe, actualiza la cantidad)
    INSERT INTO recetas (id_producto, id_insumo, cantidad_requerida)
    VALUES (p_id_producto, p_id_insumo, p_cantidad_requerida)
    ON DUPLICATE KEY UPDATE 
        cantidad_requerida = p_cantidad_requerida;
    
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Recetas_EliminarInsumo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Recetas_EliminarInsumo`(
    IN p_id_producto INT,
    IN p_id_insumo INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    DELETE FROM recetas
    WHERE id_producto = p_id_producto AND id_insumo = p_id_insumo;
    
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Recetas_InsumosDisponibles` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Recetas_InsumosDisponibles`(
    IN p_id_producto INT,
    IN p_search VARCHAR(100)
)
BEGIN
    -- Insumos que NO están ya en la receta
    SELECT 
        i.id_insumo,
        i.nombre,
        um.nombre AS unidad_medida,
        um.abreviatura,
        i.costo_unitario,
        i.activo
    FROM insumos i
    JOIN unidades_medida um ON i.id_unidad_medida = um.id_unidad_medida
    WHERE i.activo = 1
    AND i.id_insumo NOT IN (
        SELECT id_insumo FROM recetas WHERE id_producto = p_id_producto
    )
    AND (p_search IS NULL OR p_search = '' OR i.nombre LIKE CONCAT('%', p_search, '%'))
    ORDER BY i.nombre;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Recetas_Limpiar` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Recetas_Limpiar`(
    IN p_id_producto INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    DELETE FROM recetas WHERE id_producto = p_id_producto;
    
    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Recetas_ObtenerDetalle` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Recetas_ObtenerDetalle`(
    IN p_id_producto INT
)
BEGIN
    -- Información del producto (incluyendo descripcion)
    SELECT DISTINCT
        p.id_producto,
        p.nombre AS producto,
        p.descripcion,
        p.precio_venta,
        c.nombre AS categoria,
        p.activo,
        COALESCE(SUM(r.cantidad_requerida * i.costo_unitario), 0) AS costo_total
    FROM productos p
    JOIN categorias c ON p.id_categoria = c.id_categoria
    LEFT JOIN recetas r ON p.id_producto = r.id_producto
    LEFT JOIN insumos i ON r.id_insumo = i.id_insumo
    WHERE p.id_producto = p_id_producto
    GROUP BY p.id_producto, p.nombre, p.descripcion, p.precio_venta, c.nombre, p.activo;
    
    -- Lista de insumos de la receta
    SELECT * FROM V_Receta_Detalle
    WHERE id_producto = p_id_producto
    ORDER BY insumo;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Recetas_ObtenerTodos` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Recetas_ObtenerTodos`(
    IN p_search VARCHAR(100)
)
BEGIN
    IF p_search IS NOT NULL AND p_search != '' THEN
        SELECT * FROM V_Recetas_Listado
        WHERE producto LIKE CONCAT('%', p_search, '%')
        OR categoria LIKE CONCAT('%', p_search, '%')
        ORDER BY producto;
    ELSE
        SELECT * FROM V_Recetas_Listado ORDER BY producto;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Recetas_Verificar` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Recetas_Verificar`(
    IN p_id_producto INT,
    OUT p_tiene_receta BOOLEAN
)
BEGIN
    SELECT COUNT(*) > 0 INTO p_tiene_receta
    FROM recetas
    WHERE id_producto = p_id_producto;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_registrar_compra` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_registrar_compra`(
    IN p_id_proveedor INT,
    IN p_id_usuario INT,
    IN p_detalles JSON
)
BEGIN

    DECLARE v_id_compra INT;
    DECLARE v_total DECIMAL(10,2) DEFAULT 0;

    DECLARE i INT DEFAULT 0;
    DECLARE n INT;

    DECLARE v_id_insumo INT;
    DECLARE v_cantidad DECIMAL(10,4);
    DECLARE v_id_unidad INT;
    DECLARE v_costo DECIMAL(10,2);
    DECLARE v_caducidad DATE;

    DECLARE v_equivalente DECIMAL(12,4);
    DECLARE v_cantidad_base DECIMAL(12,4);
    DECLARE v_costo_unitario_base DECIMAL(12,4);

    DECLARE v_id_detalle INT;
    DECLARE v_id_lote INT;

    DECLARE v_stock_anterior DECIMAL(12,4);
    DECLARE v_stock_nuevo DECIMAL(12,4);

    DECLARE v_unidad_base INT;
    DECLARE v_msg TEXT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- 1. CREAR COMPRA
    INSERT INTO compras (id_proveedor, id_usuario)
    VALUES (p_id_proveedor, p_id_usuario);

    SET v_id_compra = LAST_INSERT_ID();

    SET n = JSON_LENGTH(p_detalles);

    WHILE i < n DO

        -- 2. EXTRAER JSON
        SET v_id_insumo = CAST(JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[',i,'].id_insumo'))) AS UNSIGNED);

        SET v_cantidad = CAST(JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[',i,'].cantidad'))) AS DECIMAL(10,4));

        SET v_id_unidad = CAST(JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[',i,'].id_unidad'))) AS UNSIGNED);

        SET v_costo = CAST(JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[',i,'].costo'))) AS DECIMAL(10,2));

        SET v_caducidad = STR_TO_DATE(
            JSON_UNQUOTE(JSON_EXTRACT(p_detalles, CONCAT('$[',i,'].caducidad'))),
            '%Y-%m-%d'
        );

        -- 3. UNIDAD BASE
        SELECT id_unidad_medida
        INTO v_unidad_base
        FROM insumos
        WHERE id_insumo = v_id_insumo;

        -- 4. STOCK ANTERIOR
        SELECT IFNULL(SUM(cantidad_disponible),0)
        INTO v_stock_anterior
        FROM lotes_insumo
        WHERE id_insumo = v_id_insumo;

        -- 5. CONVERSIÓN
        SET v_equivalente = NULL;

        IF v_id_unidad = v_unidad_base THEN
            SET v_equivalente = 1;
        ELSE
            SELECT cantidad_equivalente_base
            INTO v_equivalente
            FROM conversion_unidades_insumo
            WHERE id_insumo = v_id_insumo
            AND id_unidad_compra = v_id_unidad;
        END IF;

        -- VALIDACIÓN
        IF v_equivalente IS NULL THEN
            SET v_msg = CONCAT('No existe conversión para insumo ID: ', v_id_insumo);
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = v_msg;
        END IF;

        -- 6. CÁLCULOS BASE
        SET v_cantidad_base = v_cantidad * v_equivalente;
        SET v_costo_unitario_base = v_costo / v_equivalente;

        -- 7. DETALLE COMPRA
        INSERT INTO detalle_compras (
            id_compra, id_insumo, cantidad_comprada,
            id_unidad_medida, costo_unitario,
            cantidad_base, costo_unitario_base
        )
        VALUES (
            v_id_compra, v_id_insumo, v_cantidad,
            v_id_unidad, v_costo,
            v_cantidad_base, v_costo_unitario_base
        );

        SET v_id_detalle = LAST_INSERT_ID();

        -- 8. LOTE
        INSERT INTO lotes_insumo (
            id_insumo,
            id_detalle_compra,
            cantidad_inicial,
            cantidad_disponible,
            fecha_caducidad
        )
        VALUES (
            v_id_insumo,
            v_id_detalle,
            v_cantidad_base,
            v_cantidad_base,
            v_caducidad
        );

        SET v_id_lote = LAST_INSERT_ID();

        -- 9. INVENTARIO
        INSERT INTO inventario_insumos (id_lote)
        VALUES (v_id_lote);

        -- 10. STOCK NUEVO
        SET v_stock_nuevo = v_stock_anterior + v_cantidad_base;

        -- 11. MOVIMIENTO
        INSERT INTO movimientos_inventario_insumos (
            id_insumo,
            tipo_movimiento,
            cantidad,
            stock_anterior,
            stock_nuevo,
            referencia_tabla,
            referencia_id,
            id_usuario,
            id_lote
        )
        VALUES (
            v_id_insumo,
            'ENTRADA_COMPRA',
            v_cantidad_base,
            v_stock_anterior,
            v_stock_nuevo,
            'compras',
            v_id_compra,
            p_id_usuario,
            v_id_lote
        );

        --  12. ACUMULAR TOTAL (CORREGIDO)
        SET v_total = v_total + (v_cantidad * v_costo);

        SET i = i + 1;

    END WHILE;

    --  13. COSTO PROMEDIO (UNA SOLA VEZ)
    UPDATE insumos i
    SET costo_unitario = (
        SELECT 
            SUM(dc.cantidad_base * dc.costo_unitario_base) /
            NULLIF(SUM(dc.cantidad_base), 0)
        FROM detalle_compras dc
        WHERE dc.id_insumo = i.id_insumo
    )
    WHERE i.id_insumo IN (
        SELECT DISTINCT id_insumo 
        FROM detalle_compras 
        WHERE id_compra = v_id_compra
    );

    -- 14. TOTAL COMPRA
    UPDATE compras
    SET total = v_total
    WHERE id_compra = v_id_compra;

    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_registrar_merma` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_registrar_merma`(
    IN p_id_insumo INT,
    IN p_id_lote INT,
    IN p_cantidad DECIMAL(10,4),
    IN p_motivo VARCHAR(255),
    IN p_id_usuario INT
)
BEGIN

    DECLARE v_stock_anterior DECIMAL(12,4);
    DECLARE v_stock_nuevo DECIMAL(12,4);
    DECLARE v_disponible DECIMAL(12,4);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    -- 1. VALIDAR DISPONIBLE EN LOTE
    SELECT cantidad_disponible
    INTO v_disponible
    FROM lotes_insumo
    WHERE id_lote = p_id_lote;

    IF v_disponible IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El lote no existe';
    END IF;

    IF p_cantidad > v_disponible THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No hay suficiente stock en el lote';
    END IF;

    -- 2. STOCK ANTES
    SELECT IFNULL(SUM(cantidad_disponible),0)
    INTO v_stock_anterior
    FROM lotes_insumo
    WHERE id_insumo = p_id_insumo;

    -- 3. ACTUALIZAR LOTE
    UPDATE lotes_insumo
    SET cantidad_disponible = cantidad_disponible - p_cantidad
    WHERE id_lote = p_id_lote;

    -- 4. STOCK NUEVO
    SET v_stock_nuevo = v_stock_anterior - p_cantidad;

    -- 5. REGISTRAR MERMA
    INSERT INTO mermas_log (
        id_insumo,
        cantidad,
        motivo,
        id_usuario,
        id_lote
    )
    VALUES (
        p_id_insumo,
        p_cantidad,
        p_motivo,
        p_id_usuario,
        p_id_lote
    );

    -- 6. MOVIMIENTO
    INSERT INTO movimientos_inventario_insumos (
        id_insumo,
        tipo_movimiento,
        cantidad,
        stock_anterior,
        stock_nuevo,
        referencia_tabla,
        referencia_id,
        motivo,
        id_usuario,
        id_lote
    )
    VALUES (
        p_id_insumo,
        'SALIDA_MERMA',
        p_cantidad,
        v_stock_anterior,
        v_stock_nuevo,
        'mermas_log',
        LAST_INSERT_ID(),
        p_motivo,
        p_id_usuario,
        p_id_lote
    );

    COMMIT;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_registrar_salida_efectivo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_registrar_salida_efectivo`(
    IN p_id_usuario INT, 
    IN p_monto DECIMAL(10,2), 
    IN p_motivo VARCHAR(255)
)
BEGIN
    DECLARE v_id_caja INT;
    DECLARE v_saldo_anterior DECIMAL(12,2) DEFAULT 0;
    DECLARE v_saldo_nuevo DECIMAL(12,2) DEFAULT 0;
    
    -- 1. Validar desde BD que el monto sea positivo (doble seguridad)
    IF p_monto <= 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'El monto de la salida debe ser mayor a cero.';
    END IF;

    -- 2. Buscar la caja activa actual
    SELECT id_caja, saldo_actual INTO v_id_caja, v_saldo_anterior
    FROM caja
    WHERE activa = 1
    LIMIT 1;
    
    -- 3. Validar que exista una caja activa
    IF v_id_caja IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'No hay ninguna caja activa configurada en el sistema.';
    END IF;
    
    -- 4. Validar que la caja tenga fondos suficientes para la salida
    IF v_saldo_anterior < p_monto THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Fondos insuficientes. No hay suficiente efectivo en caja para este retiro.';
    END IF;

    -- 5. Calcular el nuevo saldo
    SET v_saldo_nuevo = v_saldo_anterior - p_monto;

    -- 6. Insertar en la tabla específica de salidas_efectivo
    INSERT INTO salidas_efectivo (id_usuario, monto, motivo, fecha_salida)
    VALUES (p_id_usuario, p_monto, p_motivo, NOW());

    -- 7. Insertar el rastro contable en movimientos_caja
    INSERT INTO movimientos_caja (
        id_caja, id_usuario, tipo_movimiento, monto, 
        saldo_anterior, saldo_nuevo, referencia, fecha_movimiento
    ) VALUES (
        v_id_caja, p_id_usuario, 'SALIDA_GASTO', p_monto, 
        v_saldo_anterior, v_saldo_nuevo, CONCAT('Salida: ', p_motivo), NOW()
    );

    -- 8. Actualizar físicamente el saldo de la caja
    UPDATE caja 
    SET saldo_actual = v_saldo_nuevo 
    WHERE id_caja = v_id_caja;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_registrar_solicitud_produccion` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_registrar_solicitud_produccion`(
    IN p_id_usuario INT,
    IN p_id_producto INT,
    IN p_cantidad INT
)
BEGIN
    DECLARE v_existe_producto INT DEFAULT 0;

    -- 1. Validar que la cantidad sea coherente (Evita números negativos por manipulación)
    IF p_cantidad <= 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'La cantidad a solicitar debe ser mayor a cero.';
    END IF;

    -- 2. VALIDACIÓN DE SEGURIDAD: Comprobar que el producto realmente exista y esté activo
    SELECT COUNT(*) INTO v_existe_producto
    FROM productos
    WHERE id_producto = p_id_producto AND activo = 1;

    IF v_existe_producto = 0 THEN
        -- Si llega aquí, significa que alguien alteró el HTML y mandó un ID inválido
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Error de validación: El producto seleccionado no es válido o está inactivo.';
    END IF;

    -- 3. Si pasa las auditorías, insertamos la solicitud
    INSERT INTO solicitudes_produccion (
        id_usuario_solicita, id_producto, cantidad, estado, fecha_solicitud
    ) VALUES (
        p_id_usuario, p_id_producto, p_cantidad, 'Pendiente', NOW()
    );

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_resumen_corte_caja` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_resumen_corte_caja`(IN p_fecha DATE, IN p_id_usuario INT)
BEGIN
    -- Result Set 1: Resumen de Totales por Cajero (Lee de la Vista)
    SELECT 
        COUNT(id_venta) AS total_ventas,
        COALESCE(SUM(CASE WHEN metodo = 'Efectivo' THEN total ELSE 0 END), 0) AS total_efectivo,
        COALESCE(SUM(CASE WHEN metodo = 'Tarjeta' THEN total ELSE 0 END), 0) AS total_tarjeta,
        COALESCE(SUM(CASE WHEN metodo = 'Tarjeta' THEN 1 ELSE 0 END), 0) AS transacciones_tarjeta,
        COALESCE(SUM(total), 0) AS total_ingresos
    FROM v_ventas_pagadas
    WHERE fecha_corte = p_fecha AND id_usuario = p_id_usuario;

    -- Result Set 2: Detalle de las ventas por Cajero (Lee de la Vista)
    SELECT 
        id_venta AS venta,
        fecha_hora,
        metodo,
        total
    FROM v_ventas_pagadas
    WHERE fecha_corte = p_fecha AND id_usuario = p_id_usuario
    ORDER BY fecha_hora DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_stock_salida_combo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_stock_salida_combo`(
    IN p_id_combo INT,
    IN p_cantidad_combo INT,
    IN p_id_usuario INT,
    IN p_id_venta INT
)
BEGIN
    DECLARE v_done INT DEFAULT 0;
    DECLARE v_id_hijo INT;
    DECLARE v_cantidad_hijo INT;

    DECLARE cur_combo CURSOR FOR
        SELECT id_producto_hijo, cantidad
        FROM combos
        WHERE id_producto_padre = p_id_combo;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;

    OPEN cur_combo;

    combo_loop: LOOP
        FETCH cur_combo INTO v_id_hijo, v_cantidad_hijo;

        IF v_done = 1 THEN
            LEAVE combo_loop;
        END IF;

        CALL sp_stock_salida_producto(
            v_id_hijo,
            v_cantidad_hijo * p_cantidad_combo,
            p_id_usuario,
            p_id_venta,
            'SALIDA_COMBO',
            CONCAT('Salida por combo ', p_id_combo)
        );
    END LOOP;

    CLOSE cur_combo;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_stock_salida_producto` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_stock_salida_producto`(
    IN p_id_producto INT,
    IN p_cantidad INT,
    IN p_id_usuario INT,
    IN p_id_venta INT,
    IN p_tipo_movimiento VARCHAR(20),
    IN p_motivo VARCHAR(255)
)
BEGIN
    DECLARE v_stock_actual INT;
    DECLARE v_stock_nuevo INT;

    SELECT stock_actual
    INTO v_stock_actual
    FROM inventario_productos
    WHERE id_producto = p_id_producto
    FOR UPDATE;

    IF v_stock_actual IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El producto no tiene inventario registrado.';
    END IF;

    IF v_stock_actual < p_cantidad THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Inventario insuficiente para completar la venta.';
    END IF;

    SET v_stock_nuevo = v_stock_actual - p_cantidad;

    UPDATE inventario_productos
    SET stock_actual = v_stock_nuevo
    WHERE id_producto = p_id_producto;

    INSERT INTO movimientos_inventario_productos (
        id_producto,
        tipo_movimiento,
        cantidad,
        stock_anterior,
        stock_nuevo,
        referencia_tabla,
        referencia_id,
        motivo,
        id_usuario
    )
    VALUES (
        p_id_producto,
        p_tipo_movimiento,
        p_cantidad,
        v_stock_actual,
        v_stock_nuevo,
        'ventas',
        p_id_venta,
        p_motivo,
        p_id_usuario
    );
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `SP_Toggle_Estado_Usuario` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `SP_Toggle_Estado_Usuario`(
    IN p_id_usuario INT
)
BEGIN
    -- Cambia el estado al contrario del que tiene actualmente
    UPDATE usuarios 
    SET active = NOT active 
    WHERE id_usuario = p_id_usuario;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_venta_completar` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`Gerente`@`localhost` PROCEDURE `sp_venta_completar`(
    IN p_id_usuario INT,
    IN p_id_metodo_pago INT,
    IN p_num_cuenta VARCHAR(20),
    IN p_monto_recibido DECIMAL(10,2)
)
BEGIN
    -- Variables generales de la venta
    DECLARE v_id_borrador BIGINT;
    DECLARE v_subtotal DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_descuento DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_total DECIMAL(10,2) DEFAULT 0.00;
    DECLARE v_metodo_nombre VARCHAR(30);
    DECLARE v_id_venta INT;
    
    -- Variables para pagos
    DECLARE v_id_cuenta INT;
    DECLARE v_saldo_anterior DECIMAL(12,2);
    DECLARE v_saldo_nuevo DECIMAL(12,2);
    DECLARE v_id_caja INT;
    DECLARE v_saldo_caja_anterior DECIMAL(12,2);
    DECLARE v_saldo_caja_nuevo DECIMAL(12,2);
    DECLARE v_cambio DECIMAL(10,2) DEFAULT 0.00;

    -- Manejador de Errores: Cierra el "paraguas" si algo falla
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- ==========================================
    -- 1. BUSCAR CARRITO ACTIVO
    -- ==========================================
    SET v_id_borrador = (
        SELECT id_venta_borrador
        FROM ventas_borrador
        WHERE id_usuario = p_id_usuario
          AND estado = 'ABIERTA'
        LIMIT 1
    );

    IF v_id_borrador IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No existe una venta en preparación.';
    END IF;

    -- ==========================================
    -- 2. CÁLCULO DE TOTALES
    -- ==========================================
    SELECT
        COALESCE(SUM(cantidad * precio_unitario), 0.00),
        COALESCE(SUM(cantidad * descuento_unitario), 0.00)
    INTO v_subtotal, v_descuento
    FROM detalle_ventas_borrador
    WHERE id_venta_borrador = v_id_borrador;

    SET v_descuento = v_descuento + COALESCE((
        SELECT descuento_global FROM ventas_borrador WHERE id_venta_borrador = v_id_borrador LIMIT 1
    ), 0.00);

    SET v_total = v_subtotal - v_descuento;

    IF v_subtotal <= 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El carrito está vacío.'; END IF;
    IF v_total < 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El total calculado es inválido.'; END IF;

    -- ==========================================
    -- 3. LÓGICA DE PAGOS (Tarjeta o Efectivo)
    -- ==========================================
    SET v_metodo_nombre = (SELECT nombre FROM metodos_pago WHERE id_metodo_pago = p_id_metodo_pago LIMIT 1);
    IF v_metodo_nombre IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Método de pago inválido.'; END IF;

    IF LOWER(v_metodo_nombre) = 'tarjeta' THEN
        IF p_num_cuenta IS NULL OR TRIM(p_num_cuenta) = '' THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Debe capturar el número de cuenta.';
        END IF;

        SET v_id_cuenta = (SELECT id_cuenta FROM cuenta WHERE num_cuenta = p_num_cuenta AND activo = 1 LIMIT 1);
        IF v_id_cuenta IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Pago rechazado: cuenta inválida o inactiva.'; END IF;

        SELECT saldo INTO v_saldo_anterior FROM cuenta WHERE id_cuenta = v_id_cuenta FOR UPDATE;
        IF v_saldo_anterior < v_total THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Pago rechazado: saldo insuficiente.'; END IF;
        
        SET v_saldo_nuevo = v_saldo_anterior - v_total;
    END IF;

    IF LOWER(v_metodo_nombre) = 'efectivo' THEN
        IF p_monto_recibido IS NULL OR p_monto_recibido <= 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Debe capturar el monto recibido.'; END IF;
        IF p_monto_recibido < v_total THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El monto recibido es menor al total de la venta.'; END IF;

        SET v_cambio = p_monto_recibido - v_total;
        SET v_id_caja = (SELECT id_caja FROM caja WHERE activa = 1 LIMIT 1);
        IF v_id_caja IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No hay una caja activa configurada.'; END IF;

        SELECT saldo_actual INTO v_saldo_caja_anterior FROM caja WHERE id_caja = v_id_caja FOR UPDATE;
        SET v_saldo_caja_nuevo = v_saldo_caja_anterior + p_monto_recibido - v_cambio;

        IF v_saldo_caja_nuevo < 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La caja no tiene saldo suficiente para entregar el cambio.'; END IF;
    END IF;

    -- ==========================================
    -- 4. INSERTAR VENTA Y DETALLES OFICIALES
    -- ==========================================
    INSERT INTO ventas (id_usuario, total, id_metodo_pago, referencia_pago, estado_venta, monto_recibido, cambio)
    VALUES (
        p_id_usuario, v_total, p_id_metodo_pago, 
        CASE WHEN LOWER(v_metodo_nombre) = 'tarjeta' THEN p_num_cuenta ELSE 'EFECTIVO' END,
        'Pagado',
        CASE WHEN LOWER(v_metodo_nombre) = 'efectivo' THEN p_monto_recibido ELSE NULL END,
        v_cambio
    );
    SET v_id_venta = LAST_INSERT_ID();

    -- Copiamos el id_combo y el id_producto tal como vengan del carrito
    INSERT INTO detalle_ventas (id_venta, id_producto, id_combo, cantidad, precio_unitario)
    SELECT v_id_venta, id_producto, id_combo, cantidad, precio_unitario
    FROM detalle_ventas_borrador
    WHERE id_venta_borrador = v_id_borrador;

    -- ==========================================
    -- 5. REGISTROS CONTABLES Y LIMPIEZA
    -- ==========================================
    IF LOWER(v_metodo_nombre) = 'tarjeta' THEN
        UPDATE cuenta SET saldo = v_saldo_nuevo WHERE id_cuenta = v_id_cuenta;
        INSERT INTO movimientos_cuenta (id_cuenta, id_venta, tipo_movimiento, monto, saldo_anterior, saldo_nuevo, referencia)
        VALUES (v_id_cuenta, v_id_venta, 'CARGO', v_total, v_saldo_anterior, v_saldo_nuevo, CONCAT('Venta #', v_id_venta));
    END IF;

    IF LOWER(v_metodo_nombre) = 'efectivo' THEN
        UPDATE caja SET saldo_actual = v_saldo_caja_nuevo WHERE id_caja = v_id_caja;
        
        INSERT INTO movimientos_caja (id_caja, id_venta, id_usuario, tipo_movimiento, monto, saldo_anterior, saldo_nuevo, referencia)
        VALUES (v_id_caja, v_id_venta, p_id_usuario, 'ENTRADA_VENTA', p_monto_recibido, v_saldo_caja_anterior, v_saldo_caja_anterior + p_monto_recibido, CONCAT('Pago recibido venta #', v_id_venta));

        IF v_cambio > 0 THEN
            INSERT INTO movimientos_caja (id_caja, id_venta, id_usuario, tipo_movimiento, monto, saldo_anterior, saldo_nuevo, referencia)
            VALUES (v_id_caja, v_id_venta, p_id_usuario, 'SALIDA_CAMBIO', v_cambio, v_saldo_caja_anterior + p_monto_recibido, v_saldo_caja_nuevo, CONCAT('Cambio entregado venta #', v_id_venta));
        END IF;
    END IF;

    INSERT INTO tickets (id_venta, folio, monto_pagado)
    VALUES (
        v_id_venta,
        CONCAT('TKT-', LPAD(v_id_venta, 8, '0')),
        CASE WHEN LOWER(v_metodo_nombre) = 'efectivo' THEN p_monto_recibido ELSE v_total END
    );

    DELETE FROM detalle_ventas_borrador WHERE id_venta_borrador = v_id_borrador;
    UPDATE ventas_borrador SET estado = 'PROCESADA' WHERE id_venta_borrador = v_id_borrador;

    -- Se retorna a Flask para imprimir el ticket (AQUÍ ESTÁ LA SOLUCIÓN DEFINITIVA)
    SELECT v_id_venta AS id_nueva_venta;

    COMMIT;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `v_historial_compras`
--

/*!50001 DROP VIEW IF EXISTS `v_historial_compras`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_historial_compras` AS select `c`.`id_compra` AS `id_compra`,`c`.`fecha_compra` AS `fecha_compra`,`c`.`estado_compra` AS `estado_compra`,`c`.`total` AS `total`,`dc`.`id_detalle_compra` AS `id_detalle_compra`,`dc`.`cantidad_comprada` AS `cantidad_comprada`,`dc`.`costo_unitario` AS `costo_unitario`,`dc`.`costo_subtotal` AS `costo_subtotal`,`i`.`nombre` AS `insumo`,`um`.`nombre` AS `unidad`,`u`.`id_usuario` AS `id_usuario` from ((((`compras` `c` join `detalle_compras` `dc` on((`dc`.`id_compra` = `c`.`id_compra`))) join `insumos` `i` on((`i`.`id_insumo` = `dc`.`id_insumo`))) join `unidades_medida` `um` on((`um`.`id_unidad_medida` = `dc`.`id_unidad_medida`))) join `usuarios` `u` on((`u`.`id_usuario` = `c`.`id_usuario`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_insumos_completo`
--

/*!50001 DROP VIEW IF EXISTS `v_insumos_completo`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_insumos_completo` AS select `i`.`id_insumo` AS `id_insumo`,`i`.`nombre` AS `nombre`,`i`.`costo_unitario` AS `costo_unitario`,`i`.`porcentaje_merma` AS `merma_teorica`,ifnull(sum(`l`.`cantidad_disponible`),0) AS `stock_actual`,ifnull(sum(`l`.`cantidad_inicial`),0) AS `total_comprado`,ifnull(sum(`m`.`cantidad`),0) AS `total_merma`,(case when (sum(`l`.`cantidad_inicial`) > 0) then ((ifnull(sum(`m`.`cantidad`),0) / sum(`l`.`cantidad_inicial`)) * 100) else 0 end) AS `merma_real` from ((`insumos` `i` left join `lotes_insumo` `l` on((`i`.`id_insumo` = `l`.`id_insumo`))) left join `mermas_log` `m` on((`i`.`id_insumo` = `m`.`id_insumo`))) group by `i`.`id_insumo` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_merma_por_mes`
--

/*!50001 DROP VIEW IF EXISTS `v_merma_por_mes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_merma_por_mes` AS select `i`.`id_insumo` AS `id_insumo`,`i`.`nombre` AS `nombre`,date_format(`c`.`fecha_compra`,'%Y-%m') AS `periodo`,sum(`dc`.`cantidad_comprada`) AS `total_comprado`,sum((`dc`.`cantidad_comprada` * (`i`.`porcentaje_merma` / 100))) AS `merma_teorica`,ifnull(sum(`m`.`cantidad`),0) AS `merma_real` from (((`insumos` `i` join `detalle_compras` `dc` on((`i`.`id_insumo` = `dc`.`id_insumo`))) join `compras` `c` on((`dc`.`id_compra` = `c`.`id_compra`))) left join `mermas_log` `m` on(((`i`.`id_insumo` = `m`.`id_insumo`) and (date_format(`m`.`fecha_baja`,'%Y-%m') = date_format(`c`.`fecha_compra`,'%Y-%m'))))) group by `i`.`id_insumo`,`periodo` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_mermas_detallado`
--

/*!50001 DROP VIEW IF EXISTS `v_mermas_detallado`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_mermas_detallado` AS select `m`.`id_merma` AS `id_merma`,cast(`m`.`fecha_baja` as date) AS `fecha`,cast(`m`.`fecha_baja` as time) AS `hora`,`i`.`nombre` AS `insumo`,`m`.`cantidad` AS `cantidad`,`m`.`motivo` AS `motivo`,`l`.`id_lote` AS `id_lote`,`l`.`fecha_caducidad` AS `fecha_caducidad`,`u`.`id_usuario` AS `id_usuario` from (((`mermas_log` `m` join `insumos` `i` on((`i`.`id_insumo` = `m`.`id_insumo`))) left join `lotes_insumo` `l` on((`l`.`id_lote` = `m`.`id_lote`))) join `usuarios` `u` on((`u`.`id_usuario` = `m`.`id_usuario`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_ordenesproduccion`
--

/*!50001 DROP VIEW IF EXISTS `v_ordenesproduccion`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_ordenesproduccion` AS select `op`.`id_orden_produccion` AS `id_orden_produccion`,`op`.`id_producto` AS `id_producto`,`p`.`nombre` AS `producto`,`p`.`precio_venta` AS `precio_venta`,`op`.`cantidad_programada` AS `cantidad_programada`,`op`.`cantidad_producida` AS `cantidad_producida`,`op`.`estado` AS `estado`,`op`.`fecha_creacion` AS `fecha_creacion`,`op`.`fecha_inicio` AS `fecha_inicio`,`op`.`fecha_finalizacion` AS `fecha_finalizacion`,`op`.`observaciones` AS `observaciones`,`u1`.`email` AS `creado_por`,`u2`.`email` AS `responsable`,(case when exists(select 1 from `recetas` `r` where ((`r`.`id_producto` = `op`.`id_producto`) and ((select coalesce(sum(`li`.`cantidad_disponible`),0) from `lotes_insumo` `li` where (`li`.`id_insumo` = `r`.`id_insumo`)) < (`r`.`cantidad_requerida` * `op`.`cantidad_programada`)))) then 'Stock Insuficiente' else 'Stock OK' end) AS `validacion_stock` from (((`ordenes_produccion` `op` join `productos` `p` on((`op`.`id_producto` = `p`.`id_producto`))) left join `usuarios` `u1` on((`op`.`id_usuario_crea` = `u1`.`id_usuario`))) left join `usuarios` `u2` on((`op`.`id_usuario_responsable` = `u2`.`id_usuario`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_receta_detalle`
--

/*!50001 DROP VIEW IF EXISTS `v_receta_detalle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_receta_detalle` AS select `p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `producto`,`p`.`descripcion` AS `descripcion`,`p`.`precio_venta` AS `precio_venta`,`p`.`activo` AS `producto_activo`,`c`.`id_categoria` AS `id_categoria`,`c`.`nombre` AS `categoria`,`i`.`id_insumo` AS `id_insumo`,`i`.`nombre` AS `insumo`,`um`.`id_unidad_medida` AS `id_unidad_medida`,`um`.`nombre` AS `unidad_medida`,`um`.`abreviatura` AS `abreviatura`,`r`.`cantidad_requerida` AS `cantidad_requerida`,`i`.`costo_unitario` AS `costo_unitario`,round((`r`.`cantidad_requerida` * `i`.`costo_unitario`),2) AS `costo_parcial`,`i`.`porcentaje_merma` AS `porcentaje_merma`,`i`.`activo` AS `insumo_activo` from ((((`recetas` `r` join `productos` `p` on((`r`.`id_producto` = `p`.`id_producto`))) join `categorias` `c` on((`p`.`id_categoria` = `c`.`id_categoria`))) join `insumos` `i` on((`r`.`id_insumo` = `i`.`id_insumo`))) join `unidades_medida` `um` on((`i`.`id_unidad_medida` = `um`.`id_unidad_medida`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_recetas_listado`
--

/*!50001 DROP VIEW IF EXISTS `v_recetas_listado`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_recetas_listado` AS select `p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `producto`,`c`.`nombre` AS `categoria`,`p`.`imagen` AS `imagen`,`p`.`descripcion` AS `descripcion`,`p`.`precio_venta` AS `precio_venta`,`p`.`activo` AS `activo`,count(`r`.`id_receta`) AS `total_insumos`,coalesce(sum((`r`.`cantidad_requerida` * `i`.`costo_unitario`)),0) AS `costo_produccion`,round((`p`.`precio_venta` - coalesce(sum((`r`.`cantidad_requerida` * `i`.`costo_unitario`)),0)),2) AS `utilidad`,(case when (count(`r`.`id_receta`) = 0) then 'Sin receta' else 'Completa' end) AS `estado_receta` from (((`productos` `p` left join `categorias` `c` on((`p`.`id_categoria` = `c`.`id_categoria`))) left join `recetas` `r` on((`p`.`id_producto` = `r`.`id_producto`))) left join `insumos` `i` on((`r`.`id_insumo` = `i`.`id_insumo`))) group by `p`.`id_producto`,`p`.`nombre`,`c`.`nombre`,`p`.`descripcion`,`p`.`precio_venta`,`p`.`activo`,`p`.`imagen` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_usuarios_detalle`
--

/*!50001 DROP VIEW IF EXISTS `v_usuarios_detalle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_usuarios_detalle` AS select `u`.`id_usuario` AS `id_usuario`,`u`.`email` AS `email`,`u`.`active` AS `active`,`u`.`fecha_registro` AS `fecha_registro`,`u`.`intentos_fallidos` AS `intentos_fallidos`,`p`.`id_persona` AS `id_persona`,`p`.`nombre` AS `nombre`,`p`.`apellido_pa` AS `apellido_pa`,`p`.`apellido_ma` AS `apellido_ma`,`p`.`fecha_nac` AS `fecha_nac`,`p`.`telefono` AS `telefono`,`r`.`id_rol` AS `id_rol`,`r`.`name` AS `nombre_rol` from (((`usuarios` `u` join `persona` `p` on((`u`.`id_persona` = `p`.`id_persona`))) left join `usuarios_roles` `ur` on((`u`.`id_usuario` = `ur`.`id_usuario`))) left join `roles` `r` on((`ur`.`id_rol` = `r`.`id_rol`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `v_ventas_pagadas`
--

/*!50001 DROP VIEW IF EXISTS `v_ventas_pagadas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `v_ventas_pagadas` AS select `v`.`id_venta` AS `id_venta`,`v`.`id_usuario` AS `id_usuario`,cast(`v`.`fecha_venta` as date) AS `fecha_corte`,`v`.`fecha_venta` AS `fecha_hora`,`v`.`total` AS `total`,`mp`.`nombre` AS `metodo` from (`ventas` `v` join `metodos_pago` `mp` on((`v`.`id_metodo_pago` = `mp`.`id_metodo_pago`))) where (`v`.`estado_venta` = 'Pagado') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_proveedores`
--

/*!50001 DROP VIEW IF EXISTS `vista_proveedores`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_proveedores` AS select `p`.`id_proveedor` AS `id_proveedor`,`p`.`nombre_empresa` AS `nombre_empresa`,`p`.`nombre_contacto` AS `nombre_contacto`,`p`.`apellido_pa` AS `apellido_pa`,`p`.`apellido_ma` AS `apellido_ma`,concat(`p`.`nombre_contacto`,' ',`p`.`apellido_pa`,ifnull(concat(' ',`p`.`apellido_ma`),'')) AS `contacto_completo`,`p`.`telefono` AS `telefono`,`p`.`email` AS `email`,`p`.`rfc` AS `rfc`,`p`.`direccion` AS `direccion`,`p`.`activo` AS `activo`,`p`.`id_categoria_proveedor` AS `id_categoria_proveedor`,`c`.`nombre` AS `nombre_categoria` from (`proveedores` `p` join `categorias_proveedor` `c` on((`p`.`id_categoria_proveedor` = `c`.`id_categoria_proveedor`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_carrito_detalle`
--

/*!50001 DROP VIEW IF EXISTS `vw_carrito_detalle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_carrito_detalle` AS select `vb`.`id_usuario` AS `id_usuario`,coalesce(`dvb`.`id_producto`,`dvb`.`id_combo`) AS `id_item`,coalesce(`p`.`nombre`,`cb`.`nombre`) AS `nombre`,(case when (`cb`.`id_combo` is not null) then 'Combos' else `c`.`nombre` end) AS `categoria`,(case when (`dvb`.`id_combo` is not null) then 'Combo' else 'Producto' end) AS `tipo_item`,`dvb`.`cantidad` AS `cantidad`,`dvb`.`precio_unitario` AS `precio_unitario`,`dvb`.`descuento_unitario` AS `descuento_unitario`,(`dvb`.`cantidad` * `dvb`.`precio_unitario`) AS `subtotal_linea`,(`dvb`.`cantidad` * `dvb`.`descuento_unitario`) AS `descuento_linea`,((`dvb`.`cantidad` * `dvb`.`precio_unitario`) - (`dvb`.`cantidad` * `dvb`.`descuento_unitario`)) AS `total_linea` from ((((`ventas_borrador` `vb` join `detalle_ventas_borrador` `dvb` on((`dvb`.`id_venta_borrador` = `vb`.`id_venta_borrador`))) left join `productos` `p` on((`p`.`id_producto` = `dvb`.`id_producto`))) left join `categorias` `c` on((`c`.`id_categoria` = `p`.`id_categoria`))) left join `combos` `cb` on((`cb`.`id_combo` = `dvb`.`id_combo`))) where (`vb`.`estado` = 'ABIERTA') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_carrito_resumen`
--

/*!50001 DROP VIEW IF EXISTS `vw_carrito_resumen`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_carrito_resumen` AS select `vb`.`id_usuario` AS `id_usuario`,coalesce(sum((`dvb`.`cantidad` * `dvb`.`precio_unitario`)),0.00) AS `subtotal`,(coalesce(sum((`dvb`.`cantidad` * `dvb`.`descuento_unitario`)),0.00) + coalesce(`vb`.`descuento_global`,0.00)) AS `descuento`,(coalesce(sum((`dvb`.`cantidad` * `dvb`.`precio_unitario`)),0.00) - (coalesce(sum((`dvb`.`cantidad` * `dvb`.`descuento_unitario`)),0.00) + coalesce(`vb`.`descuento_global`,0.00))) AS `total`,coalesce(sum(`dvb`.`cantidad`),0) AS `total_piezas`,count(`dvb`.`id_detalle_borrador`) AS `lineas` from (`ventas_borrador` `vb` left join `detalle_ventas_borrador` `dvb` on((`dvb`.`id_venta_borrador` = `vb`.`id_venta_borrador`))) where (`vb`.`estado` = 'ABIERTA') group by `vb`.`id_venta_borrador`,`vb`.`id_usuario`,`vb`.`descuento_global` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_costo_combos`
--

/*!50001 DROP VIEW IF EXISTS `vw_costo_combos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_costo_combos` AS select `c`.`id_combo` AS `id_combo`,`c`.`nombre` AS `nombre`,`c`.`precio_venta` AS `precio_venta`,`c`.`activo` AS `activo`,ifnull(sum((`dc`.`cantidad` * `cp`.`costo_produccion`)),0) AS `costo_produccion` from ((`combos` `c` left join `detalle_combos` `dc` on((`c`.`id_combo` = `dc`.`id_combo`))) left join `vw_costo_productos` `cp` on((`dc`.`id_producto` = `cp`.`id_producto`))) group by `c`.`id_combo`,`c`.`nombre`,`c`.`precio_venta`,`c`.`activo` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_costo_productos`
--

/*!50001 DROP VIEW IF EXISTS `vw_costo_productos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_costo_productos` AS select `p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `nombre`,`p`.`precio_venta` AS `precio_venta`,`p`.`activo` AS `activo`,ifnull(sum((`r`.`cantidad_requerida` * `i`.`costo_unitario`)),0) AS `costo_produccion` from ((`productos` `p` left join `recetas` `r` on((`p`.`id_producto` = `r`.`id_producto`))) left join `insumos` `i` on((`r`.`id_insumo` = `i`.`id_insumo`))) where (not((`p`.`nombre` like '%combo%'))) group by `p`.`id_producto`,`p`.`nombre`,`p`.`precio_venta`,`p`.`activo` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_costo_utilidad`
--

/*!50001 DROP VIEW IF EXISTS `vw_costo_utilidad`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_costo_utilidad` AS select `vw_costo_productos`.`id_producto` AS `id_producto`,`vw_costo_productos`.`nombre` AS `nombre`,'Producto' AS `tipo`,`vw_costo_productos`.`precio_venta` AS `precio_venta`,`vw_costo_productos`.`costo_produccion` AS `costo_produccion`,(`vw_costo_productos`.`precio_venta` - `vw_costo_productos`.`costo_produccion`) AS `utilidad`,(case when (`vw_costo_productos`.`precio_venta` > 0) then (((`vw_costo_productos`.`precio_venta` - `vw_costo_productos`.`costo_produccion`) / `vw_costo_productos`.`precio_venta`) * 100) else 0 end) AS `margen_ganancia` from `vw_costo_productos` where (`vw_costo_productos`.`activo` = 1) union all select `vw_costo_combos`.`id_combo` AS `id_producto`,`vw_costo_combos`.`nombre` AS `nombre`,'Combo' AS `tipo`,`vw_costo_combos`.`precio_venta` AS `precio_venta`,`vw_costo_combos`.`costo_produccion` AS `costo_produccion`,(`vw_costo_combos`.`precio_venta` - `vw_costo_combos`.`costo_produccion`) AS `utilidad`,(case when (`vw_costo_combos`.`precio_venta` > 0) then (((`vw_costo_combos`.`precio_venta` - `vw_costo_combos`.`costo_produccion`) / `vw_costo_combos`.`precio_venta`) * 100) else 0 end) AS `margen_ganancia` from `vw_costo_combos` where (`vw_costo_combos`.`activo` = 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_historial_caja`
--

/*!50001 DROP VIEW IF EXISTS `vw_historial_caja`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_historial_caja` AS select `mc`.`id_movimiento_caja` AS `id_movimiento_caja`,`mc`.`fecha_movimiento` AS `fecha_movimiento`,`mc`.`tipo_movimiento` AS `tipo_movimiento`,`mc`.`monto` AS `monto`,`mc`.`saldo_anterior` AS `saldo_anterior`,`mc`.`saldo_nuevo` AS `saldo_nuevo`,`mc`.`referencia` AS `referencia`,concat(`p`.`nombre`,' ',`p`.`apellido_pa`) AS `atendido_por`,`v`.`id_venta` AS `id_venta`,coalesce(`v`.`estado_venta`,'N/A') AS `estado_venta`,coalesce(`mp`.`nombre`,'N/A') AS `metodo_pago` from ((((`movimientos_caja` `mc` join `usuarios` `u` on((`mc`.`id_usuario` = `u`.`id_usuario`))) join `persona` `p` on((`u`.`id_persona` = `p`.`id_persona`))) left join `ventas` `v` on((`mc`.`id_venta` = `v`.`id_venta`))) left join `metodos_pago` `mp` on((`v`.`id_metodo_pago` = `mp`.`id_metodo_pago`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_inventario_productos`
--

/*!50001 DROP VIEW IF EXISTS `vw_inventario_productos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_inventario_productos` AS select `p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `nombre`,`p`.`precio_venta` AS `precio_venta`,`p`.`activo` AS `activo`,`ip`.`stock_actual` AS `stock_actual` from (`productos` `p` join `inventario_productos` `ip` on((`p`.`id_producto` = `ip`.`id_producto`))) where (not((`p`.`nombre` like '%combo%'))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_kds_cocina`
--

/*!50001 DROP VIEW IF EXISTS `vw_kds_cocina`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_kds_cocina` AS select `dv`.`id_detalle` AS `id_detalle`,`v`.`id_venta` AS `numero_orden`,`v`.`fecha_venta` AS `fecha_venta`,`dv`.`id_producto` AS `id_producto`,`p`.`nombre` AS `platillo`,`dv`.`cantidad` AS `cantidad`,`dv`.`estado_cocina` AS `estado_cocina`,`u`.`email` AS `cajero` from (((`detalle_ventas` `dv` join `ventas` `v` on((`dv`.`id_venta` = `v`.`id_venta`))) join `productos` `p` on((`dv`.`id_producto` = `p`.`id_producto`))) join `usuarios` `u` on((`v`.`id_usuario` = `u`.`id_usuario`))) where (`dv`.`estado_cocina` in ('Pendiente','Preparando')) order by `v`.`fecha_venta` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_kds_unificado`
--

/*!50001 DROP VIEW IF EXISTS `vw_kds_unificado`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_kds_unificado` AS select concat('V-',`dv`.`id_detalle`) AS `id_tarea`,`dv`.`id_detalle` AS `id_origen`,'Venta' AS `origen`,`v`.`id_venta` AS `folio`,`v`.`fecha_venta` AS `fecha_hora`,coalesce(`p`.`id_producto`,`cb`.`id_combo`) AS `id_producto`,coalesce(`p`.`nombre`,`cb`.`nombre`) AS `platillo`,`dv`.`cantidad` AS `cantidad`,`dv`.`estado_cocina` AS `estado`,concat(`pe`.`nombre`,' ',`pe`.`apellido_pa`) AS `solicitante` from (((((`detalle_ventas` `dv` join `ventas` `v` on((`dv`.`id_venta` = `v`.`id_venta`))) left join `productos` `p` on((`dv`.`id_producto` = `p`.`id_producto`))) left join `combos` `cb` on((`dv`.`id_combo` = `cb`.`id_combo`))) join `usuarios` `u` on((`v`.`id_usuario` = `u`.`id_usuario`))) join `persona` `pe` on((`u`.`id_persona` = `pe`.`id_persona`))) where (`dv`.`estado_cocina` in ('Pendiente','Preparando')) union all select concat('P-',`op`.`id_orden_produccion`) AS `id_tarea`,`op`.`id_orden_produccion` AS `id_origen`,'Producción' AS `origen`,`op`.`id_orden_produccion` AS `folio`,`op`.`fecha_creacion` AS `fecha_hora`,`p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `platillo`,`op`.`cantidad_programada` AS `cantidad`,`op`.`estado` AS `estado`,concat(`pe`.`nombre`,' ',`pe`.`apellido_pa`) AS `solicitante` from (((`ordenes_produccion` `op` join `productos` `p` on((`op`.`id_producto` = `p`.`id_producto`))) join `usuarios` `u` on((`op`.`id_usuario_crea` = `u`.`id_usuario`))) join `persona` `pe` on((`u`.`id_persona` = `pe`.`id_persona`))) where (`op`.`estado` in ('Pendiente','En Proceso')) order by `fecha_hora` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_productos_produccion`
--

/*!50001 DROP VIEW IF EXISTS `vw_productos_produccion`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_productos_produccion` AS select `p`.`id_producto` AS `id_producto`,`p`.`nombre` AS `nombre_producto`,`c`.`nombre` AS `categoria`,coalesce(`ip`.`stock_actual`,0) AS `stock_actual`,5 AS `stock_minimo` from ((`productos` `p` join `categorias` `c` on((`p`.`id_categoria` = `c`.`id_categoria`))) left join `inventario_productos` `ip` on((`p`.`id_producto` = `ip`.`id_producto`))) where (`p`.`activo` = 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_productos_ventas`
--

/*!50001 DROP VIEW IF EXISTS `vw_productos_ventas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_productos_ventas` AS with `insumos_reservados` as (select `r`.`id_insumo` AS `id_insumo`,sum((`dvb`.`cantidad` * `r`.`cantidad_requerida`)) AS `reservado` from ((`detalle_ventas_borrador` `dvb` join `ventas_borrador` `vb` on((`vb`.`id_venta_borrador` = `dvb`.`id_venta_borrador`))) join `recetas` `r` on((`r`.`id_producto` = `dvb`.`id_producto`))) where (`vb`.`estado` = 'ABIERTA') group by `r`.`id_insumo`), `stock_insumos` as (select `li`.`id_insumo` AS `id_insumo`,(sum(`li`.`cantidad_disponible`) - coalesce(`ir`.`reservado`,0)) AS `stock_real` from (`lotes_insumo` `li` left join `insumos_reservados` `ir` on((`ir`.`id_insumo` = `li`.`id_insumo`))) group by `li`.`id_insumo`) select `p`.`id_producto` AS `id_item`,`p`.`nombre` AS `nombre`,`c`.`nombre` AS `categoria`,`p`.`precio_venta` AS `precio_venta`,`p`.`activo` AS `activo`,`p`.`imagen` AS `imagen`,(greatest(coalesce((select min(floor((`si`.`stock_real` / nullif(`r`.`cantidad_requerida`,0)))) from (`recetas` `r` join `stock_insumos` `si` on((`si`.`id_insumo` = `r`.`id_insumo`))) where (`r`.`id_producto` = `p`.`id_producto`)),0),0) + coalesce((select sum(`ip`.`stock_actual`) from `inventario_productos` `ip` where (`ip`.`id_producto` = `p`.`id_producto`)),0)) AS `stock`,'Producto' AS `tipo_item` from (`productos` `p` join `categorias` `c` on((`c`.`id_categoria` = `p`.`id_categoria`))) union all select `cb`.`id_combo` AS `id_item`,`cb`.`nombre` AS `nombre`,'Combo' AS `categoria`,`cb`.`precio_venta` AS `precio_venta`,`cb`.`activo` AS `activo`,`cb`.`imagen` AS `imagen`,greatest(coalesce((select min(floor((`si`.`stock_real` / `t`.`total_requerido`))) from ((select `r`.`id_insumo` AS `id_insumo`,sum((`r`.`cantidad_requerida` * `dc`.`cantidad`)) AS `total_requerido` from (`detalle_combos` `dc` join `recetas` `r` on((`r`.`id_producto` = `dc`.`id_producto`))) where (`dc`.`id_combo` = `cb`.`id_combo`) group by `r`.`id_insumo`) `t` join `stock_insumos` `si` on((`si`.`id_insumo` = `t`.`id_insumo`)))),0),0) AS `stock`,'Combo' AS `tipo_item` from `combos` `cb` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_salidas_efectivo`
--

/*!50001 DROP VIEW IF EXISTS `vw_salidas_efectivo`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_salidas_efectivo` AS select `s`.`id_salida` AS `id`,`s`.`fecha_salida` AS `fecha_hora`,`s`.`monto` AS `monto`,`s`.`motivo` AS `motivo`,concat(`p`.`nombre`,' ',`p`.`apellido_pa`) AS `atendido_por` from ((`salidas_efectivo` `s` join `usuarios` `u` on((`s`.`id_usuario` = `u`.`id_usuario`))) join `persona` `p` on((`u`.`id_persona` = `p`.`id_persona`))) order by `s`.`fecha_salida` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_tablero_cocina`
--

/*!50001 DROP VIEW IF EXISTS `vw_tablero_cocina`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_tablero_cocina` AS select `sp`.`id_solicitud_prod` AS `id_solicitud_prod`,`sp`.`cantidad` AS `cantidad`,`sp`.`estado` AS `estado`,`sp`.`fecha_solicitud` AS `fecha_solicitud`,`p`.`nombre` AS `nombre_producto`,if(((select `r`.`name` from (`roles` `r` join `usuarios_roles` `ur` on((`r`.`id_rol` = `ur`.`id_rol`))) where (`ur`.`id_usuario` = `sp`.`id_usuario_solicita`) limit 1) in ('Cajero','Gerente')),'Local','En Línea') AS `tipo_orden` from (`solicitudes_produccion` `sp` join `productos` `p` on((`sp`.`id_producto` = `p`.`id_producto`))) where (`sp`.`estado` in ('Pendiente','En Proceso')) order by `sp`.`fecha_solicitud` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_ticket_cabecera`
--

/*!50001 DROP VIEW IF EXISTS `vw_ticket_cabecera`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_ticket_cabecera` AS select `t`.`id_venta` AS `id_venta`,`t`.`folio` AS `folio`,`t`.`fecha_emision` AS `fecha_emision`,`t`.`leyenda` AS `leyenda`,`v`.`total` AS `total`,`v`.`monto_recibido` AS `monto_recibido`,`v`.`cambio` AS `cambio`,`mp`.`nombre` AS `metodo_pago`,concat(`p`.`nombre`,' ',`p`.`apellido_pa`) AS `cajero` from ((((`tickets` `t` join `ventas` `v` on((`t`.`id_venta` = `v`.`id_venta`))) join `metodos_pago` `mp` on((`v`.`id_metodo_pago` = `mp`.`id_metodo_pago`))) join `usuarios` `u` on((`v`.`id_usuario` = `u`.`id_usuario`))) join `persona` `p` on((`u`.`id_persona` = `p`.`id_persona`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_ticket_detalle`
--

/*!50001 DROP VIEW IF EXISTS `vw_ticket_detalle`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_ticket_detalle` AS select `dv`.`id_venta` AS `id_venta`,`dv`.`id_producto` AS `id_producto`,`p`.`nombre` AS `producto`,(case when (`dv`.`id_combo` is not null) then 'Combo' else 'Producto' end) AS `tipo_item`,`dv`.`cantidad` AS `cantidad`,`dv`.`precio_unitario` AS `precio_unitario`,`dv`.`subtotal` AS `subtotal` from (`detalle_ventas` `dv` join `productos` `p` on((`p`.`id_producto` = `dv`.`id_producto`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_ticket_encabezado`
--

/*!50001 DROP VIEW IF EXISTS `vw_ticket_encabezado`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_ticket_encabezado` AS select `t`.`id_ticket` AS `id_ticket`,`t`.`id_venta` AS `id_venta`,`t`.`folio` AS `folio`,`t`.`fecha_emision` AS `fecha_emision`,concat(`pe`.`nombre`,' ',`pe`.`apellido_pa`,' ',`pe`.`apellido_ma`) AS `cajero`,`mp`.`nombre` AS `metodo_pago`,`v`.`total` AS `total`,`v`.`monto_recibido` AS `monto_recibido`,`v`.`cambio` AS `cambio`,`v`.`referencia_pago` AS `referencia_pago`,`t`.`monto_pagado` AS `monto_pagado`,`t`.`leyenda` AS `leyenda` from ((((`tickets` `t` join `ventas` `v` on((`v`.`id_venta` = `t`.`id_venta`))) join `usuarios` `u` on((`u`.`id_usuario` = `v`.`id_usuario`))) join `persona` `pe` on((`pe`.`id_persona` = `u`.`id_persona`))) join `metodos_pago` `mp` on((`mp`.`id_metodo_pago` = `v`.`id_metodo_pago`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_ticket_impresion`
--

/*!50001 DROP VIEW IF EXISTS `vw_ticket_impresion`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_ticket_impresion` AS select `te`.`id_ticket` AS `id_ticket`,`te`.`id_venta` AS `id_venta`,`te`.`folio` AS `folio`,`te`.`fecha_emision` AS `fecha_emision`,`te`.`cajero` AS `cajero`,`te`.`metodo_pago` AS `metodo_pago`,`te`.`total` AS `total`,`te`.`monto_recibido` AS `monto_recibido`,`te`.`cambio` AS `cambio`,`te`.`referencia_pago` AS `referencia_pago`,`te`.`monto_pagado` AS `monto_pagado`,`te`.`leyenda` AS `leyenda`,`td`.`id_producto` AS `id_producto`,`td`.`producto` AS `producto`,`td`.`tipo_item` AS `tipo_item`,`td`.`cantidad` AS `cantidad`,`td`.`precio_unitario` AS `precio_unitario`,`td`.`subtotal` AS `subtotal` from (`vw_ticket_encabezado` `te` join `vw_ticket_detalle` `td` on((`td`.`id_venta` = `te`.`id_venta`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_utilidad_diaria`
--

/*!50001 DROP VIEW IF EXISTS `vw_utilidad_diaria`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Gerente`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_utilidad_diaria` AS with `fechas` as (select distinct cast(`ventas`.`fecha_venta` as date) AS `fecha` from `ventas` where (`ventas`.`estado_venta` = 'Pagado') union select distinct cast(`salidas_efectivo`.`fecha_salida` as date) AS `DATE(fecha_salida)` from `salidas_efectivo`) select `f`.`fecha` AS `fecha`,coalesce((select count(`v`.`id_venta`) from `ventas` `v` where ((cast(`v`.`fecha_venta` as date) = `f`.`fecha`) and (`v`.`estado_venta` = 'Pagado'))),0) AS `transacciones_ventas`,coalesce((select sum(`v`.`total`) from `ventas` `v` where ((cast(`v`.`fecha_venta` as date) = `f`.`fecha`) and (`v`.`estado_venta` = 'Pagado'))),0) AS `total_ventas`,coalesce((select sum(((`dv`.`cantidad` * `r`.`cantidad_requerida`) * `i`.`costo_unitario`)) from (((`ventas` `v` join `detalle_ventas` `dv` on((`v`.`id_venta` = `dv`.`id_venta`))) join `recetas` `r` on((`dv`.`id_producto` = `r`.`id_producto`))) join `insumos` `i` on((`r`.`id_insumo` = `i`.`id_insumo`))) where ((cast(`v`.`fecha_venta` as date) = `f`.`fecha`) and (`v`.`estado_venta` = 'Pagado'))),0) AS `costo_produccion`,coalesce((select count(`s`.`id_salida`) from `salidas_efectivo` `s` where (cast(`s`.`fecha_salida` as date) = `f`.`fecha`)),0) AS `registros_salidas`,coalesce((select sum(`s`.`monto`) from `salidas_efectivo` `s` where (cast(`s`.`fecha_salida` as date) = `f`.`fecha`)),0) AS `total_salidas` from `fechas` `f` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-16 21:58:08
