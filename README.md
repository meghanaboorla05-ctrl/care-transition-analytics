# Care Transition Efficiency & Placement Outcome Analytics

## Project Overview
This project analyzes aggregate reported data related to CBP custody, HHS care, transfers, and discharges. It uses Python and Streamlit to present the data through interactive graphs and summary statistics.

## Objectives
- Explore reported counts over time.
- Visualize selected numerical columns using interactive graphs.
- Review summary statistics and missing values.
- Provide a simple dashboard for data exploration.

## Technologies Used
- Python
- Pandas
- Streamlit
- Plotly

## Project Files
- `app.py` — Streamlit dashboard and interactive visualizations.
- `analysis.py` — Dataset inspection and analysis.
- `requirements.txt` — Required Python packages.
- `data_inspection.txt` — Dataset inspection output.

## How to Run the Project

1. Install Python.
2. Install the required packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

4. Open the local URL displayed in the terminal, usually `http://localhost:8501`.

Make sure the CSV dataset is available in the `data` folder, or upload it through the dashboard.

## Limitations
The dashboard explores aggregate reported counts. It does not establish individual case processing times, causation, or the existence of a backlog without additional supporting data.

## Author
Meghana Boorla
