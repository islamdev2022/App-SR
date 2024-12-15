-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2024 at 02:58 PM
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
-- Database: `app-sr`
--

-- --------------------------------------------------------

--
-- Table structure for table `actions_history`
--

CREATE TABLE `actions_history` (
  `id` int(11) NOT NULL,
  `username` varchar(40) NOT NULL,
  `role` varchar(40) NOT NULL,
  `action` varchar(255) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `actions_history`
--

INSERT INTO `actions_history` (`id`, `username`, `role`, `action`, `date`) VALUES
(1, 'manager', 'Admin', 'Login', '2024-12-13 23:01:55'),
(2, 'username', 'role', 'Logout', '2024-12-13 23:07:07'),
(8, 'mokhtarrida', 'Head', 'Login', '2024-12-13 23:20:14'),
(21, 'manager', 'Admin', 'Login', '2024-12-13 23:56:37'),
(22, 'manager', 'Admin', 'updated user teet', '2024-12-13 23:57:01'),
(23, 'manager', 'Admin', 'added task sdfsd', '2024-12-14 00:03:39'),
(24, 'manager', 'Admin', 'deleted task dqsd', '2024-12-14 00:06:16'),
(25, 'manager', 'Admin', 'added user new', '2024-12-14 00:10:22'),
(28, 'manager', 'Admin', 'Login', '2024-12-14 00:20:09'),
(29, 'manager', 'Admin', 'updated task sdfsd', '2024-12-14 00:20:23'),
(30, 'manager', 'Admin', 'Login', '2024-12-14 11:08:26'),
(31, 'manager', 'Admin', 'Logout', '2024-12-14 11:11:02'),
(33, 'mokhtarrida', 'Head Development', 'Login', '2024-12-14 11:20:25'),
(34, 'mokhtarrida', 'Head Development', 'assigned task important task to qsdqs qsdq', '2024-12-14 11:20:52'),
(37, 'mokhtarrida', 'Head Development', 'Login', '2024-12-14 11:35:25'),
(38, 'mokhtarrida', 'Head Development', 'assigned task sdfsd to birouk islam', '2024-12-14 11:36:35'),
(39, 'mokhtarrida', 'Head Development', 'Logout', '2024-12-14 11:36:55'),
(40, 'slamo', 'Member', 'Login', '2024-12-14 11:37:04'),
(41, 'slamo', 'member Development', 'updated task sdfsd status to In Progress', '2024-12-14 11:37:14'),
(42, 'slamo', 'member Development', 'Logout', '2024-12-14 11:40:38'),
(43, 'slamos', 'Admin', 'Login', '2024-12-14 11:59:56'),
(44, 'slamos', 'Admin', 'added user khmamoun', '2024-12-14 12:00:40'),
(45, 'slamos', 'Admin', 'added user walidos', '2024-12-14 12:01:48'),
(46, 'slamos', 'Admin', 'added user nisso', '2024-12-14 12:02:10'),
(47, 'slamos', 'Admin', 'added user minou', '2024-12-14 12:03:13'),
(49, 'slamos', 'Admin', 'added user yasg4mer', '2024-12-14 12:06:03'),
(50, 'slamos', 'Admin', 'added user bess', '2024-12-14 12:06:50'),
(51, 'slamos', 'Admin', 'added user chetiteb', '2024-12-14 12:08:44'),
(52, 'slamos', 'Admin', 'added user oussama', '2024-12-14 12:10:08'),
(53, 'slamos', 'Admin', 'Logout', '2024-12-14 12:14:07'),
(54, 'khmamoun', 'Head Data Analysis', 'Login', '2024-12-14 12:14:24'),
(55, 'khmamoun', 'Head Data Analysis', 'assigned task Data Cleaning to aymen boumezbeur', '2024-12-14 12:14:36'),
(56, 'khmamoun', 'Head Data Analysis', 'assigned task Sales Report Analysis to chettab mohcine', '2024-12-14 12:22:03'),
(57, 'khmamoun', 'Head Data Analysis', 'Logout', '2024-12-14 12:22:14'),
(58, 'tamime', 'Head Managemnt', 'Login', '2024-12-14 12:24:09'),
(59, 'tamime', 'Head Managemnt', 'assigned task Project Kickoff Meeting to yassine krika', '2024-12-14 12:24:19'),
(60, 'tamime', 'Head Managemnt', 'assigned task Team Performance Review to yassine krika', '2024-12-14 12:24:23'),
(61, 'tamime', 'Head Managemnt', 'Logout', '2024-12-14 12:24:36'),
(62, 'oussama', 'Member', 'Login', '2024-12-14 12:24:54'),
(63, 'oussama', 'member Marketing', 'Logout', '2024-12-14 12:27:02'),
(64, 'fateh', 'Head Marketing', 'Login', '2024-12-14 12:27:20'),
(65, 'fateh', 'Head Marketing', 'assigned task Social Media Campaign to bessam chamekh', '2024-12-14 12:27:30'),
(66, 'fateh', 'Head Marketing', 'assigned task Email Campaign to abdelmadjid belilet', '2024-12-14 12:27:38'),
(67, 'fateh', 'Head Marketing', 'Logout', '2024-12-14 12:28:17'),
(68, 'walidos', 'Head Design', 'Login', '2024-12-14 12:28:29'),
(69, 'walidos', 'Head Design', 'assigned task Create Landing page to anis zaimen', '2024-12-14 12:28:45'),
(70, 'walidos', 'Head Design', 'assigned task Logo Redesign to anis zaimen', '2024-12-14 12:28:48'),
(71, 'walidos', 'Head Design', 'Logout', '2024-12-14 12:29:47'),
(72, 'slamos', 'Admin', 'Login', '2024-12-14 12:33:17'),
(73, 'slamos', 'Admin', 'added user aymen', '2024-12-14 12:37:45'),
(76, 'slamos', 'Admin', 'Login', '2024-12-14 13:42:17');

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `ID` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `deadline` date DEFAULT NULL,
  `priority` enum('Low','Medium','High') NOT NULL,
  `responsible_team` varchar(255) NOT NULL,
  `responsible_member` varchar(40) DEFAULT NULL,
  `status` enum('Not started','In Progress','Completed') NOT NULL DEFAULT 'Not started'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`ID`, `title`, `description`, `deadline`, `priority`, `responsible_team`, `responsible_member`, `status`) VALUES
(1, 'Create Landing page', '................;', '0000-00-00', 'High', 'Design', 'anis zaimen', 'In Progress'),
(2, 'important task', 'blablablablablabalb', '2024-11-18', 'Low', 'Development', 'qsdqs qsdq', 'Completed'),
(4, 'sdfsd', 'fsfsdf', '2024-12-29', 'Medium', 'Development', 'birouk islam', 'In Progress'),
(5, 'Logo Redesign', 'Redesign the company logo for a fresh look', '2024-06-05', 'High', 'Design', 'anis zaimen', 'In Progress'),
(6, 'Social Media Campaign', 'Launch a summer marketing campaign on social media', '2024-06-10', 'Medium', 'Marketing', 'bessam chamekh', 'Not started'),
(7, 'API Development', 'Develop REST APIs for the new feature', '2024-06-15', 'High', 'Development', NULL, 'Not started'),
(8, 'Data Cleaning', 'Clean and preprocess customer purchase data', '2024-06-12', 'Low', 'Data Analysis', 'aymen boumezbeur', 'Not started'),
(9, 'Project Kickoff Meeting', 'Conduct the project kickoff meeting with stakeholders', '2024-06-08', 'High', 'Managemnt', 'yassine krika', 'Completed'),
(10, 'Website Mockup', 'Create wireframes and high-fidelity mockups for the website', '2024-06-14', 'Medium', 'Design', NULL, 'Not started'),
(11, 'Email Campaign', 'Send promotional emails for the product launch', '2024-06-18', 'Low', 'Marketing', 'abdelmadjid belilet', 'In Progress'),
(12, 'Database Optimization', 'Optimize queries for faster database performance', '2024-06-20', 'High', 'Development', NULL, 'Not started'),
(13, 'Sales Report Analysis', 'Analyze quarterly sales report to identify trends', '2024-06-25', 'Medium', 'Data Analysis', 'chettab mohcine', 'Not started'),
(14, 'Team Performance Review', 'Evaluate team performance for the current quarter', '2024-06-30', 'High', 'Managemnt', 'yassine krika', 'In Progress');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL,
  `team` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `username`, `password`, `first_name`, `last_name`, `role`, `team`) VALUES
(1, 'slamos', 'aaaa', 'Islam', 'Birouk', 'Admin', 'NULL'),
(2, 'MokhtarRida', 'aa', 'Rida', 'Mokhtar', 'Member', 'Development'),
(5, 'fateh', 'pp', 'fateh', 'baha', 'Head', 'Marketing'),
(6, 'slamo', 'aa', 'birouk', 'islam', 'Member', 'Development'),
(8, 'rami', 'qsdqs', 'Rami', 'Guessab', 'Head', 'Development'),
(9, 'khmamoun', '2003', 'mamoune', 'khaldi', 'Head', 'Data Analysis'),
(10, 'walidos', 'azerty', 'walid', 'moussaoui', 'Head', 'Design'),
(11, 'nisso', '1234567', 'anis', 'zaimen', 'Member', 'Design'),
(12, 'minou', 'okokokok', 'aymen', 'boumezbeur', 'Member', 'Data Analysis'),
(13, 'tamime', 'kokokoko', 'Tamime', 'Ziyane', 'Head', 'Managemnt'),
(14, 'yasg4mer', 'azazaz', 'yassine', 'krika', 'Member', 'Managemnt'),
(15, 'bess', '121212', 'bessam', 'chamekh', 'Member', 'Marketing'),
(16, 'chetiteb', 'aqaqaq', 'chettab', 'mohcine', 'Member', 'Data Analysis'),
(17, 'oussama', 'xoxoxoxo', 'abdelmadjid', 'belilet', 'Member', 'Marketing'),
(18, 'aymen', 'aaaaa', 'aymen', 'saidi', 'Member', 'Data Analysis');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `actions_history`
--
ALTER TABLE `actions_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `actions_history`
--
ALTER TABLE `actions_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
