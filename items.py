'''
items and related functions
define global variables:
vs_url = your vidispine ip address and port, no trailing slash
vs_auth = ('user','password')
vs_headers = {'Content-type':'application/xml'} xml or json
'''
import requests
import xml.etree.ElementTree as ET

class vsItem(object):
	def __init__(self, item_id, vs_url, vs_auth):
		self.item_id = item_id
		self.metadata  = requests.get(vs_url+'/API/item/'+self.item_id+'/?content=metadata',auth=vs_auth)

	def getShapedata(self, vs_url, vs_auth):
		r = requests.get(vs_url+'/API/item/'+self.item_id+'/?content=shape',auth=vs_auth)
		return r

	def valueFind(self,vs_field):
		mdTree = ET.fromstring(self.metadata.text)
		ns = {'vs':'http://xml.vidispine.com/schema/vidispine'}
		mdRaw = mdTree.find('vs:metadata',ns)
		timespan = mdRaw.find('vs:timespan',ns)
		for field in timespan.findall('vs:field',ns):
			if field.find('vs:name',ns).text == vs_field:
				return field.find('vs:value',ns).text

	def getSubmitter(self,vs_url,vs_auth,vs_headers):
		submitterQuery = requests.get(vs_url + '/API/item/' + self.item_id + '/metadata/changes', auth=vs_auth, headers=vs_headers)
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