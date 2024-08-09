import requests
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='nasdaq_scraping.log', filemode='w')

# Define headers
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Name': 'Theis Scheuer Jansen',
    'Email': 'Theisscheuerjansen@gmail.com',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Define the URL
url = "https://www.nasdaqomxnordic.com/webproxy/DataFeedProxy.aspx"

# Define the POST data
post_data = """
<post>
<param name="Exchange" value="NMF"/>
<param name="SubSystem" value="History"/>
<param name="Action" value="GetDataSeries"/>
<param name="AppendIntraDay" value="no"/>
<param name="Instrument" value="DK0016268840"/>
<param name="FromDate" value="1996-10-10"/>
<param name="ToDate" value="2024-08-07"/>
<param name="hi__a" value="0,1,2,4,21,8,10,11,12"/>
<param name="ext_xslt" value="/nordicV3/hi_table.xsl"/>
<param name="ext_xslt_lang" value="da"/>
<param name="ext_xslt_hiddenattrs" value=",ip,iv,"/>
<param name="ext_xslt_tableId" value="historicalTable"/>
<param name="app" value="/visitolur/soguleg_gogn"/>
</post>
"""

# Make the request
try:
    response = requests.post(url, data=post_data, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    logging.info("Successfully retrieved data from Nasdaq")
except requests.RequestException as e:
    logging.error(f"Request failed: {e}")
    raise

# Check if the request was successful
if response.status_code == 200:
    # Parse the response
    try:
        data = pd.read_html(response.text, attrs={'id': 'historicalTable'})[0]
        logging.info("Successfully parsed the data into DataFrame")
    except ValueError as e:
        logging.error(f"Failed to parse HTML: {e}")
        raise
else:
    logging.warning(f"Failed to retrieve data: Status code {response.status_code}")

# Print the DataFrame
print(data)
