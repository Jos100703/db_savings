# db_savings  
Reverse engineering of the Deutsche Bahn Navigator API  

# DISCLAIMER
This approach only works from German IP-Adresses

## Overview  
This project extracts train connection and pricing data directly from the Deutsche Bahn Navigator API.  
Given a DB search URL, it retrieves the available connections (including intermediate stops and prices) and outputs the results as a structured CSV.  

## Workflow  
**Input:** A DB search URL copied from the Bahn website or Navigator app.  
**Output:** A CSV file (`02_Output/Full_conn_stops.csv`) containing:  
- Departure and arrival stations  
- Departure/arrival times  
- Intermediate stops  
- Duration and transfer information  
- Price details  

## Usage Instructions  

1. **Select a connection to analyze**  
   - Go to the [DB Navigator website](https://www.bahn.de) and search for a route.  
   - Copy the resulting URL from your browser’s address bar (see example screenshot below).  
   - Paste this URL into the file `input_url.txt`.  

   <img width="2044" height="1496" alt="DB Navigator screenshot" src="https://github.com/user-attachments/assets/cde668f8-c83c-4eba-8d2c-94a3b435789b" />

2. **Run the processing script**  
   ```bash
   python 01_Processing/main.py
   ```
3. **Retrieve the results**
   The parsed connections will be available as a CSV in:
   ```bash
   02_Output/Full_conn_stops.csv
   ```
# Notes
- Only the first few available connections (and their corresponding prices) are extracted for efficiency.
- The project is designed for personal research and analysis of DB pricing; it is not affiliated with or supported by Deutsche Bahn.
