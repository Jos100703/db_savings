# Project Documentation 
(AI-generated, but roughly read through and validated)

This document provides an overview of the project structure, its components, and the data flow from input to output.

## Project Structure

The project is organized into several directories, each with a specific purpose.

```
.
├── 00_Input/
│   └── input_url.txt
├── 01_Processing/
│   └── 00_main.py
├── 02_Output/
│   ├── Full_conn_stops.csv
│   └── Sample_results_for_testing.json
├── DbReq/
│   ├── Configs/
│   │   ├── base_params.json
│   │   └── headers.json
│   ├── __init__.py
│   ├── DbReq.py
│   └── utils.py
└── README.md
```

### Folders

-   **`00_Input/`**: Contains the input data for the application.
    -   `input_url.txt`: A text file containing a single URL of a Deutsche Bahn (DB) train connection search result. This URL is the starting point for the data retrieval process.
-   **`01_Processing/`**: Holds the main script that orchestrates the entire workflow.
    -   `00_main.py`: The entry point of the application. It reads the input URL, utilizes the `DbReq` library to fetch and parse the data, and writes the final output.
-   **`02_Output/`**: This directory stores the results of the data processing.
    -   `Full_conn_stops.csv`: The final, processed data in CSV format. It contains a detailed list of all stops for the connections found from the input URL.
    -   `Sample_results_for_testing.json`: A sample JSON response from the DB API, likely used for development and testing purposes.
-   **`DbReq/`**: A Python package designed to interact with the Deutsche Bahn API.
    -   **`Configs/`**: Contains JSON configuration files for making API requests.
        -   `base_params.json`: Default parameters for the API query.
        -   `headers.json`: HTTP headers to be sent with the request.

### Key Files

-   **`01_Processing/00_main.py`**: This is the main driver script. It performs the following steps:
    1.  Reads the URL from `00_Input/input_url.txt`.
    2.  Instantiates the `DbReq` object using the URL.
    3.  Calls methods to fetch the connection data from the DB API.
    4.  Parses the hierarchical JSON response into structured objects.
    5.  Flattens the parsed data into a list of stops.
    6.  Converts the list into a pandas DataFrame.
    7.  Saves the DataFrame to `02_Output/Full_conn_stops.csv`.

-   **`DbReq/DbReq.py`**: The core of the `DbReq` library.
    -   **`DbReq` class**: Manages the API request. It can be initialized from a URL (`from_input_link`), builds the request payload, sends it to the DB server, and retrieves the response.
    -   **`DbParser` class**: A base class for parsing different parts of the API's JSON response. It provides a generic mechanism for extracting nested data.
    -   **`DbCon`**, **`DbConAbs`**, **`DbConAbsStop`**: These classes inherit from `DbParser` and are specialized for parsing specific levels of the data hierarchy:
        -   `DbCon`: Parses a whole trip/connection.
        -   `DbConAbs`: Parses a section of a trip (e.g., a single train journey between two points).
        -   `DbConAbsStop`: Parses a single stop within a journey section.

-   **`DbReq/utils.py`**: Contains utility functions used by the library.
    -   `parse_hafas_lid`: A helper function to decode the proprietary `LID` (Location ID) format used by HAFAS (the system behind many European train schedules) into a human-readable dictionary containing information like station name, coordinates, and external IDs.
    -   `get_from_list`: A flexible utility to extract values from nested dictionaries based on a list of keys.

## Data Flow

The application follows a linear data flow:

1.  **Input**: The process begins with a URL from `input_url.txt`. This URL represents a user's search for a train connection on the Deutsche Bahn website.

2.  **Fetch**: `00_main.py` uses the `DbReq` class to send an HTTP POST request to the DB API (`https://www.bahn.de/web/api/angebote/fahrplan`). The request is constructed using the station IDs from the input URL and configuration from `DbReq/Configs/`.

3.  **Parse**: The API returns a complex, nested JSON object. The script iteratively parses this object:
    -   The top-level `verbindungen` array is parsed into a list of `DbCon` objects.
    -   Each `DbCon` object's `verbindungsAbschnitte` are parsed into `DbConAbs` objects.
    -   Each `DbConAbs` object's `halte` are parsed into `DbConAbsStop` objects.
    -   During parsing, relevant parent information (like `tripId` or cost) is inherited by the child objects.

4.  **Structure**: The deeply nested information is flattened. The attributes of each `DbConAbsStop` object, which now contain information about the stop, the section, and the overall trip, are collected into a simple list of dictionaries.

5.  **Output**: This list is converted into a pandas DataFrame and then exported to `Full_conn_stops.csv`, providing a clean, tabular representation of all the stops in the journey.
