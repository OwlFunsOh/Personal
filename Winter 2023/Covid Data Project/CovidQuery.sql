--SELECT *
--FROM covid_deaths
--ORDER BY location, date

--SELECT *
--FROM covid_vaccinations
--ORDER BY location, date

--Above, I verified that the excel sheet was loaded in properly

--SELECT location, date, total_cases, new_cases, total_deaths, population
--FROM covid_deaths
--ORDER BY location, date

-- Querying total cases vs total deaths
-- I want to know the percentage of people dying who report
-- being infected.
-- Equation: (total_deaths / total_cases) * 100

-- BELOW RESULTS IN AN ERROR!!!

SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases) * 100 AS [Percentage of Deaths]
FROM covid_deaths
ORDER BY location, date

-- ERROR 1: I thought that the integers in the table were going to be automatically
-- converted into an int type so I can divide. However, doing so results in an error
-- because the operand/column data type is actually an nvarchar. Thus, I need to convert
-- it to an int somehow.
-- Below is the code that verifies that the column data type is actually an nvarchar

SELECT data_type
FROM information_schema.columns
WHERE table_name = 'covid_deaths' AND column_name = 'total_cases'

SELECT data_type
FROM information_schema.columns
WHERE table_name = 'covid_deaths' AND column_name = 'total_deaths'

-- Now, I will attempt to convert an nvarchar to an int so I can perform the
-- necessary calculation

CREATE TABLE check_death_datatype(
[Total Deaths] int
)

SELECT *
FROM check_death_datatype

INSERT INTO check_death_datatype
SELECT CONVERT(int, covid_deaths.total_deaths)
FROM covid_deaths

-- Now that I found a solution, let's check again if the datatype
-- is now an int

SELECT data_type
FROM information_schema.columns
WHERE table_name = 'check_death_datatype' AND column_name = 'Total Deaths'

-- It is now changed to an int! Unfortunately, I had to create another table though.
-- I did not know how to do it using a temporary table.
-- Now that we know how to convert a column to an int, we should now be able to 
-- do the percentage calculation like we tried before.

SELECT 
	location,
	date, 
	total_cases,
	total_deaths,
	((CONVERT(int, covid_deaths.total_deaths) / (CONVERT(int, covid_deaths.total_cases))) * 100) AS [Percentage of Deaths]
FROM 
	covid_deaths
ORDER BY 
	[Percentage of Deaths] DESC

-- ERROR 2: Unfortunately, I was getting a lot of zeroes. This is because I am doing integer division and not
-- float division. Now, I should change the datatype of the column to float instead of int

SELECT 
	location,
	date, 
	total_cases,
	total_deaths,
	((CONVERT(float, covid_deaths.total_deaths) / (CONVERT(float, covid_deaths.total_cases))) * 100) AS [Percentage of Deaths]
FROM 
	covid_deaths
ORDER BY 
	location,
	date

-- It worked! Let's explore the country of the United States

SELECT 
	location,
	date, 
	total_cases,
	total_deaths,
	((CONVERT(float, covid_deaths.total_deaths) / (CONVERT(float, covid_deaths.total_cases))) * 100) AS [Percentage of Deaths]
FROM 
	covid_deaths
WHERE
	location = 'United States'
ORDER BY 
	location,
	date

-- What can I learn from above:
-- As of 01/14/2024 which was last week (at the time I'm making this), If I contracted covid-19, the chance of me dying to it
-- is around 1.123%. This sounds low until you realize that in numbers, that is equivalent to 1,161,235
-- people dying in the United States.

-- Next, I want to know how much of the total population has been infected.
-- Equation: (Total Cases / Population) * 100

SELECT 
	location,
	date,
	total_cases,
	population,
	((CONVERT(float, covid_deaths.total_cases) / (CONVERT(float, covid_deaths.population))) * 100) AS [Percentage Infected]
FROM
	covid_deaths
WHERE
	location = 'United States'
ORDER BY
	location,
	date

-- As of 01/14/2024, the data shows that 30.576% of people living in the United States have been infected by Covid 19 at some point

-- Now, I want to know what countries have the highes infection rates compared to population?

SELECT 
	location,
	MAX(CONVERT(float, total_cases)) AS [Total Cases],
	population,
	(MAX((CONVERT(float, covid_deaths.total_cases)) / (CONVERT(float, covid_deaths.population))) * 100) AS [Highest Percentage of Infections]
FROM
	covid_deaths
WHERE
	continent IS NOT NULL
GROUP BY
	population,
	location
ORDER BY
	[Highest Percentage of Infections] DESC


-- Now, I want to know the countries with the highest death count

SELECT 
	location,
	MAX(CONVERT(float, total_deaths)) AS [Total Deaths]
FROM
	covid_deaths
WHERE
	continent IS NOT NULL
GROUP BY
	location
ORDER BY
	[Total Deaths] DESC

-- Now let's go bigger and look at things by continent

SELECT 
	location,
	MAX(CONVERT(float, total_deaths)) AS [Total Deaths]
FROM
	covid_deaths
WHERE
	continent IS NULL
GROUP BY
	location
ORDER BY
	[Total Deaths] DESC


-- Now, I want to see only global numbers
SELECT
	SUM(CONVERT(float, covid_deaths.new_cases)) AS [Total Cases],
	SUM(CONVERT(float, covid_deaths.new_deaths)) AS [Total Deaths],
	SUM(CONVERT(float, covid_deaths.new_deaths)) / SUM(CONVERT(float, covid_deaths.new_cases)) * 100 AS [Death Percentage]
FROM
	covid_deaths
WHERE
	continent IS NOT NULL AND new_cases <> 0
ORDER BY
	1, 2
