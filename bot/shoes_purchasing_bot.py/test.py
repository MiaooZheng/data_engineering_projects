import requests

# Example URL
url = 'https://www.birkenstock.com/ca/login'

# Make the HTTP request
response = requests.get(url)

# Access the headers of the response object
headers = response.headers

# Extract the value of the :path header
# path_header = headers.get(':path')

# Print the value of the :path header
#print(headers)

path_header = headers.get('Date')
print(path_header)







from flask import Flask, send_file
import pickle

app = Flask(__name__)

# Define an API endpoint that returns a pickle file
@app.route('/pickle', methods=['GET'])
def get_pickle_file():
    # Load the pickle file into memory
    with open('example.pickle', 'rb') as f:
        data = pickle.load(f)

    # Return the pickle file as a response
    return send_file(data, mimetype='application/octet-stream', as_attachment=True, attachment_filename='example.pickle')











