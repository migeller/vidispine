#Vidispine
A python module for use with a Vidispine Database.

requires -

python 2.7+

xml.etree.ElementTree (https://docs.python.org/2/library/xml.etree.elementtree.html)

Requests (http://docs.python-requests.org/en/master/)

#Classes

##vsDB 
Create this base class to define:

vs_url - IP address or url, including port number, no trailing slash

vs_auth - ('username','password')

vs_headers - {'content-type':'application/xml'} currently only supports parsing xml returns.

##vsItem
Subclass that takes an item id and a database to create. 
Methods:

getShapedata() - returns request object of shape data, use the .text to utilize contents.
	
findValue(value) - returns metadata value for specified field.
	
lastChange() - returns username of most recent metadata update, excluding admin. Modify default user if you have one.

##vsStorage
Subclass that takes a storage id and database to create.
Methods:

forceRescan() - forces a rescan of the storage

getFileList(optional count=['num']) - returns a requests object of the list of files on a storage, default count is 100.