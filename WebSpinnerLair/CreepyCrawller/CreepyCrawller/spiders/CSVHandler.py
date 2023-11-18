import os
import pandas as pd
import logging

class CSVHandler:
    def __init__(self, csv_file, data_class):
        self.csv_file = csv_file
        self.data_class = data_class
        logging.basicConfig(filename='CSVHandler.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_file_with_header(self):
        logging.info("Create File with Headers")
        if not os.path.exists(self.csv_file):
            #logging.info(f"Attributes in StockData: {dir(self.data_class)}")
            self.get_properties_names()
            # Get the property names from the class
            header_row = [prop for prop in dir(self.data_class) if not callable(getattr(self.data_class, prop)) and not prop.startswith("__")]
            logging.info("Header Row {header_row}")
            # Create a DataFrame with the header row
            df_header = pd.DataFrame(columns=header_row)
            df_header.to_csv(self.csv_file, index=False)
    def append_data(self, data):
        logging.info("Append data to the CSV")
        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame([data.__dict__])
        # Append data to the CSV file
        df.to_csv(self.csv_file, mode='a', index=False, header=not os.path.exists(self.csv_file), sep=';')

    def get_properties_names(self):
        obj = self.data_class
        classname = self.data_class
        logging.info(f"Nome da Class: {classname}")
        components = dir(classname)
        logging.info(f"Componentes: {components}")
        
        properties = [attr for attr in components if type(getattr(obj, attr, None)) is property]
        
        for prop in properties:
            logging.info(f"Found property: {prop}")
        
        return properties