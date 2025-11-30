# Time-series_category-charts

A Python script that generates time-series and category-based sales data visualization with charts.

## Features

- **Data Generation**: Creates sample sales data for 2024 (daily sales across 4 categories: Electronics, Clothing, Home, Books)
- **Visualizations**: 
  - Daily total sales line chart
  - Monthly total sales line chart
  - Quarterly total sales line chart
  - Category-wise sales bar chart
  - Category sales share pie chart
- **Data Export**: Saves sample data to CSV format
- **Summary Report**: Generates a summary file with key metrics (total sales, top category, best month)

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib

## Installation

```bash
pip install pandas numpy matplotlib
```

## Usage

Run the script to generate all charts and data:

```bash
python Time_series.py
```

## Output

All generated files are saved in the `sales_charts_output/` directory:
- `daily_sales.png` - Daily sales trend
- `monthly_sales.png` - Monthly sales trend
- `quarterly_sales.png` - Quarterly sales trend
- `category_bar.png` - Sales by category (bar chart)
- `category_pie.png` - Category sales distribution (pie chart)
- `sample_sales.csv` - Raw sales data
- `summary.txt` - Summary statistics

## Notes

- The script uses a fixed random seed (42) for reproducible results
- November and December data includes a 25% seasonal boost
- Sales values are generated with a normal distribution around category baselines