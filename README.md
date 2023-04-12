This is a simple Streamlit application for anonymizing and validating CSV files. Users can upload a CSV file, select the columns to be anonymized, and download the resulting file. The application also sends an email notification containing the download URL of the anonymized file.

Features
	• Upload CSV files
	• Validate CSV data
	• Anonymize selected columns using SHA-256 hashing
	• Send email notifications with download links to anonymized files
	• Store anonymized files in Azure Blob Storage

Prerequisites
Before you can run the application, you will need to have the following:

	• Python 3.7 or newer
	• An Azure Blob Storage account and container for storing anonymized files
	• A SendGrid account for sending email notifications

Installation

Clone the repository:

	• git clone https://github.com/your_username/csv-anonymization-validation.git

Change to the project directory:
	
	• cd csv-anonymization-validation

Install the required Python packages:

	• pip install -r requirements.txt

Configure the required environment variables in the .env file:

	• AZURE_CONNECTION_STRING=your_azure_connection_string
	• STORAGE_ACCOUNT_KEY=your_storage_account_key
	• AZURE_CONTAINER_NAME=your_azure_container_name
	• STORAGE_ACCOUNT_NAME=your_storage_account_name
	• SENDGRID_API_KEY=your_sendgrid_api_key
	• SENDER_EMAIL=your_sender_email
	• RECIPIENT_EMAIL=your_recipient_email
	• USERNAME=your_username
	• PASSWORD=your_password
	
Replace the placeholders with your own credentials and settings.

Run the application:

	• streamlit run app.py
	• Open a web browser and navigate to the URL provided by Streamlit, usually http://localhost:8501.

Usage
	• Log in using the username and password specified in the .env file.
	• Upload a CSV file using the file uploader.
	• The application will display a preview of the uploaded data and the file details.
	• Select the columns you want to anonymize from the multi-select dropdown menu.
	• Click the "Submit" button.
	• The application will anonymize the selected columns, save the anonymized data to a new CSV file, upload the file to Azure Blob Storage, and generate a download URL.
	• The application will send an email notification to the recipient email address specified in the .env file, containing the download URL of the anonymized file.
	• Download the anonymized file using the provided download link.
