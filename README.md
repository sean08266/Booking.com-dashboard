# Booking.com-dashboard

## Introduction
In this project, I am tasked with scraping data from booking.com and performing various operations. Let me delve into the details. This assignment serves as both a roadmap and a primer, providing hands-on exposure to key tools such as terminal usage, web crawling, Git version control, and data application development. 

The results are as follows, and the dashboard allows users to dynamically add input fields for location and dates to trigger the web crawler:
  
###### ![image](https://github.com/sean08266/Booking.com-dashboard/blob/main/Dashboard%20sample.png)

## Description

### Step 1: Web Crawling
In a Jupyter notebook named web_crawler.ipynb, write a web crawler to fetch
data from booking.com. Implement a function that takes “location”, “check-in date”,and “check-out date” as inputs and returns a DataFrame containing hotel details like
name, location, price, rating, distance, and comments. Commit this notebook to the Git
repository with a clear commit message.

###### ![image](https://github.com/sean08266/Booking.com-dashboard/blob/main/.png/ex1.png)

### Step 2: Data Cleaning
After scraping, ensure data types are correctly formatted: “price” as integer, “rat-
ing” as float, “comment” as string, and “distance” in kilometers (as a float).



