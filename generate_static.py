import pandas as pd
import plotly.graph_objects as go
import json
import os
from datetime import datetime

def generate_static_data():
    # Load the data
    try:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        excel_files = [f for f in os.listdir(data_dir) if f.endswith('.xlsx')]
        
        if not excel_files:
            print("No Excel files found in the data directory")
            return None
            
        file_path = os.path.join(data_dir, excel_files[0])
        df = pd.read_excel(file_path)
        
        # Ensure the first column is treated as dates
        try:
            df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
        except:
            pass

        # Create the static data directory if it doesn't exist
        static_dir = os.path.join(os.path.dirname(__file__), "static", "data")
        os.makedirs(static_dir, exist_ok=True)

        # Generate JSON data for the dashboard
        dashboard_data = {
            "wacc_values": {
                "dates": df.iloc[:, 0].dt.strftime('%Y-%m-%d').tolist(),
                "values": df.iloc[:, -1].tolist()
            },
            "current_wacc": {
                "value": float(df.iloc[-1, -1]),
                "date": df.iloc[-1, 0].strftime('%Y-%m-%d'),
                "previous": float(df.iloc[-2, -1]) if len(df) > 1 else None
            },
            "summary_stats": {
                "minimum": float(df.iloc[:, -1].min()),
                "maximum": float(df.iloc[:, -1].max()),
                "average": float(df.iloc[:, -1].mean()),
                "std_dev": float(df.iloc[:, -1].std())
            },
            "yearly_data": {
                "years": sorted(df.iloc[:, 0].dt.year.unique().tolist()),
                "averages": [float(df[df.iloc[:, 0].dt.year == year].iloc[:, -1].mean()) 
                           for year in sorted(df.iloc[:, 0].dt.year.unique().tolist())]
            }
        }

        # Save the data as JSON
        with open(os.path.join(static_dir, 'dashboard_data.json'), 'w') as f:
            json.dump(dashboard_data, f)

        print("Static data generated successfully!")
        return True

    except Exception as e:
        print(f"Error generating static data: {e}")
        return None

if __name__ == "__main__":
    generate_static_data()