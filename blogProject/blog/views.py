#from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Blog
#from django.views.generic import ListView



class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    queryset = Blog.objects.all()

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'

    def get_object(self):
       id = self.kwargs.get('pk')
       return get_object_or_404(Blog, pk=id)
    
