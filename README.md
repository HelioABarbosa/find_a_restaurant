# Find-A-Restaurant

This dashboard was built to investigate restaurant and cuisine ratings from all over the world.
The project was developed while studying with “Comunidade DS”, a community of data enthusiasts and avid learners that share experiences and take into consideration real-world problems to elaborate solutions within market standards.

## 1) Business Problem

To facilitate data-driven decisions, the Find-a-Restaurant project started. The project used the Zomato Restaurants database, which helps clients to find restaurants worldwide, informing the cuisines, addresses, booking information, and delivery information of restaurants; alongside a rating system.

The business problem was creating a dashboard that allows strategic planning, and analyzing the data to answer relevant business questions.

## 2) Basic Assumptions

- The business is a catalog of restaurants with worldwide representation
- The analysis was made during the week of August 07, 2023.
- It was given focuses on the countries' data, the cities' data, and the cuisines' data
- Data source: https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv

## 3) Problem-solving strategy

The goal was to make a dashboard using Python that would have a main page and three other pages for the analysis (countries, cities, and cuisines). To avoid performance issues on the home page, the interactive map was moved to a separate dashboard and the filters were set to less selected options by default. There’s a notebook with more analysis for future uses, but the analysis pages on the dashboard have the following metrics:

### I - Home
- General metrics
- Detailed instructions to use all the pages on the dashboard, including possible issues that could arise in case of excessive filtering. There are instructions to help any user to solve potential issues that may arise if an error is found.

### II - Countries
- Number of registered restaurants per country;
- Number of registered cities per country;
- The mean number of ratings per country;
- Mean aggregate rating per country;
- Number of cuisines per country;
- The mean average cost for two per country.

### III - Cities
- Top 10 cities with the most restaurants on the database;
- Top 5 cities with restaurants with an average rating > 4;
- Top 5 cities with restaurants with an average rating < 2.5;
- Top 10 cities with unique cuisine types;

### IV - Cuisines
- Best restaurant from popular cuisines;
- Top 10 restaurants overall;
- Top 10 cuisines with the highest mean average cost for two;
- Top 10 cuisines;
- Bottom 10 cuisines.

### V - World Map
Interactive world map with sidebar options. Selecting all options available could cause performance issues in older systems due to the size of the database.

## 4. Top 3 Data-driven Insights

### I - The database has a lot of results from India and there’s a relevant segmentation of Indian cuisines to be considered (“North Indian”, “Modern Indian”, “South Indian”), which should be considered in the decision-making process. (Note: Sometimes removing India from the filters helps to visualize the metrics for different countries)

### II - Brazilian ratings are significantly lower than other countries in the database, with a significant number of restaurants in major cities with low ratings. Considering the size of the Brazilian market, specific strategies could be adopted to improve the overall experience in that country.

### III - United States is the top 2 country in number of restaurants and the top 4 when it comes to mean average ratings. Alongside India, that market can be used to inspire strategies for other marketings that are underperforming by some metrics, like Brazil.

## 5. Final Product

Online dashboard hosted in the cloud that can be accessed by any device connected to the web using the following link:

https://find-a-restaurant.streamlit.app/

## 6. Conclusion

The dashboard can be used as a tool for data-driven decisions with good usability for company staff with different backgrounds and different levels of computer skills.

## 7. Next steps

- Collecting user feedback to reevaluate the “top restaurant per food type” section because, while it is an important metric for users, it can lead to problems if one of the popular restaurant types is removed from the filters. An alternative could be moving that section to a different page without cuisine filters;
- Turning some metrics into percentiles to improve some visualizations;
- Adding new visions according to the company strategies;
