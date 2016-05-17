'''
defining and acting on vidispine storages
define global variables:
vs_url = your vidispine ip address and port, no trailing slash
vs_auth = ('user','password')
vs_headers = {'Content-type':'application/xml'} xml or json
'''

import requests
import xml.etree.ElementTree as ET

class vsStorage(object):
	def __init__(self, storage_id, vs_url, vs_auth):
		self.storage_id = storage_id
		
	def forceRescan(self): #forces rescan of items in the storage
		r = requests.post(vs_url+'/API/'+self.storage_id+'/rescan',auth=vs_auth,headers=vs_headers)
		if str(r) == '<Response [200]>':
			return True
		else:
			return False

	def getFileList(self, count=100): 
	#returns xml as string of files on storage, up to count 
		r = requests.get(vs_url+':8080/API/storage/'+self.storage_id+'/file?count='+count,auth=vs_auth,headers=vs_headers)
		return r.text
