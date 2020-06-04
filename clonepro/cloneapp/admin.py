from django.contrib import admin
from cloneapp.models import Videos, Comment ,recently_viewed
from django.utils.html import format_html

class VideoAdmin(admin.ModelAdmin):
    if Videos.videofile:
        list_display = ('videofile_tag',)
        readonly_fields = ('videofile_tag',)
    else:
        list_display = ('videofile_tag',)
        
    def videofile_tag(self,obj):
        if obj.videofile.url:
            return format_html('<video src ="{}" width = "50" height = "50" />'.format(obj.videofile.url))
    #profile_pic_tag.allow_tags = True
    
    videofile_tag.short_description = 'videofile'

admin.site.register(Videos,VideoAdmin)
admin.site.register(Comment)
admin.site.register(recently_viewed)

# Register your models here
