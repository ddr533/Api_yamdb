from django.contrib import admin

from .models import Comment, Review, User, Title, Category, Genre


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'text', 'author', 'score', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'text', 'author', 'pub_date')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Title)
admin.site.register(Cateogory)
admin.site.register(Genre)
admin.site.register(User)
