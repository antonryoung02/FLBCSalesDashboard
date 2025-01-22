## Summary 

This dashboard was created specifically for management at Flathead Lake Brewing Company because I noticed the difficulty of extracting sales trends and insights from excel spreadsheets. I made this standalone tool to read the company's sales data, apply transformations to reveal meaningful trends, and display them in an easy-to-use interface.

The [app/](https://github.com/antonryoung02/FLBCSalesDashboard/tree/main/app) directory contains the executable script (main.py) as well as other helper functions and classes.

The [app/display_data](https://github.com/antonryoung02/FLBCSalesDashboard/tree/main/app/display_data) directory contains the functions to create each visualization.

The [app/transform_data](https://github.com/antonryoung02/FLBCSalesDashboard/tree/main/app/transform_data) directory contains the functions that perform the data transformation steps in the project.

The [tests/](https://github.com/antonryoung02/FLBCSalesDashboard/tree/main/tests) directory provides a way to validate the correctness of the code.

<img width="995" alt="Screenshot 2025-01-22 at 2 36 03 PM" src="https://github.com/user-attachments/assets/71382eff-58dd-4c38-9dec-925cae7b7a2d" />

## Explanation

#### Filters

Each visualization uses a filter object to isolate the data of interest. The user chooses which feature to display (number of items sold, total profit, % of revenue, etc) and can filter by products and time range.

#### Menu Engineering Matrix

One important measure for menu items in restaurant sales analytics is the relationship between profitability and popularity. Groups of products will naturally fall into specific quadrants -- proteins like chicken and beef contribute to higher costs and desserts are less frequently ordered -- but it is useful to identify outliers in within-group values. For example, if a specific burger is much less profitable than the others you may want to consider re-sourcing an expensive ingredient, increasing the menu price, or replacing it on the menu with a more affordable alternative. The scatterplot color-codes products by category, allows category selection for within-group comparisons, and has a time slider to show how the menu engineering matrix has changed over time. 

#### Line Chart

This chart displays individual or group product trends for each feature over time. Previously, there was no easy way to see how a product or group of products changed over time as the data was spread across each month's spreadsheet.

#### Stacked Bar Chart

This chart displays the selected individual or group product values in a stacked bar chart, making it easy to visualize cumulative information.

#### Percent-change over time Bar Chart

This chart displays the percent change of a feature for each product between time A and B. It is especially useful for understanding food cost inflation for each product and making month vs month sales comparisons.



