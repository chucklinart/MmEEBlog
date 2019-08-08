from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from . models import Blog, Promo
from video_encoding.admin import FormatInline
from .submodels.media import Pic, Video, Podcast
from .submodels.taxonomy import Category
from .submodels.people import Blogger

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['title']
    search_fields =['title']

class PicAdmin(admin.ModelAdmin):
    exclude = ['thumbnail']
    ordering = ['posted', ]
    search_fields = ['title', 'desc']

class VideoAdmin(admin.ModelAdmin):
    exclude = ('posted', )
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['category']
    search_fields = ['title', 'description']
    inlines = (FormatInline,)
    list_display = ('file_name', 'width', 'height', 'duration')
    readonly_fields = ('file_name', 'width', 'height', 'duration')

class BlogAdmin(admin.ModelAdmin):
    exclude = ('posted', )
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['blogimg', 'blogvid']

class BloggerInline(admin.StackedInline):
    model = Blogger
    can_delete = False
    verbose_name_plural = 'Blogger'
    fk_name = 'user'

class BloggerAdmin(UserAdmin):
    inlines = (BloggerInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(BloggerAdmin, self).get_inline_instances(request, obj)

class PodcastAdmin(admin.ModelAdmin):
    exclude = ('pubdate', )
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    # add 'audio_file_player' tag to your admin view
    list_display = (..., 'audio_file_player', ...)
    actions = ['custom_delete_selected']

    def custom_delete_selected(self, request, queryset):
        #custom delete code
        n = queryset.count()
        for i in queryset:
            if i.audio_file:
                if os.path.exists(i.audio_file.path):
                    os.remove(i.audio_file.path)
            i.delete()
        self.message_user(request, ("Successfully deleted %d audio files.") % n)
    custom_delete_selected.short_description = "Delete selected items"

    def get_actions(self, request):
        actions = super(PodcastAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.unregister(User)
admin.site.register(User, BloggerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Pic, PicAdmin)
admin.site.register(Podcast)
admin.site.register(Promo)
