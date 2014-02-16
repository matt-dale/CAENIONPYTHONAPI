"""Database connection and functions for RFID System"""
from globalImports import *

clr.AddReference('Npgsql')
import Npgsql as pgsql

"""
The PostgreSQL table should have the following format for tag saving.
TableName = rfidread
Fields:
    tagid
    locationid
    timestamp

"""

class dataBaseConnector:
    """Provides a PostgreSQL connection for tag saving
    """
    def __init__(self, IPAddress, database, user, password):
        """connects to the given database"""

        connectionString = 'server=%s; database=%s; user id=%s; password=%s' % (IPAddress, database, user, password)
        self.connection = pgsql.NpgsqlConnection(connectionString)
        self.conection.Open()
        return self

    def saveTheTagData(self, tagID, locationID, readTime):
        """queries the database for the last saved data.
            Then saves a new record if necessary 
            and deletes an older one if neccessary.

            readTime is a python datetime object

            The goal is to have the oldest location time, and the most recent read.
            For example, if an asset sits in one location for an entire day, 
            we want to know when it arrived to that location, then the last time
            it was seen there.  Not every read in between those two reads.

        """
        fmt = "%m/%d/%Y %H:%M:%S"
        command = self.connection.CreateCommand()
        #I wasn't able to figure out the bind variable use, so this statement is vulnerable to SQL Injection
        theSQL = "SELECT * FROM rfidread WHERE tagid = "+"'"+str(tagID)+"'"+" ORDER BY rfidread.timestamp DESC;"
        command.CommandText = theSQL
        reader = command.ExecuteReader()
        saveNewReadData = False
        #pop off the top record which will be the latest read datetime
        lastTwoTagReads = []
        for i in range(2):
            if reader.Read() == True:
                theOldID = reader.GetValue(reader.GetOrdinal('id'))
                oldLocationID = reader.GetValue(reader.GetOrdinal('locationid'))
                theDateTime = reader.GetValue(reader.GetOrdinal('timestamp'))
                oldDateTime = datetime.datetime.strptime(str(theDateTime), fmt)
                lastTwoTagReads.append([oldDateTime, oldLocationID, theOldID])
        reader.Close()
        if len(lastTwoTagReads) > 0:
            if len(lastTwoTagReads) == 2:
                #compare the location IDs, if they are different, then save the data
                if locationID != lastTwoTagReads[0][1]:
                    saveNewReadData = True
                else:
                    #the new read location is the same as the most recent read
                    #[1] should be the older record, while [0] should be the newest
                    #do the two older records have the same location id?
                    """
                    UPDATE rfidread
                       SET "timestamp"='12/31/2015 12:12:12'
                    WHERE id=14;
                     """
                if lastTwoTagReads[0][1] == lastTwoTagReads[1][1]:
                    #now update record [0][2] timestamp to readTime
                    updateSQL = 'UPDATE rfidread SET "timestamp"= '+"'"+datetime.datetime.strftime(readTime, fmt)+"'"+'WHERE id= '+str(lastTwoTagReads[0][2])+';'
                    updateCommand = self.connection.CreateCommand()
                    updateCommand.CommandText = updateSQL
                    updateCommand.ExecuteNonQuery()
            else:
                #This tag has more than one read, but not only 2
                saveNewReadData = True
        else:
            #this tag has no data, just save the new read
            saveNewReadData = True
        if saveNewReadData == True:
            insertCommand = self.connection.CreateCommand()
            insertCommand.CommandText = "insert into rfidread (tagid, locationid, timestamp)  values (:tagid, :locationid, :datetime)"
            insertCommand.Parameters.AddWithValue('datetime', datetime.datetime.strftime(readTime, fmt))
            insertCommand.Parameters.AddWithValue('tagid', tagID)
            insertCommand.Parameters.AddWithValue('locationid', locationID)
            insertCommand.ExecuteNonQuery()
        self.connection.Close()
        return





