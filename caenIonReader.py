"""Caen 4300P Ion RFID reader functions for Masque use"""
from globalImports import *

import urllib
clr.AddReferenceToFile('CAENRFIDLibrary.dll')
from com.caen.RFIDLibrary import *


class CaenIonReader:
    """Instantiates the Caen Reader for use.

    Depending on the given attribute, it connects via TCP to 
    the given reader.

    Attributes:
        IPAddress: A String, IP of the CAEN Ion Reader
    """

    def __init__(self, IPAddress):
        """connects to the given reader and waits for a read command"""
        
        self.theReader = CAENRFIDReader()
        self.theReader.Connect(CAENRFIDPort.CAENRFID_TCP,
                                IPAddress)
        try:
            #this is used to make sure that we are connected before continuing
            #passing for now....
            #self.theReader.GetReaderInfo()
            t = 1
        except:
            raise Exception('Cannot connect to %s reader' % self.readerLocation)
        return self

    def setOneGPIO(self, pin, value):
        """Fairly obvious. This will only change the specific pin's value, 
        leaving all other values the same. If the pin is set to an input, it
        cannot be changed.

        Args:
            pin = GPIO Pin as string
            value = String 'Low' or 'High'
        Returns:
            Boolean if GPIO was successfully set
        Raises: 
            Exception if pin is designated as an Input
        """
        pinValues = {
            '0':1,
            '1':2,
            '2':4,
            '3':8,
            '4':16,
            '5':32,
            '6':64,
            '7':128,
            '8':256,
            '9':512,
            '10':1024,
            '11':2048,
            '12':4096
            }
        ioDirection = self.theReader.GetIODirection()
        inputPins = []
        for i in range(13):
            if 2**i & ioDirection == 0:
                inputPins.append(i)
        if pin in inputPins:
            raise Exception('%s is an input pin. Cannot change the value' % pin)
        else:
            currentValue = self.theReader.GetIO()
            currentValues = {}
            for i in range(13):
                if 2**i & currentValue == 0:
                    currentValues[str(i)] = 'Low'
                else:
                    currentValues[str(i)] = 'High'
            if value == 'High':
                if currentValues[pin] == 'High':
                    return True
                else:
                    newValue = currentValue + pinValues[pin]
            elif value == 'Low':
                if currentValues[pin] == 'Low':
                    return True
                else:
                    newValue = currentValue - pinValues[pin]
            else:
                return False
            self.theReader.SetIO(newValue)    
            return True

    def disconnect(self):
        """just makes the CAENRFIDReader Disconnect() method local
        """
        self.theReader.Disconnect()
        return

    def inventoryTags(self, source):
        """returns dict of tags read with tagID as key, with the tagObject as value
        """
        inventory = source.InventoryTag()
        tags = {}
        if inventory:
            if len(inventory) > 0:
                for i in inventory:
                    tagID = System.BitConverter.ToString(i.GetId()).replace('-','')
                    tags[tagID] = i
        return tags