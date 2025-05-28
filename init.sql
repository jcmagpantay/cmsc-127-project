-- Database Creation
CREATE DATABASE 127project;

CREATE TABLE member(
	member_id INT(5) NOT NULL AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	gender VARCHAR(6),
	degree_program VARCHAR(50) NOT NULL,
	password VARCHAR(20) NOT NULL,
	access_level INT(1) NOT NULL,
	username VARCHAR(20) NOT NULL,
	PRIMARY KEY(member_id),
	CONSTRAINT member_username_uk UNIQUE(username)
);

-- ORGANIZATION TABLE CREATION
CREATE TABLE organization(
	organization_id INT(5) NOT NULL AUTO_INCREMENT,
	organization_name VARCHAR(20) NOT NULL,
	date_established DATE NOT NULL,
	PRIMARY KEY(organization_id),
	CONSTRAINT organization_organization_name_uk UNIQUE KEY(organization_name)
);

-- MEMBER_ORG TABLE CREATION
-- Relationship of member BEING IN an organization
-- All organization related roles are here
-- MANY to MANY relationship
CREATE TABLE member_org (
    member_id INT(5),
    organization_id INT(5),
    batch VARCHAR(20) NOT NULL,
    status VARCHAR(10) NOT NULL,
    role VARCHAR(10) NOT NULL,
    committee VARCHAR(20),
    academic_year VARCHAR(10) NOT NULL,
    semester INT(1) NOT NULL,
    PRIMARY KEY (member_id, organization_id, academic_year, semester),
    FOREIGN KEY (member_id) REFERENCES member(member_id),
    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
);


-- FINANCIAL_RECORD TABLE CREATION
-- The financial records of an organization
-- FINANCIAL_RECORD has MULTIPLE FEES
-- ORG has MULTIPLE RECORDS
CREATE TABLE financial_record(
	record_id INT(5) NOT NULL AUTO_INCREMENT,
	balance INT(10) NOT NULL,
	academic_year VARCHAR(10) NOT NULL,
	semester INT(1) NOT NULL,
	organization_id INT(5) NOT NULL,
	PRIMARY KEY(record_id),
	CONSTRAINT financial_record_organization_id_fk FOREIGN KEY(organization_id) REFERENCES organization(organization_id)
);

-- FEE TABLE CREATION
-- FEEs belong in a FINANCIAL_RECORD
-- MEMBERs have MULTIPLE FEEs
CREATE TABLE fee(
	fee_id INT(5) NOT NULL AUTO_INCREMENT,
	amount INT(10) NOT NULL,
	due_date DATE NOT NULL,
	date_issued DATE NOT NULL,
	fee_type VARCHAR(50) NOT NULL,
	payment_status VARCHAR(10) NOT NULL,
	pay_date DATE,
	description VARCHAR(50),
	member_id INT(5) NOT NULL,
	record_id INT(5) NOT NULL,
	PRIMARY KEY(fee_id),
	CONSTRAINT fee_member_id_fk FOREIGN KEY(member_id) REFERENCES member(member_id),
	CONSTRAINT fee_record_id_fk FOREIGN KEY(record_id) REFERENCES financial_record(record_id)
);

-- Sample Members
INSERT INTO member (member_id, name, gender, degree_program, password, access_level, username) VALUES
(1, 'Olivia Santos', 'Female', 'BS Environmental Science', 'pass1', 1, 'osantos'),
(2, 'Jacob Mendoza', 'Male', 'BS Computer Science', 'pass2', 1, 'jmendoza'),
(3, 'Mia Cruz', 'Female', 'BS Psychology', 'pass3', 2, 'mcruz');

INSERT INTO member (member_id, name, gender, degree_program, password, access_level, username) VALUES
(4, 'Lorenzo dela Cruz', 'Male', 'BS Agriculture', 'pass4', 1, 'ldelacruz'),
(5, 'Anna Villanueva', 'Female', 'BS Forestry', 'pass5', 1, 'avillanueva'),
(6, 'Carlos Tan', 'Male', 'BS Biology', 'pass6', 2, 'ctan'),
(7, 'Maria Lim', 'Female', 'BA Sociology', 'pass7', 1, 'mlim'),
(8, 'Jose Padilla', 'Male', 'BS Civil Engineering', 'pass8', 2, 'jpadilla'),
(9, 'Teresita Mabini', 'Female', 'BS Development Communication', 'pass9', 1, 'tmabini');

-- Sample Organizations
INSERT INTO organization (organization_id, organization_name, date_established) VALUES
(1, 'EnviroOrg', '2010-06-15'),
(2, 'CodeSoc', '2015-08-01'),
(3, 'PsyCircle', '2000-01-01');

INSERT INTO organization (organization_id, organization_name, date_established) VALUES
(4, 'AgriCore', '1998-07-01'),
(5, 'SocioLeague', '2005-06-15'),
(6, 'ACSS', '2011-04-14');

-- Member-Org Relationships (snapshots)
INSERT INTO member_org (member_id, organization_id, batch, status, role, committee, academic_year, semester) VALUES
(1, 1, 'Crescendo', 'Active', 'Member', 'Logistics', '2023-2024', 1),
(1, 2, 'Dream', 'Active', 'Member', 'Finance', '2023-2024', 2),
(1, 3, 'Oryza', 'Alumni', 'Member', 'Academic', '2024-2025', 2),
(2, 2, 'Flash', 'Active', 'President', 'Executive', '2023-2024', 1),
(2, 3, 'Sweep', 'Active', 'Member', 'Publicity', '2023-2024', 2),
(3, 1, 'Satoru', 'Alumni', 'Secretary', 'Executive', '2022-2023', 2),
(3, 2, 'Gojo', 'Active', 'Member', 'Membership', '2023-2024', 1),--
(4, 4, 'Lotus 2.0', 'Active', 'Member', 'Finance', '2023-2024', 1),
(4, 5, 'Arpeggio', 'Active', 'Member', 'Documentation', '2023-2024', 2),
(5, 6, 'Hash', 'Active', 'Member', 'Academic', '2023-2024', 2),
(5, 4, 'NBA2K', 'Active', 'Member', 'Logistics', '2023-2024', 1),
(6, 3, 'Alpha', 'Active', 'Member', 'Publicity', '2023-2024', 2),
(6, 2, 'Catalyst', 'Active', 'Secretary', 'Executive', '2023-2024', 1),
(7, 6, 'Nova', 'Active', 'President', 'Executive', '2023-2024', 1),
(7, 2, 'Catalyst', 'Active', 'Secretary', 'Executive', '2023-2024', 2),
(8, 6, 'Nova', 'Active', 'President', 'Executive', '2024-2025', 2),
(9, 6, 'Nova', 'Active', 'Member', 'Publicity', '2023-2024', 1);


-- Financial Records (snapshots for each org at each academic year/semester)
INSERT INTO financial_record (balance, academic_year, semester, organization_id) VALUES
-- EnviroOrg (org_id: 1)
(15750.50, '2022-2023', 2, 1),
(18200.75, '2023-2024', 1, 1),

-- CodeSoc (org_id: 2)
(22400.00, '2023-2024', 1, 2),
(19850.25, '2023-2024', 2, 2),

-- PsyCircle (org_id: 3)
(8950.00, '2023-2024', 2, 3),
(12300.50, '2024-2025', 2, 3),

-- AgriCore (org_id: 4)
(16500.00, '2023-2024', 1, 4),

-- SocioLeague (org_id: 5)
(11200.75, '2023-2024', 2, 5),

-- ACSS (org_id: 6)
(25600.00, '2023-2024', 1, 6),
(27150.50, '2023-2024', 2, 6),
(29800.25, '2024-2025', 2, 6);

-- Fee Records (at least 2 per member with varied payment statuses)
INSERT INTO fee (amount, due_date, date_issued, fee_type, payment_status, pay_date, description, member_id, record_id) VALUES
-- Member 1 (Olivia Santos) - EnviroOrg and CodeSoc
(500.00, '2023-08-15', '2023-07-01', 'Membership', 'Paid', '2023-08-10', 'Annual membership fee - EnviroOrg', 1, 2),
(250.00, '2023-09-30', '2023-09-01', 'Activity', 'Unpaid', NULL, 'Environmental symposium fee', 1, 2),
(750.00, '2024-02-15', '2024-01-15', 'Membership', 'Paid', '2024-02-20', 'Semester membership - CodeSoc (Late Payment)', 1, 3),
(300.00, '2024-03-10', '2024-02-25', 'Event', 'Paid', '2024-03-05', 'Coding workshop fee', 1, 3),

-- Member 2 (Jacob Mendoza) - CodeSoc and PsyCircle
(800.00, '2023-08-20', '2023-07-15', 'Leadership', 'Paid', '2023-08-18', 'President fee - CodeSoc', 2, 2),
(400.00, '2023-10-15', '2023-09-20', 'Activity', 'Unpaid', NULL, 'Tech conference registration', 2, 2),
(350.00, '2024-02-28', '2024-01-30', 'Membership', 'Paid', '2024-03-05', 'PsyCircle membership (Late Payment)', 2, 4),
(200.00, '2024-04-15', '2024-03-20', 'Event', 'Paid', '2024-04-12', 'Psychology seminar fee', 2, 4),

-- Member 3 (Mia Cruz) - EnviroOrg and CodeSoc
(600.00, '2022-12-15', '2022-11-15', 'Leadership', 'Paid', '2022-12-10', 'Secretary fee - EnviroOrg', 3, 1),
(300.00, '2023-01-30', '2022-12-20', 'Activity', 'Paid', '2023-02-05', 'Research project fee (Late Payment)', 3, 1),
(450.00, '2023-08-25', '2023-07-20', 'Membership', 'Unpaid', NULL, 'CodeSoc annual fee', 3, 2),
(250.00, '2023-09-15', '2023-08-30', 'Event', 'Paid', '2023-09-12', 'Programming bootcamp', 3, 2),

-- Member 4 (Lorenzo dela Cruz) - AgriCore and SocioLeague
(550.00, '2023-08-10', '2023-07-10', 'Membership', 'Paid', '2023-08-08', 'AgriCore membership fee', 4, 5),
(400.00, '2023-10-20', '2023-09-25', 'Activity', 'Paid', '2023-10-25', 'Farm visit fee (Late Payment)', 4, 5),
(350.00, '2024-02-20', '2024-01-25', 'Membership', 'Unpaid', NULL, 'SocioLeague semester fee', 4, 6),
(275.00, '2024-03-15', '2024-02-28', 'Event', 'Paid', '2024-03-10', 'Social research workshop', 4, 6),

-- Member 5 (Anna Villanueva) - ACSS and AgriCore
(600.00, '2024-02-25', '2024-01-20', 'Membership', 'Paid', '2024-02-22', 'ACSS membership fee', 5, 7),
(320.00, '2024-04-10', '2024-03-15', 'Activity', 'Unpaid', NULL, 'Computer science competition fee', 5, 7),
(480.00, '2023-08-30', '2023-07-25', 'Membership', 'Paid', '2023-09-05', 'AgriCore membership (Late Payment)', 5, 5),
(200.00, '2023-11-15', '2023-10-20', 'Event', 'Paid', '2023-11-12', 'Agricultural expo fee', 5, 5),

-- Member 6 (Carlos Tan) - PsyCircle and CodeSoc
(400.00, '2024-02-28', '2024-01-28', 'Membership', 'Paid', '2024-03-10', 'PsyCircle membership (Late Payment)', 6, 4),
(250.00, '2024-04-20', '2024-03-25', 'Activity', 'Unpaid', NULL, 'Psychology research fee', 6, 4),
(700.00, '2023-08-15', '2023-07-12', 'Leadership', 'Paid', '2023-08-12', 'Secretary fee - CodeSoc', 6, 2),
(300.00, '2023-10-05', '2023-09-10', 'Event', 'Paid', '2023-10-02', 'Tech summit registration', 6, 2),

-- Member 7 (Maria Lim) - ACSS and CodeSoc
(850.00, '2023-08-05', '2023-07-05', 'Leadership', 'Paid', '2023-08-03', 'President fee - ACSS', 7, 7),
(380.00, '2023-09-20', '2023-08-25', 'Activity', 'Paid', '2023-09-25', 'CS project development (Late Payment)', 7, 7),
(650.00, '2024-02-10', '2024-01-10', 'Leadership', 'Unpaid', NULL, 'Secretary fee - CodeSoc', 7, 3),
(290.00, '2024-03-25', '2024-02-28', 'Event', 'Paid', '2024-03-22', 'Software engineering workshop', 7, 3),

-- Member 8 (Jose Padilla) - ACSS
(750.00, '2025-02-15', '2025-01-15', 'Leadership', 'Paid', '2025-02-20', 'President fee - ACSS (Late Payment)', 8, 8),
(420.00, '2025-03-30', '2025-03-01', 'Activity', 'Unpaid', NULL, 'Systems development project', 8, 8),

-- Member 9 (Teresita Mabini) - ACSS
(500.00, '2023-08-12', '2023-07-15', 'Membership', 'Paid', '2023-08-10', 'ACSS membership fee', 9, 7),
(350.00, '2023-10-25', '2023-09-30', 'Activity', 'Paid', '2023-10-30', 'Programming competition (Late Payment)', 9, 7);