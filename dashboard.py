import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="FY2024 Campaign Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    monthly_stats = pd.read_csv('analysis_results/monthly_stats.csv')
    program_performance = pd.read_csv('analysis_results/program_performance.csv')
    program_click_rates = pd.read_csv('analysis_results/program_click_rates.csv')
    program_lpv_rates = pd.read_csv('analysis_results/program_lpv_rates.csv')
    program_roi = pd.read_csv('analysis_results/program_roi.csv')
    monthly_trends = pd.read_csv('analysis_results/monthly_trends.csv')
    
    # Try to load predictive data if available
    try:
        what_if = pd.read_csv('analysis_results/what_if_scenarios.csv')
        roi_optimization = pd.read_csv('analysis_results/roi_optimization.csv')
    except:
        what_if = None
        roi_optimization = None
    
    return {
        'monthly_stats': monthly_stats,
        'program_performance': program_performance,
        'program_click_rates': program_click_rates,
        'program_lpv_rates': program_lpv_rates,
        'program_roi': program_roi,
        'monthly_trends': monthly_trends,
        'what_if': what_if,
        'roi_optimization': roi_optimization
    }

data = load_data()

# Sidebar navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Executive Dashboard", "📈 Seasonality Analysis", "🎯 Conversion Rates", 
     "💼 Program Performance", "🔮 Predictive Insights", "💡 Recommendations"]
)

# ============================================================================
# EXECUTIVE DASHBOARD
# ============================================================================
if page == "🏠 Executive Dashboard":
    st.markdown('<h1 class="main-header">FY2024 Campaign Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Lead Generation Performance Analysis | July 2024 - June 2025</p>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_leads = data['program_performance']['Results'].sum()
    total_spend = data['program_performance']['Amount spent (USD)'].sum()
    avg_cpl = data['program_performance'][data['program_performance']['CPL'].notna()]['CPL'].mean()
    total_clicks = data['program_click_rates']['Link clicks'].sum()
    total_submits = data['program_click_rates']['Results'].sum()
    click_rate = (total_submits / total_clicks * 100) if total_clicks > 0 else 0
    
    with col1:
        st.metric("Total Leads", f"{total_leads:,.0f}", "619 RFI Submissions")
    with col2:
        st.metric("Total Spend", f"${total_spend:,.0f}", "$209,548")
    with col3:
        st.metric("Average CPL", f"${avg_cpl:.2f}", "Cost Per Lead")
    with col4:
        st.metric("Click-to-Submit Rate", f"{click_rate:.2f}%", "Conversion Rate")
    
    st.markdown("---")
    
    # Story Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Performance Overview")
        
        # Lead volume by month
        fig_leads = px.bar(
            data['monthly_stats'],
            x='Month_Name',
            y='Results',
            title='Lead Volume by Month',
            color='Results',
            color_continuous_scale='Blues',
            labels={'Results': 'Leads', 'Month_Name': 'Month'}
        )
        fig_leads.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_leads, use_container_width=True)
        
        # CPL by month
        fig_cpl = px.line(
            data['monthly_stats'][data['monthly_stats']['CPL'].notna()],
            x='Month_Name',
            y='CPL',
            title='Cost Per Lead Trend',
            markers=True,
            color_discrete_sequence=['#ff6b6b']
        )
        fig_cpl.update_layout(height=300)
        st.plotly_chart(fig_cpl, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Key Insights")
        
        # Find peak month
        peak_month = data['monthly_stats'].loc[data['monthly_stats']['Results'].idxmax(), 'Month_Name']
        peak_leads = data['monthly_stats']['Results'].max()
        
        st.markdown(f"""
        <div class="insight-box">
            <h3>Peak Performance</h3>
            <p><strong>{peak_month}</strong> generated the most leads ({peak_leads:.0f})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Find best CPL month
        best_cpl_month = data['monthly_stats'][data['monthly_stats']['CPL'].notna()].loc[
            data['monthly_stats'][data['monthly_stats']['CPL'].notna()]['CPL'].idxmin(), 'Month_Name']
        best_cpl = data['monthly_stats'][data['monthly_stats']['CPL'].notna()]['CPL'].min()
        
        st.markdown(f"""
        <div class="recommendation-box">
            <h3>Best CPL</h3>
            <p><strong>{best_cpl_month}</strong> had lowest CPL (${best_cpl:.2f})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Top program
        top_program = data['program_performance'].loc[data['program_performance']['Results'].idxmax()]
        st.markdown(f"""
        <div class="insight-box">
            <h3>Top Program</h3>
            <p><strong>{top_program['Program'][:30]}...</strong><br>
            {top_program['Results']:.0f} leads</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Program Performance Summary
    st.markdown("---")
    st.subheader("💼 Program Performance Summary")
    
    program_summary = data['program_performance'][['Program', 'Results', 'CPL', 'Amount spent (USD)']].copy()
    program_summary = program_summary.sort_values('Results', ascending=False)
    
    fig_programs = px.bar(
        program_summary,
        x='Program',
        y='Results',
        color='CPL',
        title='Lead Generation by Program',
        color_continuous_scale='RdYlGn_r',
        labels={'Results': 'Leads', 'CPL': 'CPL ($)'}
    )
    fig_programs.update_xaxes(tickangle=-45)
    fig_programs.update_layout(height=500)
    st.plotly_chart(fig_programs, use_container_width=True)

# ============================================================================
# SEASONALITY ANALYSIS
# ============================================================================
elif page == "📈 Seasonality Analysis":
    st.markdown('<h1 class="main-header">Seasonality Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Understanding Monthly Patterns in Lead Volume and CPL</p>', unsafe_allow_html=True)
    
    # Dual axis chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Lead volume bars
    fig.add_trace(
        go.Bar(
            x=data['monthly_stats']['Month_Name'],
            y=data['monthly_stats']['Results'],
            name='Lead Volume',
            marker_color='#1f77b4',
            opacity=0.8
        ),
        secondary_y=False,
    )
    
    # CPL line
    cpl_data = data['monthly_stats'][data['monthly_stats']['CPL'].notna()]
    fig.add_trace(
        go.Scatter(
            x=cpl_data['Month_Name'],
            y=cpl_data['CPL'],
            name='CPL',
            mode='lines+markers',
            line=dict(color='#ff6b6b', width=3),
            marker=dict(size=10)
        ),
        secondary_y=True,
    )
    
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Lead Volume", secondary_y=False)
    fig.update_yaxes(title_text="CPL ($)", secondary_y=True)
    fig.update_layout(
        title="Lead Volume vs. Cost Per Lead by Month",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Key Findings")
        
        peak_month = data['monthly_stats'].loc[data['monthly_stats']['Results'].idxmax(), 'Month_Name']
        peak_value = data['monthly_stats']['Results'].max()
        low_month = data['monthly_stats'].loc[data['monthly_stats']['Results'].idxmin(), 'Month_Name']
        low_value = data['monthly_stats']['Results'].min()
        
        st.info(f"**Peak Lead Month:** {peak_month} with {peak_value:.0f} leads")
        st.info(f"**Lowest Lead Month:** {low_month} with {low_value:.0f} leads")
        
        high_cpl_month = cpl_data.loc[cpl_data['CPL'].idxmax(), 'Month_Name']
        high_cpl_value = cpl_data['CPL'].max()
        low_cpl_month = cpl_data.loc[cpl_data['CPL'].idxmin(), 'Month_Name']
        low_cpl_value = cpl_data['CPL'].min()
        
        st.warning(f"**Highest CPL:** {high_cpl_month} at ${high_cpl_value:.2f}")
        st.success(f"**Lowest CPL:** {low_cpl_month} at ${low_cpl_value:.2f}")
    
    with col2:
        st.markdown("### 💡 Recommendations")
        st.markdown("""
        - **Increase budget allocation** to May-June (peak months)
        - **Optimize campaigns** during high CPL periods (May-June)
        - **Test increased spend** in low CPL months (July, March) for efficiency
        - **Plan seasonal budget** with 40-50% allocated to Q4
        """)
    
    # Heatmap
    st.markdown("---")
    st.subheader("📅 Monthly Performance Heatmap")
    
    heatmap_data = data['monthly_stats'][['Month_Name', 'Results', 'CPL']].copy()
    heatmap_data['Results_Normalized'] = (heatmap_data['Results'] / heatmap_data['Results'].max() * 100)
    heatmap_data['CPL_Normalized'] = (heatmap_data['CPL'] / heatmap_data['CPL'].max() * 100)
    
    fig_heatmap = px.imshow(
        heatmap_data[['Results_Normalized', 'CPL_Normalized']].T,
        labels=dict(x="Month", y="Metric", color="Normalized Value (%)"),
        x=heatmap_data['Month_Name'],
        y=['Lead Volume', 'CPL'],
        color_continuous_scale='RdYlGn_r',
        aspect="auto"
    )
    fig_heatmap.update_layout(height=300)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ============================================================================
# CONVERSION RATES
# ============================================================================
elif page == "🎯 Conversion Rates":
    st.markdown('<h1 class="main-header">Conversion Rate Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Click-to-Submit and Landing Page View-to-Submit Rates</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Overall metrics
    total_clicks = data['program_click_rates']['Link clicks'].sum()
    total_submits = data['program_click_rates']['Results'].sum()
    click_rate = (total_submits / total_clicks * 100) if total_clicks > 0 else 0
    
    total_lpv = data['program_lpv_rates']['Landing page views'].sum()
    lpv_rate = (total_submits / total_lpv * 100) if total_lpv > 0 else 0
    
    with col1:
        st.metric("Click-to-Submit Rate", f"{click_rate:.2f}%", 
                 f"{total_submits:,.0f} submits from {total_clicks:,.0f} clicks")
    
    with col2:
        st.metric("LPV-to-Submit Rate", f"{lpv_rate:.2f}%",
                 f"{total_submits:,.0f} submits from {total_lpv:,.0f} LPVs")
    
    st.markdown("---")
    
    # Comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Click-to-Submit Rate by Program")
        click_data = data['program_click_rates'].sort_values('Conversion_Rate', ascending=True)
        click_data = click_data[click_data['Results'] > 0]  # Filter out zero results
        
        fig_click = px.bar(
            click_data,
            x='Conversion_Rate',
            y='Program',
            orientation='h',
            color='Conversion_Rate',
            color_continuous_scale='Greens',
            labels={'Conversion_Rate': 'Conversion Rate (%)', 'Program': 'Program'}
        )
        fig_click.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_click, use_container_width=True)
    
    with col2:
        st.subheader("LPV-to-Submit Rate by Program")
        lpv_data = data['program_lpv_rates'].sort_values('Conversion_Rate', ascending=True)
        lpv_data = lpv_data[lpv_data['Results'] > 0]  # Filter out zero results
        
        fig_lpv = px.bar(
            lpv_data,
            x='Conversion_Rate',
            y='Program',
            orientation='h',
            color='Conversion_Rate',
            color_continuous_scale='Blues',
            labels={'Conversion_Rate': 'Conversion Rate (%)', 'Program': 'Program'}
        )
        fig_lpv.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_lpv, use_container_width=True)
    
    # Insight
    st.markdown("---")
    st.info(f"""
    **Key Insight:** Landing Page View-to-Submit rate ({lpv_rate:.2f}%) is nearly **double** the Click-to-Submit rate ({click_rate:.2f}%). 
    This indicates that users who reach the landing page are significantly more qualified and likely to convert.
    **Recommendation:** Focus on improving ad-to-landing page alignment to increase click-to-LPV rate.
    """)
    
    # Funnel visualization
    st.subheader("📊 Conversion Funnel")
    
    # Get impressions from program_performance
    total_impressions = data['program_performance']['Impressions'].sum() if 'Impressions' in data['program_performance'].columns else 0
    
    funnel_data = pd.DataFrame({
        'Stage': ['Impressions', 'Link Clicks', 'Landing Page Views', 'RFI Submits'],
        'Count': [
            total_impressions,
            total_clicks,
            total_lpv,
            total_submits
        ]
    })
    
    # Calculate percentages relative to initial stage (Impressions)
    if funnel_data['Count'].iloc[0] > 0:
        funnel_data['Percentage'] = (funnel_data['Count'] / funnel_data['Count'].iloc[0] * 100).round(2)
    else:
        funnel_data['Percentage'] = 0
    
    # Calculate conversion rates between stages
    conversion_rates = [0.0]  # First stage has no previous stage
    for i in range(1, len(funnel_data)):
        if funnel_data['Count'].iloc[i-1] > 0:
            rate = (funnel_data['Count'].iloc[i] / funnel_data['Count'].iloc[i-1] * 100).round(2)
        else:
            rate = 0.0
        conversion_rates.append(rate)
    funnel_data['Conversion_Rate'] = conversion_rates
    
    # Create custom text labels showing count and percentage
    funnel_text = []
    for idx, row in funnel_data.iterrows():
        if idx == 0:
            text = f"{row['Count']:,.0f}<br>({row['Percentage']:.1f}%)"
        else:
            text = f"{row['Count']:,.0f}<br>({row['Percentage']:.1f}% of initial)<br>{row['Conversion_Rate']:.2f}% conversion"
        funnel_text.append(text)
    
    # Create funnel chart with custom text
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        text=funnel_text,
        textposition="inside",
        textfont=dict(size=12, color="white"),
        marker=dict(
            color=funnel_data['Percentage'],
            colorscale='Viridis',
            line=dict(width=4, color="white"),
            showscale=True,
            colorbar=dict(title="% of Initial")
        )
    ))
    fig_funnel.update_layout(
        title='Conversion Funnel - Shows progression from Impressions to Submissions',
        height=500,
        showlegend=False,
        font=dict(size=12)
    )
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Display conversion rates table
    st.markdown("**Conversion Rates Between Stages:**")
    conversion_table = pd.DataFrame({
        'From Stage': ['Impressions → Clicks', 'Clicks → Landing Page Views', 'Landing Page Views → Submits'],
        'Conversion Rate': [
            f"{funnel_data.loc[1, 'Conversion_Rate']:.2f}%",
            f"{funnel_data.loc[2, 'Conversion_Rate']:.2f}%",
            f"{funnel_data.loc[3, 'Conversion_Rate']:.2f}%"
        ]
    })
    st.dataframe(conversion_table, use_container_width=True, hide_index=True)

# ============================================================================
# PROGRAM PERFORMANCE
# ============================================================================
elif page == "💼 Program Performance":
    st.markdown('<h1 class="main-header">Program Performance Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comprehensive Performance Metrics by Program</p>', unsafe_allow_html=True)
    
    # Performance scatter plot
    perf_data = data['program_performance'].copy()
    perf_data = perf_data[perf_data['CPL'].notna() & (perf_data['Results'] > 0)]
    
    fig_scatter = px.scatter(
        perf_data,
        x='Click_to_Submit_Rate',
        y='CPL',
        size='Results',
        color='Results',
        hover_name='Program',
        title='Program Performance: CPL vs Conversion Rate',
        color_continuous_scale='RdYlGn_r',
        labels={
            'Click_to_Submit_Rate': 'Click-to-Submit Rate (%)',
            'CPL': 'Cost Per Lead ($)',
            'Results': 'Total Leads'
        },
        size_max=60
    )
    
    # Add median lines
    median_cpl = perf_data['CPL'].median()
    median_conv = perf_data['Click_to_Submit_Rate'].median()
    
    fig_scatter.add_hline(y=median_cpl, line_dash="dash", line_color="gray", 
                         annotation_text=f"Median CPL: ${median_cpl:.2f}")
    fig_scatter.add_vline(x=median_conv, line_dash="dash", line_color="gray",
                         annotation_text=f"Median Conv: {median_conv:.2f}%")
    
    fig_scatter.update_layout(height=600)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Program details table
    st.subheader("📋 Detailed Program Performance")
    
    display_cols = ['Program', 'Amount spent (USD)', 'Results', 'CPL', 
                    'Click_to_Submit_Rate', 'Category']
    display_data = data['program_performance'][display_cols].copy()
    display_data = display_data.sort_values('CPL', ascending=False)
    display_data['Amount spent (USD)'] = display_data['Amount spent (USD)'].apply(lambda x: f"${x:,.2f}")
    display_data['CPL'] = display_data['CPL'].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
    display_data['Click_to_Submit_Rate'] = display_data['Click_to_Submit_Rate'].apply(
        lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A")
    
    st.dataframe(display_data, use_container_width=True, hide_index=True)
    
    # Underperforming programs alert
    st.markdown("---")
    underperforming = data['program_performance'][
        data['program_performance']['Category'].isin(['Underperforming', 'High CPL', 'Low Conversion', 'No Leads'])
    ]
    
    if len(underperforming) > 0:
        st.warning(f"⚠️ **{len(underperforming)} Programs Requiring Attention**")
        for idx, row in underperforming.iterrows():
            st.write(f"- **{row['Program']}**: {row['Category']} | CPL: ${row['CPL']:.2f}" if pd.notna(row['CPL']) else f"- **{row['Program']}**: {row['Category']}")

# ============================================================================
# PREDICTIVE INSIGHTS
# ============================================================================
elif page == "🔮 Predictive Insights":
    st.markdown('<h1 class="main-header">Predictive & Prescriptive Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Forecasts and Optimization Recommendations for FY2025</p>', unsafe_allow_html=True)
    
    if data['what_if'] is not None and data['roi_optimization'] is not None:
        # What-if scenarios
        st.subheader("🎯 What-If Scenario Analysis")
        
        fig_scenarios = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Predicted Lead Volume', 'Average CPL'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        fig_scenarios.add_trace(
            go.Bar(
                x=data['what_if']['Scenario'],
                y=data['what_if']['Total_Leads'],
                name='Leads',
                marker_color='#1f77b4',
                text=data['what_if']['Total_Leads'].round(0),
                textposition='outside'
            ),
            row=1, col=1
        )
        
        fig_scenarios.add_trace(
            go.Bar(
                x=data['what_if']['Scenario'],
                y=data['what_if']['Avg_CPL'],
                name='CPL',
                marker_color='#ff6b6b',
                text=data['what_if']['Avg_CPL'].round(2),
                textposition='outside'
            ),
            row=1, col=2
        )
        
        fig_scenarios.update_xaxes(tickangle=-15)
        fig_scenarios.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_scenarios, use_container_width=True)
        
        # Best scenario highlight
        best_scenario = data['what_if'].loc[data['what_if']['Total_Leads'].idxmax()]
        st.success(f"""
        **Recommended Scenario:** {best_scenario['Scenario']}
        - Predicted Leads: {best_scenario['Total_Leads']:.0f} (+{best_scenario['Improvement_Leads']:.1f}%)
        - Average CPL: ${best_scenario['Avg_CPL']:.2f} ({best_scenario['Improvement_CPL']:.1f}% improvement)
        - Budget: ${best_scenario['Total_Budget']:,.0f}
        """)
        
        # ROI Optimization
        st.markdown("---")
        st.subheader("💰 ROI Optimization Model")
        
        fig_roi = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Budget vs Lead Volume', 'Budget vs ROI'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig_roi.add_trace(
            go.Scatter(
                x=data['roi_optimization']['Total_Budget'],
                y=data['roi_optimization']['Total_Leads'],
                mode='lines+markers',
                name='Leads',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=10)
            ),
            row=1, col=1
        )
        
        fig_roi.add_trace(
            go.Scatter(
                x=data['roi_optimization']['Total_Budget'],
                y=data['roi_optimization']['ROI'],
                mode='lines+markers',
                name='ROI',
                line=dict(color='#00cc96', width=3),
                marker=dict(size=10)
            ),
            row=1, col=2
        )
        
        fig_roi.update_xaxes(title_text="Budget ($)", row=1, col=1)
        fig_roi.update_xaxes(title_text="Budget ($)", row=1, col=2)
        fig_roi.update_yaxes(title_text="Total Leads", row=1, col=1)
        fig_roi.update_yaxes(title_text="ROI", row=1, col=2)
        fig_roi.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_roi, use_container_width=True)
        
        optimal_budget_min = data['roi_optimization']['Total_Budget'].min()
        optimal_budget_max = data['roi_optimization']['Total_Budget'].max()
        st.info(f"**Optimal Budget Range:** ${optimal_budget_min:,.0f} - ${optimal_budget_max:,.0f}")
    else:
        st.info("Predictive analysis data not available. Run predictive_prescriptive_analysis.py to generate forecasts.")

# ============================================================================
# RECOMMENDATIONS
# ============================================================================
elif page == "💡 Recommendations":
    st.markdown('<h1 class="main-header">Strategic Recommendations</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Actionable Insights for FY2025 Campaign Optimization</p>', unsafe_allow_html=True)
    
    # Current vs Predicted
    current_leads = data['program_performance']['Results'].sum()
    current_spend = data['program_performance']['Amount spent (USD)'].sum()
    current_cpl = data['program_performance'][data['program_performance']['CPL'].notna()]['CPL'].mean()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Leads", f"{current_leads:,.0f}", "619 RFI Submissions")
    with col2:
        st.metric("Current Spend", f"${current_spend:,.0f}", "$209,548")
    with col3:
        st.metric("Current CPL", f"${current_cpl:.2f}", "Average Cost Per Lead")
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("🎯 Key Recommendations")
    
    rec1, rec2 = st.columns(2)
    
    with rec1:
        st.markdown("""
        ### 1. Optimal Budget Allocation
        - **Implement balanced approach:** $162,531 budget
        - **Expected leads:** 1,890 (+205% vs current)
        - **Average CPL:** $85.99 (10% improvement)
        
        ### 2. Seasonal Planning
        - **Q4 allocation:** 40-50% of annual budget (Apr-Jun)
        - **Peak months:** Increase May-June spend by 20-30%
        - **Low season:** Optimize campaigns in Jul-Sep
        """)
    
    with rec2:
        st.markdown("""
        ### 3. Program Optimization
        - **Pause underperformers:** Masters of Space Operations (0 leads)
        - **Increase top performers:** Military, BSE, MBA Airlines
        - **Optimize high CPL:** MS in Engineering Management
        
        ### 4. Conversion Improvement
        - **Landing page optimization:** Focus on programs <3.5% LPV conversion
        - **Ad-to-LPV alignment:** Improve click quality
        - **A/B testing:** Test new creative and landing pages
        """)
    
    st.markdown("---")
    
    # Expected Impact
    st.subheader("📈 Expected Impact")
    
    impact_data = pd.DataFrame({
        'Metric': ['Lead Volume', 'Average CPL', 'Total Budget', 'ROI'],
        'Current': [619, 95.77, 209548, 0.0030],
        'Predicted': [1890, 85.99, 162531, 0.0116],
        'Improvement': ['+205%', '-10%', '-22%', '+287%']
    })
    
    fig_impact = go.Figure()
    
    fig_impact.add_trace(go.Bar(
        name='Current',
        x=impact_data['Metric'],
        y=impact_data['Current'],
        marker_color='#ff6b6b',
        text=impact_data['Current'],
        textposition='outside'
    ))
    
    fig_impact.add_trace(go.Bar(
        name='Predicted',
        x=impact_data['Metric'],
        y=impact_data['Predicted'],
        marker_color='#00cc96',
        text=impact_data['Predicted'],
        textposition='outside'
    ))
    
    fig_impact.update_layout(
        title='Current vs Predicted Performance',
        barmode='group',
        height=500,
        yaxis_title='Value'
    )
    
    st.plotly_chart(fig_impact, use_container_width=True)
    
    # Action Items
    st.markdown("---")
    st.subheader("✅ Action Items")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Immediate (Q1 2025):**
        - ✅ Implement optimal budget allocation
        - ✅ Pause underperforming programs
        - ✅ Reallocate budget to top performers
        - ✅ Set up engagement-based budgeting
        """)
    
    with col2:
        st.markdown("""
        **Short-Term (Q2-Q3 2025):**
        - ✅ Test MS in Management scaling
        - ✅ Optimize MSEM campaign strategy
        - ✅ Implement landing page A/B testing
        - ✅ Monitor performance vs predictions
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>FY2024 Campaign Analytics Dashboard | Generated: December 2024</p>
    <p>Data Period: July 2024 - June 2025</p>
</div>
""", unsafe_allow_html=True)

