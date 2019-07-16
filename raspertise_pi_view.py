import pyodbc
import pandas as pd

driver = 'ODBC Driver 17 for SQL Server'    # change to what you found in libsqlvdi.so
port = 1433                                 # default MSSQL port.
server = 'localhost'                        # Server address
database = 'ContosoUniversity3'             # Desired database on the server
user_id = 'SA'                              # default user name of MSSQL. Change if necessary
password = 'Hackathon1201!'                 # MSSQL Password

con = pyodbc.connect(
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"PORT:{port};"
    f"DATABASE={database};"
    f"UID={user_id};"
    f"PWD={password}")

con.execute("USE ContosoUniversity3")

# cursor = con.cursor()
# cursor.execute('SELECT * FROM Student')

# for row in cursor:
#     print('row = %r' % (row,))

df = pd.read_sql_query("SELECT * FROM Student;", con)

# print(str(df))

# for r in df:
#     print(r)

# print(df)
# print(df['LastName'])

for name, row in df.iterrows():
    print(f"{row['ID']}, {row['FirstName']}, {row['LastName']}, {row['EnrollmentDate']}")

con.close()

