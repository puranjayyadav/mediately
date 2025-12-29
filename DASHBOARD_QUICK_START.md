# 🚀 Dashboard Quick Start Guide

## Launch the Dashboard

### Option 1: Using the launcher (Windows)
Double-click `run_dashboard.bat`

### Option 2: Command line
```bash
streamlit run dashboard.py
```

### Option 3: Direct Python
```bash
python -m streamlit run dashboard.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## 📊 Dashboard Pages Overview

### 🏠 Executive Dashboard
**What it shows:**
- Key metrics at a glance (Total Leads, Spend, CPL, Conversion Rate)
- Lead volume trends by month
- CPL trends
- Program performance summary
- Visual insights and peak performance highlights

**Use it for:**
- Quick overview of campaign performance
- High-level insights for executives
- Identifying top-performing months and programs

---

### 📈 Seasonality Analysis
**What it shows:**
- Monthly lead volume vs CPL comparison
- Performance heatmap
- Peak and low season identification
- Seasonal recommendations

**Use it for:**
- Understanding seasonal patterns
- Budget planning by month
- Identifying optimization opportunities

---

### 🎯 Conversion Rates
**What it shows:**
- Click-to-submit conversion rates (overall and by program)
- Landing page view-to-submit rates
- Conversion funnel visualization
- Program-level conversion analysis

**Use it for:**
- Identifying conversion optimization opportunities
- Comparing program performance
- Understanding user journey

---

### 💼 Program Performance
**What it shows:**
- CPL vs Conversion rate scatter plot
- Program categorization
- Detailed performance table
- Underperforming program alerts

**Use it for:**
- Identifying programs needing attention
- Comparing program efficiency
- Making budget allocation decisions

---

### 🔮 Predictive Insights
**What it shows:**
- What-if scenario analysis
- ROI optimization models
- Budget scaling recommendations
- Forecast visualizations

**Use it for:**
- Planning FY2025 budget
- Evaluating different strategies
- Understanding ROI at different budget levels

---

### 💡 Recommendations
**What it shows:**
- Strategic recommendations
- Current vs predicted performance
- Expected impact metrics
- Action items timeline

**Use it for:**
- Understanding recommended actions
- Seeing expected improvements
- Planning implementation

---

## 🎨 Interactive Features

### Charts
- **Hover** over data points to see detailed values
- **Click and drag** to zoom into specific areas
- **Double-click** to reset zoom
- **Download** charts using the toolbar

### Navigation
- Use the **sidebar** to switch between pages
- Each page tells a different part of the story
- Data is consistent across all pages

### Responsive Design
- Works on desktop and tablet
- Optimized for wide screens
- Professional presentation quality

---

## 💡 Tips for Best Experience

1. **Start with Executive Dashboard** to get the big picture
2. **Explore Seasonality** to understand patterns
3. **Check Conversion Rates** to find optimization opportunities
4. **Review Program Performance** to identify issues
5. **Use Predictive Insights** for planning
6. **End with Recommendations** for action items

---

## 🔧 Troubleshooting

**Dashboard won't start:**
- Check Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Ensure you're in the correct directory

**Charts not showing:**
- Verify CSV files exist in `analysis_results/` folder
- Check file permissions
- Ensure data files are not corrupted

**Performance slow:**
- Close other browser tabs
- Clear browser cache
- Restart the dashboard

---

## 📱 Sharing the Dashboard

### Local Network
The dashboard runs on `localhost:8501` by default. To share:
1. Find your local IP address
2. Run: `streamlit run dashboard.py --server.address 0.0.0.0`
3. Share: `http://YOUR_IP:8501`

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

---

## 🎯 Key Metrics Explained

- **CPL (Cost Per Lead):** Average cost to acquire one lead
- **Click-to-Submit Rate:** Percentage of clicks that result in form submission
- **LPV-to-Submit Rate:** Percentage of landing page views that result in submission
- **ROI:** Return on investment (leads per dollar spent)

---

*Enjoy exploring your campaign data! 📊*






