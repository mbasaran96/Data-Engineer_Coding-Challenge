# Data-Engineer_Coding-Challenge
*Hands-on coding exercise for a Junior Data Engineer position*

#### Enclosed you will find the task for the challenge

Challenge Overview
You've been provided with a flat table in CSV format (attached) containing retail sales data from various stores across Munich.
This dataset includes transaction records, store information, product details, and customer data all combined into a single denormalized structure.
Your task is to:

1. Design a proper data model for this dataset
2. Document your data model
3. Deploy the schema to a database (ORM libraries like SQLAlchemy are fine)
4. Develop a data pipeline to clean, transform and load the data from the CSV file into your database schema

Dataset Details
The file munich_sales.csv contains the following information:

- Transaction records with timestamps
- Store details including location and type
- Product information including categories and pricing
- Customer data including loyalty status and demographics
- Sales information including staff, promotions, and discounts

### Requirements

**1. Data Modeling**

* Analyze the provided CSV file to understand the data structure
* Design a dimensional data model (star or snowflake schema) with appropriate fact and dimension tables
* Identify primary and foreign keys
* Consider performance implications of your design (optional)

**2. Documentation**

* Document any assumptions you made about the data
* Create an Entity-Relationship Diagram (ERD) illustrating your data model
* Document the purpose of each table in your schema

**3. Database and Schema Deployment**

* Write SQL scripts to create your database schema
* Include appropriate data types, constraints
* Ensure your scripts are idempotent (can be run multiple times without error)
* You may use any SQL database for this exercise:
* PostgreSQL (either locally installed or in Docker)
* SQLite for a simpler setup
* or any other relational database of your choice
* Your solution should include clear documentation on how to set up and connect to your chosen database

**4. Data Pipeline Implementation**

* Create a Python script to:
* Extract data from the CSV file
* Transform the data to fit your data model
* Load the transformed data into your database

**Technical Constraints**

* Use Python for your data pipeline implementation
* Use a relational database (PostgreSQL preferred, but SQLite or any relational database is fine)  maybe use Docker (optional)? 
* Your solution should be easily runnable on another machine
