# WACC Dashboard

A Streamlit dashboard for Weighted Average Cost of Capital (WACC) analysis.

## Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/wacc_dashboard.git
cd wacc_dashboard
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Place your WACC data file in the `data` folder.

4. Run the dashboard:
```bash
streamlit run app.py
```

## Features

- Real-time WACC monitoring
- Historical trend analysis
- Summary statistics
- Detailed data view
- Data export capabilities

## Data Format

The dashboard expects an Excel file with the following structure:
- First column: Dates
- Last column: WACC values
- Additional columns will be available for detailed analysis

## Contributing

Feel free to open issues or submit pull requests.

## License

MIT License