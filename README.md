# FLBCSalesDashboard

This data pipeline & dashboard was created specifically for management at Flathead Lake Brewing Co. I noticed the difficulty of extracting sales trends and insights from excel spreadsheets and decided to make this tool which reads sales data for each month and creates a locally hosted dashboard to show metrics and trends of interest. 

## Data Flow Diagram

<img width="995" alt="Screenshot 2025-01-22 at 2 36 03 PM" src="https://github.com/user-attachments/assets/71382eff-58dd-4c38-9dec-925cae7b7a2d" />

## Explanation

#### Filters

Each visualization uses a filter object to isolate the data of interest. The user chooses which feature to display (number of items sold, total profit, % of revenue, etc) and can filter by products and time range.

#### Menu Engineering Matrix

One important measure for menu items in restaurant sales analytics is the relationship between profitability and popularity. Groups of products will naturally fall into specific quadrants -- proteins like chicken and beef lead contribute to higher costs and desserts are less frequently ordered -- but it is useful to identify outliers in within-group values. For example, if a specific burger is much less profitable than the others you may want to consider re-sourcing an expensive ingredient, increasing the menu price, or replacing it on the menu with a more affordable alternative. The scatterplot color-codes products by category, allows category selection for within-group comparisons, and has a time slider to show how the menu engineering matrix has changed over time. 

#### Line Chart

This chart displays individual or group product trends for each feature over time. Previously, there was no easy way to see how a product or group of products changed over time as the data was located across each month's spreadsheet.

#### Stacked Bar Chart

This chart displays the selected individual or group product values in a stacked bar chart, making it easy to visualize cumulative information. I was able to identify a data-entry error where newly added menu items weren't being included in the 'total revenue' sum because the cumulative '% of revenue' column did not sum to 1.

#### Percent-change over time Bar Chart

This chart displays the percent change of a feature for each product between time A and B. It is especially useful for understanding food cost inflation for each product and making month vs month sales comparisons.



