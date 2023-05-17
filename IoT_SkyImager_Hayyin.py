import time
import socket
import tqdm
import os
import schedule
from time import sleep
from datetime import datetime
import mysql.connector
from PIL import Image
import pandas as pd

location = input("State location: ")

# Establish a connection to mysql database
cnx = mysql.connector.connect(user='root',
                              password='mysql',
                              host='localhost',
                              port = '3307',
                              database='skyimager')

def imageprocessor(imgname):
    im = Image.open(imgname)
    im = im.resize((1080,720))
    current_time = datetime.now().strftime('%Y%m%d%H%M')
    current_timeInt = int(current_time)
    data = {'cloudinfo_datetime':[], 'cloudinfo_location':[], 'cloudinfo_colour':[], 'cloudinfo_colourpercent':[]}
    df1 = pd.DataFrame(data)
    df4 = {}
    print("Processing Image")
    for i in range(120,255):
        total_pixel = 0
        j = list(range(i,i+15))
        for pixel in im.getdata():
                r,g,b = pixel
                if g == i and b in j:              # if your image is RGB (if RGBA, (0, 0, 0, 255) or so
                    total_pixel += 1

        print('RGB(' + str(i) + ',' + str(i) + ',' + str(i) + ')=' + str(total_pixel))
        
        data = {'cloudinfo_datetime':[current_timeInt], 'cloudinfo_location':[location], 'cloudinfo_colour':[int(i)], 'cloudinfo_colourpercent':[total_pixel]}
        df2 = pd.DataFrame(data)
        # print(df2)
        if i == 120:
            df3 = pd.concat([df1, df2], ignore_index=True)
            df3.reset_index()
        

        else:
            df3 = pd.concat([df3, df2], ignore_index=True)
            df3.reset_index()
    
    # To sort values addording to most colour code
    df4 = df3.sort_values(by='cloudinfo_colourpercent',ascending=False)  
    
    # To take top 10 colour code
    df4 = df4.head(10)

    cnx = mysql.connector.connect(user='root',
                              password='mysql',
                              host='localhost',
                              port = '3307',
                              database='skyimager')

    # Create a cursor object
    cursor = cnx.cursor()


    # Iterate through the rows of the DataFrame
    for index, row in df4.iterrows():
        # Build the update query
        # query = f'INSERT INTO cloudinfo WHERE cloudinfo_datetime = "{row["cloudinfo_datetime"]}", cloudinfo_location = "{row["cloudinfo_location"]}", cloudinfo_colour = "{row["cloudinfo_colour"]}",cloudinfo_colourpercent = "{row["cloudinfo_colourpercent"]}"'
        # query = f'INSERT INTO cloudinfo (cloudinfo_datetime,cloudinfo_location,cloudinfo_colour,cloudinfo_colourpercent) VALUES ("{row["cloudinfo_datetime"]}", "{row["cloudinfo_location"]}", "{row["cloudinfo_colour"]}","{row["cloudinfo_colourpercent"]}"'
        
        query = f'INSERT INTO cloudinfo (cloudinfo_datetime, cloudinfo_location, cloudinfo_colour, cloudinfo_colourpercent) VALUES ("{row["cloudinfo_datetime"]}", "{row["cloudinfo_location"]}", "{row["cloudinfo_colour"]}", "{row["cloudinfo_colourpercent"]}")'

        # Execute the update query
        cursor.execute(query)

    # Commit the changes
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()
    
    
       # print('RGB(' + str(i) + ',' + str(i) + ',' + str(i) + ')=' + str(total_pixel))
    print("Done processing Image")
    



    #INSERTING DATA TO MYSQL  




def receiver():
    print("Start\n\n")
    # device's IP address
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = 5001
    # receive 4096 bytes each time
    BUFFER_SIZE = 4096
    SEPARATOR = "<SEPARATOR>"

    # create the server socket
    # TCP socket
    s = socket.socket()

    # bind the socket to our local address
    s.bind((SERVER_HOST, SERVER_PORT))

    # enabling our server to accept connections
    # 5 here is the number of unaccepted connections that
    # the system will allow before refusing new connections
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    # accept connection if there is any
    client_socket, address = s.accept() 
    # if below code is executed, that means the sender is connected
    print(f"[+] {address} is connected.")

    # receive the file infos
    # receive using client socket, not server socket
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    filename = os.path.basename(filename)
    # convert to integer
    filesize = int(filesize)

    # start receiving the file from the socket
    # and writing to the file stream
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    path = filename
    #path = "./rec/" + filename 

    with open(path, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the client socket
    client_socket.close()
    # close the server socket
    s.close()
    sleep(1)
    print("\n\nRECEIVED")

    current_time = datetime.now().strftime('%Y%m%d%H%M')
    # COUNTING CLOUD PIXEL FROM IMAGE
    imageprocessor(filename)


    #TO RENAME FILE    
    # print("\n\nRenaming file")
    # Get the current time and convert it to a string
    current_timeInt = int(current_time)
    # Define the old and new file names, and the folder where the file will be moved
    old_file_name = filename
    new_file_name = f'Sky_Image_{current_time}.jpg'
    folder_name = 'rec'
    newFileDir = os.path.join(folder_name, new_file_name)
    # Rename the file and move it inside the folder
    os.rename(old_file_name, new_file_name)
    # os.rename(new_file_name, os.path.join(folder_name, new_file_name))
    os.rename(new_file_name, newFileDir)




     
    


schedule.every(5).minutes.do(receiver)
print("Dah Start")
receiver()


while True:
    schedule.run_pending()
    sleep(1)




