# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from sucker.models import Post,Photo,Topic,Topic_site,Site,Category,Tag,User,Quote
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Topic)
admin.site.register(Site)
admin.site.register(Topic_site)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Quote)

