# cust-eval
Customer Evaluation CLI Tool

a CLI called cust-eval using lifetimes’ Beta-Geometric model with the following two commands:

Install-Package by using:
pip install .

How Run CLI Tool:
a. Top predicted purchases — you let your user pass the csv and number
of customers then and return the top N customers with the most
purchases and how many purchases are expected:

cust-eval count -n 100 --input data/data.csv --output data/count.csv

b. Top predicted spend — you let your user pass the csv and number of
customers then and return the top spending customers and their
expected spend:

cust-eval spend -n 100 --input data/data.csv --output data/spend.csv
