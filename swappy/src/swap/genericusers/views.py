from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class UserzoneView(View):
    """
    The view endpoint of the userzone url.
    """
    template_name = 'genericusers/userzone.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
    	return HttpResponse(status=200)