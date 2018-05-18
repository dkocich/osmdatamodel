from django.contrib import admin
from .models import Tag,Node,KeyValueString,Way,OSM_Relation,MemberRelation

class TagAdmin(admin.ModelAdmin):
	display = ('tag.id')
class NodeAdmin(admin.ModelAdmin):
	list_display =('id','user')
class KeyValueStringAdmin(admin.ModelAdmin):
	display =('value')
class WayAdmin(admin.ModelAdmin):
	list_display =('id','user')
class RelationAdmin(admin.ModelAdmin):
	list_display = ('id','user')

admin.site.register(Tag,TagAdmin)
admin.site.register(Node,NodeAdmin)
admin.site.register(KeyValueString,KeyValueStringAdmin)
admin.site.register(Way,WayAdmin)
admin.site.register(OSM_Relation,RelationAdmin)