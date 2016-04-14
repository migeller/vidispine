'''
items and related functions
'''
import requests
import xml.etree.ElementTree as ET

class VSItem:
	def __init__(self, itemId):
		self.itemId = itemId

	def getMetadata(self, portalIp, portalAuth):
		r = requests.get(portalIp+'/API/item/'+self.itemId+'/?content=metadata',auth=portalAuth)
		return r

	def getShapedata(self, portalIp, portalAuth):
		r = requests.get(portalIp+'/API/item/'+self.itemId+'/?content=shape',auth=portalAuth)
		return r

	def valueFind(self,xml,portalField):
		mdTree = ET.fromstring(xml.text)
		ns = {'itemdoc':'http://xml.vidispine.com/schema/vidispine'}
		mdRaw = mdTree.find('itemdoc:metadata',ns)
		timespan = mdRaw.find('itemdoc:timespan',ns)
		for field in timespan.findall('itemdoc:field',ns):
			if field.find('itemdoc:name',ns).text == portalField:
				return field.find('itemdoc:value',ns).text