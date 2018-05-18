from django.shortcuts import render
from .models import Tag, KeyValueString, Node, Way,OSM_Relation, MemberRelation
from lxml import etree
from decimal import Decimal
from django.contrib.gis.geos import Point

def load(request):
	xmlfile = '''
	<osm version='0.6' generator='JOSM'>
	  <node id='313586' timestamp='2018-01-15T17:26:05Z' uid='72151' user='GeorgFausB' version='13' changeset='55469382' lat='50.9558026' lon='6.9691347'>
		<tag k='TMC:cid_58:tabcd_1:Class' v='Point' />
		<tag k='TMC:cid_58:tabcd_1:Direction' v='positive' />
		<tag k='TMC:cid_58:tabcd_1:LCLversion' v='9.00' />
		<tag k='TMC:cid_58:tabcd_1:LocationCode' v='39623' />
		<tag k='TMC:cid_58:tabcd_1:NextLocationCode' v='39624' />
		<tag k='TMC:cid_58:tabcd_1:PrevLocationCode' v='39622' />
		<tag k='test-tag' v='testvalue' />
	  </node>
	  <node id='23423432' timestamp='2017-01-15T17:26:05Z' uid='51' user='FausB' version='1' changeset='469382' lat='50.9558026' lon='6.9691347'>
	  <tag k='test-tag' v='testvalue' />
	</node>
	<node id='474327' timestamp='2017-03-23T16:54:06Z' uid='445794' user='hsimpson' version='20' changeset='47101627' lat='50.9555172' lon='6.9679685'>
	    <tag k='VRS:gemeinde' v='Köln' />
	    <tag k='VRS:ortsteil' v='Innenstadt' />
	    <tag k='bus' v='yes' />
	    <tag k='name' v='Worringer Straße' />
	    <tag k='network' v='VRS' />
	    <tag k='operator' v='KVB' />
	    <tag k='public_transport' v='stop_position' />
	</node>
	<way id='25250108' timestamp='2016-03-28T13:24:52Z' uid='109062' user='Jojo4u' version='28' changeset='38120453'>
	    <nd ref='313586' />
	    <nd ref='23423432' />
	    <tag k='electrified' v='contact_line' />
	    <tag k='frequency' v='0' />
	    <tag k='gauge' v='1000;1435' />
	    <tag k='maxspeed' v='30' />
	    <tag k='network' v='VVS' />
	    <tag k='operator' v='Stuttgarter Straßenbahnen AG' />
	    <tag k='railway' v='light_rail' />
	    <tag k='railway:pzb' v='no' />
	    <tag k='voltage' v='750' />
	    <tag k='workrules' v='DE:BOStrab' />
	 </way>
	 <way id='39694704' timestamp='2015-04-28T05:41:32Z' uid='15188' user='Polyglot' version='9' changeset='30569585'>
	    <nd ref='474327' />
	    <nd ref='12312343' />
	    <nd ref='5667674563' />
	    <tag k='bicycle' v='yes' />
	    <tag k='highway' v='residential' />
	    <tag k='name' v='Tommestraat' />
	    <tag k='oneway' v='yes' />
	  </way>
    <relation id='1403616' timestamp='2018-04-10T22:37:56Z' uid='15188' user='Polyglot' version='104' changeset='57986945'>
	  	<member type='node' ref='313586' role='platform' />
	    <member type='node' ref='474327' role='platform' />
	    <member type='way' ref='39694704' role='' />
	    <member type='way' ref='25250108' role='' />
	    <member type='node' ref='23423421' role='flat' />
	    <member type='way' ref='677668' role='relway' />
	    <member type='relation' ref='876878' role='relrel' />
	 </relation>

	 </osm>
	'''
	xmlfile = xmlfile.encode('utf-8')
	parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
	root = etree.fromstring(xmlfile,parser=parser)

	for primitive in root.getchildren():
		if primitive.tag == "node":
			#create tag
			snode_id   = int(primitive.get("id"))
			stimestamp = primitive.get("timestamp")
			suid       = int(primitive.get("uid"))
			suser      = primitive.get("user")
			sversion   = int(primitive.get("version"))
			schangeset = int(primitive.get("changeset"))
			slat       = float(primitive.get("lat"))
			slon       = float(primitive.get("lon"))

			node = Node(id=snode_id, timestamp=stimestamp,uid=suid,user=suser,version=sversion,visible=True,changeset=schangeset,incomplete=False)
			node.set_cordinates(slat,slon)
			node.save()

			for xmlTag in primitive.getchildren():
				getkey_fromxml = xmlTag.get("k")
				getvalue_fromxml = xmlTag.get("v")

				tag = Tag()
				tag = tag.add_tag(getkey_fromxml,getvalue_fromxml)
				node.tags.add(tag)

		elif primitive.tag == "way":
			wway_id    = int(primitive.get("id"))
			wtimestamp = primitive.get("timestamp")
			wuid       = int(primitive.get("uid"))
			wuser      = primitive.get("user")
			wversion   = int(primitive.get("version"))
			wchangeset = int(primitive.get("changeset"))

			way = Way(id=wway_id,timestamp=wtimestamp,visible=True,incomplete=False,uid=wuid,user=wuser,version=wversion,changeset=wchangeset)
			way.save()
			way.wn_set.all().delete()

			for xmlTag in primitive.getchildren():
				if xmlTag.tag == "nd":
					node_reference = int(xmlTag.get('ref'))
					try:
						node = Node.objects.get(id=node_reference)
						way.add_node(node)
						print(node)
					except Exception as e:
						print("Node does not exist creating dummy node")
						dummy_node = Node.objects.create(id=node_reference, visible=False, incomplete=True)
						dummy_node.set_cordinates(0,0)
						dummy_node.save()
						way.incomplete = 'True'
						way.save()
						way.add_node(node)

				elif xmlTag.tag == "tag":
					getkey_fromxml= xmlTag.get("k")
					getvalue_fromxml =xmlTag.get("v")

					tag = Tag()
					tag = tag.add_tag(getkey_fromxml,getvalue_fromxml)
					way.tags.add(tag)
		elif primitive.tag == "relation":
			rid        = int(primitive.get("id"))
			rtimestamp = primitive.get("timestamp")
			ruid       = int(primitive.get("uid"))
			ruser      = primitive.get("user")
			rversion   = int(primitive.get("version"))
			rchangeset = int(primitive.get("changeset"))

			relation = OSM_Relation(id=rid, timestamp=rtimestamp, uid=ruid, user=ruser, version=rversion, changeset=rchangeset,visible=True,incomplete=False)
			relation.save()
			relation.memberrelation_set.all().delete()

			for xmlTag in primitive.getchildren():

				if xmlTag.tag == 'tag':
					getkey_fromxml= xmlTag.get("k")
					getvalue_fromxml =xmlTag.get("v")

					tag = Tag()
					tag = tag.add_tag(getkey_fromxml, getvalue_fromxml)
					relation.tags.add(tag)

				elif xmlTag.tag == 'member':
					type = xmlTag.get("type")
					ref  = xmlTag.get("ref")
					role = xmlTag.get("role")

					try:
						if type == 'node':
							rel_node = Node.objects.get(id=ref)
							rm = relation.add_member(rel_node,type ,role)
						elif type == 'way':
							rel_way = Way.objects.get(id=ref)
							rm = relation.add_member(rel_way,type, role)
						elif type == 'relation':
							rel_child_relation = OSM_Relation.get(id=ref)
							rm = relation.add_member(rel_child_relation,type, role)

					except Exception as e:
						if type == 'node':
							dummy_rel_node = Node.objects.create(id=ref, visible=False, incomplete=True)
							dummy_rel_node.set_cordinates(0,0)
							dummy_rel_node.save()

							rm = relation.add_member(dummy_rel_node, type, role)
						
						elif type == 'way':
							dummy_rel_way = Way.objects.create(id=ref, visible=False, incomplete=True)
							dummy_rel_way.save()

							rm = relation.add_member(dummy_rel_way, type ,role)

						elif type == 'relation':
							dummy_rel_relation = OSM_Relation.objects.create(id= ref, visible=False, incomplete=True)
							dummy_rel_relation.save()

							rm = relation.add_member(dummy_rel_relation, type, role)

	return render(request,'osm/load.html')
