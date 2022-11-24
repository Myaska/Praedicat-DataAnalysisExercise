# Data collection from diverse data sources

<img width="566" alt="Screen Shot 2022-11-23 at 3 45 51 PM" src="https://user-images.githubusercontent.com/72933965/203654548-6135195a-b2d1-4779-93cc-55030da6bbdb.png">

This application takes files from ExperimentalMaterials folder:
*chemid.xml, MeSHSupplemental.xml, List_of_Classifications.xls, chemname.zip*
read, clean and aggregate them. In the final table collected chemicals only with unique CAS Numbers from each data source. 

### Before run this app you should:
- create a DataBase in PostgresSQL where you want to load aggregated data

### Change parameters in params.yml:
 - Enter the path and names of files you want to aggregate in the **files** section and PostgresSQL credential in **postgres** section. Enter the name of csv file in the **csv_directory** where you want to store final table.

### To run the app execute the following commands: 
- tested im Python 3.9.12
- pip install -r requirements.txt
- set up app parameters in params.yaml
- sh run_app.sh 

### Test application
This test checks that provided application can work with any file of the same type

- For test two types of files were downloaded:
  - MeSH Data from https://www.nlm.nih.gov/databases/download/mesh.html
  - ChemIDplus Subset Data from https://www.nlm.nih.gov/databases/download/chemidplus.html 
