from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    """
    The view endpoint of the home url.
    """
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)