# Data collection from diverse data sources
<img width="901" alt="Screen Shot 2022-11-24 at 8 56 49 AM" src="https://user-images.githubusercontent.com/72933965/203840255-6757ddb7-1a64-4c61-a6ff-d21865b55466.png">

### Description
This application combines data from four diverse sources, and when aggregatted by CAS Numbers, generates a single, analytical dataset and loads it to:
- a table in PostgresSQL database 
- .csv file 
to make all the data available to the end user. 

The following files should be provided and uploaded to ExperimentalMaterials folder as inputs:
-	chemid.xml
-	MeSHSupplemental.xml
-	List_of_Classifications.xls
-	chemname.zip.

### Before running the application:
Make sure there is a database available in PostgresSQL as the target location for the data. User can choose the table to be created automatically at a runtime (see params.yml)

### User parameters in params.yml:
Under **files** section, enter the path and names of input files to be combined; **postgres** section lets the user provide PostgresSQL credentials as well as table name. Finally, the name and location of output csv file can be specified in **csv_directory** section; **test** section applies to run the application in test mode (see below).

### To run the application execute the following command:
- *python main.py*

### Test mode
A total of two static files have been prepared to run the application in a test mode: 
- List_of_Classifications.xls,
-	chemname.zip. 
both located in ExperimentalMaterials folder. 

These files may be replaced by different versions with modified data as long as the overall structure and format remains the same. The other two files can be substituted with any of files available on the following sources:
- MeSH Data from https://www.nlm.nih.gov/databases/download/mesh.html
- ChemIDplus Subset Data from https://www.nlm.nih.gov/databases/download/chemidplus.html

### To run test:
-	Set parameters under **test** section in params.yml
-	execute the following commands:
-	*python test.py*
