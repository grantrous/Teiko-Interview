# Streamlit CSV Database Application

This project is a Streamlit application that allows users to upload a CSV file, initialize a SQLite database from a relational schema, and interact with the data by adding or removing samples.

## Project Structure

```
streamlit-csv-db-app
├── src
│   ├── app.py          # Main entry point for the Streamlit application
│   ├── db.py           # Database management and operations
│   ├── utils.py        # Utility functions for data processing
│   └── schema.sql      # SQL schema for the SQLite database
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Features

- Upload a CSV file to load data into the database.
- View the data stored in the SQLite database.
- Add new samples to the database.
- Remove existing samples from the database.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/streamlit-csv-db-app.git
   cd streamlit-csv-db-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run src/app.py
   ```

## Usage Guidelines

- After running the application, navigate to the provided local URL in your web browser.
- Use the interface to upload a CSV file and interact with the database.
- Follow the prompts to add or remove samples as needed.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.