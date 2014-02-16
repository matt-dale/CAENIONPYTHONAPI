CAEN Ion 4-port RFID Reader IronPython API
==========================================

The Ion reader has a .NET API for easy manipulation of the reader.
It requires the CAENRFIDLibrary.dll

The decision to use IronPython instead of C# was out of speed. 
This library is not full featured API, but can get the reader up and running very quickly. 
Integrating different database connectors is quite easy for saving parsed tag reads.

