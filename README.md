# Booking.com-dashboard

## Introduction
In this project, I am tasked with scraping data from booking.com and performing various operations. Let me delve into the details. This assignment serves as both a roadmap and a primer, providing hands-on exposure to key tools such as terminal usage, web crawling, Git version control, and data application development. 

The results are as follows, and the dashboard allows users to dynamically add input fields for location and dates to trigger the web crawler:
  
<div align="center">
  <img src="https://github.com/sean08266/Booking.com-dashboard/blob/main/Dashboard%20sample.png" width="85%" alt="image">
</div>

## Description

### Step 1: Web Crawling
In a Jupyter notebook named web_crawler.ipynb, write a web crawler to fetch
data from booking.com. Implement a function that takes “location”, “check-in date”,and “check-out date” as inputs and returns a DataFrame containing hotel details like
name, location, price, rating, distance, and comments. Commit this notebook to the Git
repository with a clear commit message.

<div align="center">
  <img src="https://github.com/sean08266/Booking.com-dashboard/blob/main/.png/ex1.png" width="75%" alt="image">
</div>

### Step 2: Data Cleaning
After scraping, ensure data types are correctly formatted: “price” as integer, “rat-
ing” as float, “comment” as string, and “distance” in kilometers (as a float).

<div align="center">
  <img src="https://github.com/sean08266/Booking.com-dashboard/blob/main/.png/ex2.png" width="75%" alt="image">
</div>

### Step 3: Data Visualization
Use Plotly to visualize the data in web_crawler.ipynb. The scatter plot should
have the price on the x-axis and distance from the center on the y-axis, color-coded by
ratings.

<div align="center">
  <img src="https://github.com/sean08266/Booking.com-dashboard/blob/main/.png/ex3.png" width="75%" alt="image">
</div>

### Step 4: Dash Application
Create a Dash web application that integrates everything. In app.py, employ Plotly Dash
to build an interactive dashboard. Add input fields for location and dates to trigger the
web crawler dynamically.The results are as shown in the initial image.

