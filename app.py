import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Set page config
st.set_page_config(
    page_title="WACC Dashboard",
    page_icon="📊",
    layout="wide"
)

# Function to load and prepare data
@st.cache_data
def load_data():
    try:
        # Look for Excel files in the data directory
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        excel_files = [f for f in os.listdir(data_dir) if f.endswith('.xlsx')]
        
        if not excel_files:
            st.error("No Excel files found in the data directory")
            return None
            
        # Use the first Excel file found
        file_path = os.path.join(data_dir, excel_files[0])
        df = pd.read_excel(file_path)
        
        # Ensure the first column is treated as dates if it contains dates
        try:
            df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
        except:
            pass
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Load the data
df = load_data()

if df is not None:
    # Title
    st.title("WACC Analysis Dashboard")
    
    # Create a container for the most recent WACC value
    most_recent_container = st.container()
    with most_recent_container:
        st.markdown("### Most Recent WACC Value")
        
        try:
            most_recent_wacc = df.iloc[-1]  # Get the last row
            most_recent_date = df.iloc[-1, 0].strftime('%Y-%m-%d')
            st.markdown(f"As of {most_recent_date}")
            
            # Create three columns for better layout
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.metric(
                    label="Current WACC",
                    value=f"{most_recent_wacc.iloc[-1]:.4f}",  # Format to 4 decimal places without percentage
                )
            
            # If you have previous period data for comparison
            try:
                previous_wacc = df.iloc[-2].iloc[-1]
                delta = most_recent_wacc.iloc[-1] - previous_wacc
                with col2:
                    st.metric(
                        label="Change from Previous",
                        value=f"{delta:.4f}",
                        delta=f"{delta:.4f}",
                        delta_color="inverse"
                    )
            except:
                pass
            
        except Exception as e:
            st.warning("Could not display most recent WACC value. Please check data format.")
    
    st.markdown("---")  # Add a separator

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Overview", "Detailed Analysis", "Visualization"])
    
    with tab1:
        st.header("WACC Overview")
        
        # Create time series plot
        fig = go.Figure()
        
        # Add WACC values line
        fig.add_trace(
            go.Scatter(
                x=df.iloc[:, 0],  # First column assumed to be dates
                y=df.iloc[:, -1],  # Last column assumed to be WACC values
                name='WACC',
                line=dict(color='#1f77b4', width=2),
                mode='lines+markers'
            )
        )
        
        # Update layout
        fig.update_layout(
            title='WACC Time Series Overview',
            xaxis_title='Date',
            yaxis_title='WACC',
            hovermode='x unified',
            plot_bgcolor='white',
            showlegend=True,
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey'
            )
        )
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
        
        # Add summary statistics in a cleaner format
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Summary Statistics")
            summary_stats = pd.DataFrame({
                'Metric': ['Minimum', 'Maximum', 'Average', 'Std Dev'],
                'Value': [
                    f"{df.iloc[:, -1].min():.4f}",
                    f"{df.iloc[:, -1].max():.4f}",
                    f"{df.iloc[:, -1].mean():.4f}",
                    f"{df.iloc[:, -1].std():.4f}"
                ]
            })
            st.dataframe(summary_stats, hide_index=True)
        
    with tab2:
        st.header("Detailed Analysis")
        # Add interactive filters based on columns
        if len(df.columns) > 0:
            selected_columns = st.multiselect(
                "Select columns to display",
                options=df.columns.tolist(),
                default=df.columns.tolist()
            )
            st.dataframe(df[selected_columns])
            
    with tab3:
        st.header("WACC Visualization")
        # Create advanced visualizations
        try:
            # Year-over-Year comparison if dates are available
            if pd.api.types.is_datetime64_any_dtype(df.iloc[:, 0]):
                df['Year'] = df.iloc[:, 0].dt.year
                yearly_avg = df.groupby('Year').iloc[:, -1].mean().reset_index()
                
                fig = go.Figure()
                
                # Add yearly average bars
                fig.add_trace(
                    go.Bar(
                        x=yearly_avg['Year'],
                        y=yearly_avg.iloc[:, -1],
                        name='Yearly Average',
                        marker_color='#1f77b4'
                    )
                )
                
                fig.update_layout(
                    title='WACC Yearly Comparison',
                    xaxis_title='Year',
                    yaxis_title='Average WACC',
                    plot_bgcolor='white',
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.warning("Could not create advanced visualizations. Please check data structure.")

    # Sidebar
    st.sidebar.header("Dashboard Controls")
    st.sidebar.markdown("""
    ### About WACC
    WACC (Weighted Average Cost of Capital) represents the average cost a company 
    pays for its funding sources, including:
    - Cost of Equity
    - Cost of Debt
    - Capital Structure Weights
    """)

    # Add download capability
    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="wacc_data.csv",
        mime="text/csv"
    )

else:
    st.error("Unable to load the WACC data. Please check the data directory for Excel files.")

# Footer
st.markdown("---")
st.markdown("Dashboard created for WACC analysis. Contact support for assistance.")