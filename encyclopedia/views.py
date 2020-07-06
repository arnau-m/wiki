from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def new(request):
    return render(request, "encyclopedia/new.html",)

def random(request):
    return render(request, "encyclopedia/random.html")
