# Customer Data Management and Improvement

This repository contains the code and documentation for a project focused on managing and improving customer data through various work packages, ranging from database management and data warehousing to machine learning model development and deployment. The goal is to build a comprehensive system for storing, analyzing, and extracting valuable insights from customer data using SQL databases, Python, Azure services, and MLOps.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Work Packages](#work-packages)
  - [Work Package 1: Data Management and SQL Database Setup](#work-package-1-data-management-and-sql-database-setup)
  - [Work Package 2: Data Warehousing and Python Programming](#work-package-2-data-warehousing-and-python-programming)
  - [Work Package 3: Data Science and Azure Integration](#work-package-3-data-science-and-azure-integration)
  - [Work Package 4: MLOps, Deployment, and Final Presentation](#work-package-4-mlops-deployment-and-final-presentation)
- [Technologies Used](#technologies-used)
- [Deliverables](#deliverables)
- [Team Members](#team-members)

## Project Overview

This project focuses on building a robust system for customer data management, including database setup, data warehousing, data analysis, and machine learning model deployment. The project is divided into four main work packages, each addressing a specific aspect of data management and analysis.

## Repository Structure

```bash
├───CSV                        # Sample data and CSV files
├───Database                   # SQL database schema and data warehouse
├───Req1                       # Work Package 1: Data Management and SQL Database Setup
├───Req2                       # Work Package 2: Data Warehousing and Python Programming
├───Req3                       # Work Package 3: Data Science and Azure Integration
│   ├───models                 # Machine learning models
│   ├───notebooks              # Jupyter notebooks for analysis
│   └───scripts                # Python scripts for data analysis and model training
└───Req4                       # Work Package 4: MLOps, Deployment, and Final Presentation
    ├───mlflow                 # MLflow tracking and experiment management
    └───templates              # Web application templates for deployment
```
## Database Used

The project uses a dataset sourced from Kaggle, titled [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/erak1006/brazilian-e-commerce-company-olist).

This dataset contains a range of information from a large e-commerce platform, Olist, including customer details, order transactions, product reviews, and other important e-commerce activities. The dataset is structured to support analysis of customer behavior, sales trends, and other e-commerce insights.

**Dataset Highlights**:
- Customer information
- Product order history
- Transactional data including payments and shipping
- Product reviews and ratings

We use this dataset to build our SQL schema, analyze customer behavior, and train machine learning models for customer churn prediction.
## Work Packages

### Work Package 1: Data Management and SQL Database Setup

- **Objective**: Design and implement a SQL database for storing customer-related information such as personal details, transactions, and interactions.
- **Tools**: Microsoft SQL Server, SQL Server Management Studio
- **Deliverables**:
  - SQL database schema design
  - Sample data population script
  - SQL queries for extracting and analyzing customer data

### Work Package 2: Data Warehousing and Python Programming

- **Objective**: Set up a SQL Data Warehouse for aggregating large volumes of customer data and develop Python scripts for interacting with the database.
- **Tools**: Microsoft SQL Data Warehouse, Python (Pandas, SQLAlchemy)
- **Deliverables**:
  - A fully functioning SQL Data Warehouse
  - Python scripts for data extraction and transformation

### Work Package 3: Data Science and Azure Integration

- **Objective**: Conduct data analysis and build predictive models using Python and integrate Azure services to manage customer data.
- **Tools**: Python (Scikit-learn, Matplotlib), Azure Data Studio, Azure Machine Learning
- **Deliverables**:
  - Customer churn prediction model
  - Analysis report with insights and predictions

### Work Package 4: MLOps, Deployment, and Final Presentation

- **Objective**: Implement MLOps for managing machine learning experiments and deploy the trained models for customer data predictions.
- **Tools**: MLflow, Azure services, Flask/Streamlit (for web application deployment)
- **Deliverables**:
  - Deployed machine learning model or web application for customer data predictions
  - MLflow setup for tracking experiments

## Technologies Used

- **Database**: Microsoft SQL Server, SQL Server Management Studio, SQL Data Warehouse
- **Python**: Pandas, SQLAlchemy, Scikit-learn, Matplotlib
- **Azure**: Azure Data Warehouse (Synapse Analytics)
- **MLOps**: MLflow for experiment tracking and model management
- **Web Framework**: Flask (for model deployment)

## Deliverables

1. **SQL Database**: Schema design and SQL queries for data management and extraction.
2. **Python Scripts**: For data extraction, cleaning, and preparation.
3. **Machine Learning Models**: Trained predictive models for customer data analysis.
4. **Web Application**: A deployed application using Flask for making predictions using the trained machine learning models.
5. **Final Presentation**: Brief Project Presentation.

## Team Members

- **Kirollos Ehab**
- **Ahd Islam**
- **Alaa Magdy**
- **Farah Walid**
- **Youssef Hany**
