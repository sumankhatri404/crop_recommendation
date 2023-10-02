-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 02, 2023 at 12:48 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `crops`
--

CREATE TABLE `crops` (
  `id` int(11) NOT NULL,
  `name` varchar(500) NOT NULL,
  `scientific_name` varchar(500) NOT NULL,
  `description` varchar(500) NOT NULL,
  `season` varchar(500) NOT NULL,
  `image_url` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `crops`
--

INSERT INTO `crops` (`id`, `name`, `scientific_name`, `description`, `season`, `image_url`) VALUES
(3, 'onioon', 'asdas', 'sasasa', 'September ', 'https://www.thespruceeats.com/thmb/s8HhkmVV57OfA7YcVUlKbKMyMJQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/high-angle-view-of-onions-in-basket-on-table-769799173-5be8e9b846e0fb00268a905f.jpg'),
(11, 'apple', 'Malus', 'Common Names: Names for this tree species include the apple, common apple, and paradise apple. The accepted scientific name is Malus pumila, but is also referred to as Malus domestica, Malus sylvestris, Malus communis, and Pyrus malus (ITIS website)', 'mid-July to December', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS22Jug4cEBCSiRBuseqni_Eet5psqRVIWGPA&usqp=CAU');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fname` varchar(200) NOT NULL,
  `lname` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fname`, `lname`, `email`, `password`) VALUES
(1, 'keshav', 'pandey', 'keshav@gmail.com', 'admin'),
(13, 'suman', 'khatri', 'suman@gmail.com', 'sha256$FRniXFpAGhodUkCw$bed50e8f5ff843e0e4a0bfac9f2efd90cc80e9f8f4bff62395b11098893b32ce');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `crops`
--
ALTER TABLE `crops`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `crops`
--
ALTER TABLE `crops`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
