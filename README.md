# Data collection from diverse data sources

<img width="700" alt="Screen Shot 2022-11-23 at 11 34 15 PM" src="https://user-images.githubusercontent.com/72933965/203702297-ddf0c96a-1f0f-48d8-86c3-6b7f0e8bda52.png">

This application takes files from ExperimentalMaterials folder: *chemid.xml, MeSHSupplemental.xml, List_of_Classifications.xls, chemname.zip* - 
read, clean and aggregate them. In the final table collected all chemicals with unique CAS Numbers from each data source. 

### Before run this app you should:
- create a DataBase in PostgresSQL where you want to load aggregated data

### Change parameters in params.yml:
 - Enter the path and names of files you want to aggregate in the **files** section and PostgresSQL credential in **postgres** section. Enter the name of csv file ,where you want to store final table in the **csv_directory**.

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
