from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from swizzleapi.views import register_user, login_user
from swizzleapi.views import RecipeView, TagView, CommentView, MixologistView, CategoryView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'recipes', RecipeView, 'recipe')
router.register(r'tags', TagView, 'tag')
router.register(r'comments', CommentView, 'comment')
router.register(r'mixologists', MixologistView, 'mixologist')
router.register(r'categories', CategoryView, 'category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]
