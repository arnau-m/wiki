from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms
from . import util

class SearchEntry(forms.Form):
    search = forms.CharField()


def index(request):
    if request.method == "POST":
        form = SearchEntry(request.POST)
        if form.is_valid():
            entry = util.get_entry(form.cleaned_data["search"])
            return render(request, "encyclopedia/wiki.html", {
                "entry": Markdown().convert(entry),
                "form": SearchEntry()
            })
    return render(request, "encyclopedia/index.html", {
            "form": SearchEntry(),
            "entries": util.list_entries()
        })


def new(request):
    return render(request, "encyclopedia/new.html",{
    })

def random(request):
    return render(request, "encyclopedia/random.html")

def wiki(request, title):
    entry = util.get_entry(title)
    msg = "404 Sorry, we coudn't find this entry..."
    if entry:
        return render(request, "encyclopedia/wiki.html", {
           "title": title, "entry": Markdown().convert(entry),
           "form": SearchEntry()
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "msg": msg,
            "form": SearchEntry()
        })
