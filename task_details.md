# **Analytics & Insights Lead Technical Challenge**

# **Introduction**

Welcome to this Technical Challenge! This exercise aims to assess your coding skills, SQL proficiency, and problem-solving mindset. We expect this to take no more than 4 hours.

Please submit your solution as a GitHub repository, including:

- The code
- A `README.md` explaining how to run the application, your design choices, and your data analysis

You can use **Python**.

<aside>
💡

We will assess:

- Correctness and efficiency of your solution.
- Code structure and cleanliness.
- SQL query efficiency and database schema design.
- Data handling and validation.
- Git history and commit messages.
- The depth of your data analysis and forecasting.
</aside>

# **Challenge**

You are provided with simplified and truncated CSV files containing invoice and customer data.

[**📁 Invoices**](https://docs.google.com/spreadsheets/d/1SqVP-dvsAbm3sQLWX06qsQWs7JRHmqFBsyeWmhS8io8/edit?usp=sharing)

[**📁 Customers**](https://docs.google.com/spreadsheets/d/14u0G1C4F5nXb0rGhQFfm2Vd6qNTLWVoA3F6Mq0ph8Vw/edit?usp=sharing)

Your task is:

1. **Data Ingestion and Database Design:**
    - Design a relational database schema to store the invoice data. You can use any SQL database (PostgreSQL, SQLite etc.).
    - Write a script to import the CSV data into your database.
    
    <aside>
    💡
    
    Make sure all steps are reproducible. 
    
    </aside>
    
2. **Monthly Recurring Revenue (MRR) Calculation:**
    - Implement program to calculate the MRR of any customer at any given date. Outline any limitations or unknowns you might encounter.
    - Build a basic cohort segmentation of the MRR.
3. **Data Analysis and Insights:**
    - Analyze the calculated MRR data (from task 2) to identify trends and patterns.
    - Implement program that will calculate:
        - Month-over-month MRR growth
        - Identifying days with significant changes
        - Calculate churn rate
        - Biggest customers
        - (**optional**) Metric of your choice. Is there anything that you would find interesting?
    - You are free to use any libraries or tools within your chosen language to assist with the analysis.
4. **(Optional) Basic Forecasting:**
    - Develop a simple forecast for future MRR based on the observed trends.
    - Identify potential risks or factors that could impact the forecast.
    - Provide the forecast results.

**Output options**

You can structure your output the way you find most efficient. This may include, but is not limited to:

- A set of standalone programs.
- A RESTful API with small service.
- Output files such as JSON or CSV.
- Any other reasonable method.

The `README.md` should clearly explain how to run the your solution and access the results.