# FY2024 Campaign Analytics Dashboard

A beautiful, interactive Streamlit dashboard for analyzing Meta campaign performance and generating actionable insights.

## 🚀 Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the dashboard:**
```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

## 📊 Dashboard Features

### 🏠 Executive Dashboard
- Key performance metrics at a glance
- Lead volume trends by month
- CPL trends
- Program performance summary
- Visual insights and recommendations

### 📈 Seasonality Analysis
- Monthly lead volume patterns
- CPL trends by month
- Performance heatmap
- Peak and low season identification
- Seasonal budget recommendations

### 🎯 Conversion Rates
- Click-to-submit conversion rates
- Landing page view-to-submit rates
- Program-level conversion analysis
- Conversion funnel visualization
- Optimization opportunities

### 💼 Program Performance
- CPL vs Conversion rate scatter plot
- Program categorization (underperforming/well-performing)
- Detailed performance table
- Actionable insights for each program

### 🔮 Predictive Insights
- What-if scenario analysis
- ROI optimization models
- Budget scaling recommendations
- Forecast visualizations

### 💡 Recommendations
- Strategic recommendations
- Expected impact metrics
- Action items timeline
- Implementation roadmap

## 🎨 Design Features

- **Beautiful UI:** Modern gradient cards and color schemes
- **Interactive Charts:** Plotly visualizations with hover details
- **Story-Driven:** Data tells a clear narrative
- **Responsive:** Works on desktop and tablet
- **Professional:** Client-ready presentation quality

## 📁 Required Files

The dashboard expects the following data files in `analysis_results/`:
- `monthly_stats.csv`
- `program_performance.csv`
- `program_click_rates.csv`
- `program_lpv_rates.csv`
- `program_roi.csv`
- `monthly_trends.csv`
- `what_if_scenarios.csv` (optional, for predictive insights)
- `roi_optimization.csv` (optional, for predictive insights)

## 🔧 Customization

You can customize the dashboard by:
- Modifying color schemes in the CSS section
- Adding new pages in the navigation
- Adjusting chart layouts and styles
- Adding new metrics or visualizations

## 📝 Notes

- The dashboard uses cached data loading for performance
- All charts are interactive and exportable
- Data updates automatically when CSV files are refreshed
- The dashboard is optimized for wide-screen displays

## 🆘 Troubleshooting

**Dashboard won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that all required CSV files exist in `analysis_results/`

**Charts not displaying:**
- Verify CSV files are properly formatted
- Check for missing data columns
- Ensure data files are in the correct directory

**Performance issues:**
- Clear Streamlit cache: `streamlit cache clear`
- Check file sizes of CSV data files

---

*Dashboard created: December 2024*






