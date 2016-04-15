'''
items and related functions
define global variables:
portalIp = your portal ip address and port, no trailing slash
portalAuth = ('user','password')
portalHeaders = {'Content-type':'application/xml'} xml or json
'''
import requests
import xml.etree.ElementTree as ET

class VSItem(object):
	def __init__(self, itemId, portalIp, portalAuth):
		self.itemId = itemId
		self.metadata  = requests.get(portalIp+'/API/item/'+self.itemId+'/?content=metadata',auth=portalAuth)

	def getShapedata(self, portalIp, portalAuth):
		r = requests.get(portalIp+'/API/item/'+self.itemId+'/?content=shape',auth=portalAuth)
		return r

	def valueFind(self,portalField):
		mdTree = ET.fromstring(self.metadata.text)
		ns = {'itemdoc':'http://xml.vidispine.com/schema/vidispine'}
		mdRaw = mdTree.find('itemdoc:metadata',ns)
		timespan = mdRaw.find('itemdoc:timespan',ns)
		for field in timespan.findall('itemdoc:field',ns):
			if field.find('itemdoc:name',ns).text == portalField:
				return field.find('itemdoc:value',ns).text

	def getSubmitter(self,portalIp,portalAuth,portalHeaders):
		submitterQuery = requests.get(portalIp + '/API/item/' + self.itemId + '/metadata/changes', auth=portalAuth, headers=portalHeaders)
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