# Housing-Passport
MSc Individual Project at Imperial College London in partial fulfillment for the MSc degree in Software Engineering

## Back end
The back end is implemented in Python using Flask. It is the flask-basic file directory and can be run by running the command  

flask run  

The dependencies are in the requirements.txt file. In addition to this, the machine learning model requires Pandas, PyTorch, Numpy and Pickle to run.

## Front end
The front end is implemented in React.js. It is the react-basic file directory and can be run by running the command  

npm install  
npm start  

## ML Model
The ML Model directory contains the errors collected for the pickle models and the file convert_to_db.py which is used to convert EPC data to the format used in the database. 

## EPC Data Analysis
The EPC Data Analysis folder contains the script run on the EPC data for analysis and the Excel file with the results.

## Notes
The EPC data is 31GB so it has not been added to this project. It is available from  
https://epc.opendatacommunities.org/

## Acknowledgements

The ML model takes inspiration from the project:
https://gitlab.doc.ic.ac.uk/lab2021_autumn/neural_networks_72
