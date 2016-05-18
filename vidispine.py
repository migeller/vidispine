'''
Classes and methods for use with Vidispine DB

vs_url = your vidispine ip address and port, no trailing slash
vs_auth = ('user','password')
vs_headers = {'Content-type':'application/xml'} xml or json
'''

import requests
import xml.etree.ElementTree as ET

class vsDB(object):
	def __init__(self, vs_url, vs_auth, vs_headers):
		self.vs_url = vs_url
		self.vs_auth = vs_auth
		self.vs_headers = vs_headers

class vsItem(vsDB):
	def __init__(self, item_id, database):
		vsDB.__init__(self,database.vs_url,database.vs_auth,database.vs_headers)
		self.item_id = item_id
		self.metadata  = requests.get(self.vs_url+'/API/item/'+self.item_id+'/?content=metadata',auth=self.vs_auth)

	def getShapedata(self):
		r = requests.get(self.vs_url+'/API/item/'+self.item_id+'/?content=shape',auth=self.vs_auth)
		return r

	def valueFind(self,vs_field):
		mdTree = ET.fromstring(self.metadata.text)
		ns = {'vs':'http://xml.vidispine.com/schema/vidispine'}
		mdRaw = mdTree.find('vs:metadata',ns)
		timespan = mdRaw.find('vs:timespan',ns)
		for field in timespan.findall('vs:field',ns):
			if field.find('vs:name',ns).text == vs_field:
				return field.find('vs:value',ns).text

	def lastChange(self):
		submitterQuery = requests.get(self.vs_url + '/API/item/' + self.item_id + '/metadata/changes', auth=self.vs_auth, headers=self.vs_headers)
		submitterQuery.encoding = 'utf-8'
		tree = ET.fromstring(submitterQuery.text)
		fields = tree.iter('{http://xml.vidispine.com/schema/vidispine}field')
		submitterFound = False
		while submitterFound == False:
			try:
				field = fields.next()
			except StopIteration:
				return 'postingest' #or other default user
				submitterFound = True
			if field.attrib['user'] != 'system' and field.attrib['user'] != 'admin':
				return field.attrib['user']
				submitterFound = True

class vsStorage(vsDB):
	def __init__(self, storage_id, database):
		self.storage_id = storage_id
		vsDB.__init__(self,database.vs_url,database.vs_auth,database.vs_headers)

	def forceRescan(self): 
		#forces rescan of items in the storage
		r = requests.post(vs_url+'/API/'+self.storage_id+'/rescan',auth=self.vs_auth,headers=self.vs_headers)
		if str(r) == '<Response [200]>':
			return True
		else:
			return False

	def getFileList(self, count='100'): 
		#returns xml as string of files on storage, up to count 
		r = requests.get(self.vs_url+'/API/storage/'+self.storage_id+'/file?count='+count,auth=self.vs_auth,headers=self.vs_headers)
		return r.text