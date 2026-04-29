from plc_client import read_plc_data
#from database import save_data

data = read_plc_data()
#save_data(data)
print(data)