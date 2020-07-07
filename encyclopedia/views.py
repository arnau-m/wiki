from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def new(request):
    return render(request, "encyclopedia/new.html",{

    })

def random(request):
    return render(request, "encyclopedia/random.html")

def wiki(request, title):
    entry = util.get_entry(title)
    msg = "404, Sorry, we coudn't find this entry..."
    if entry:
        return render(request, "encyclopedia/wiki.html", {
           "title": title, "entry": Markdown().convert(entry),
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "msg": msg
        })
