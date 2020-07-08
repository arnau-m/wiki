from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from markdown2 import Markdown
markdowner = Markdown()

from . import util

class SearchEntry(forms.Form):
    search = forms.CharField()

class NewEntry(forms.Form):
    title = forms.CharField()
    textarea = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = SearchEntry(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            for i in entries:
                if search in entries:
                    page = util.get_entry(search)
                    page_converted = markdowner.convert(page)
                    return render(request, "encyclopedia/wiki.html", {"entry": page_converted, "title": search, "form":SearchEntry()})
                if search.lower() in i.lower():
                    searched.append(i)
            return render(request, "encyclopedia/search.html", {"searched": searched, "form":SearchEntry()})

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":SearchEntry()
        })

def new(request):
    form = NewEntry(request.POST or None)
    if request.method == "POST" and form.is_valid():
        title = form.cleaned_data["title"]
        textarea = form.cleaned_data["textarea"]
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/404.html", {"msg": "This entry is already in use.", "form": SearchEntry()})
        else:
            util.save_entry(title, textarea)
            entry = markdowner.convert(util.get_entry(title))
            return render(request, "encyclopedia/wiki.html", {
                "entry": entry, "title":title, "form": SearchEntry()
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": SearchEntry(), "post": NewEntry()
        })


def random(request):
    return render(request, "encyclopedia/random.html", {
        "form":SearchEntry()
    })

def wiki(request, title):
    entry = util.get_entry(title)
    msg = "404, Sorry, we coudn't find this entry..."
    if entry:
        return render(request, "encyclopedia/wiki.html", {
           "title": title, "entry": Markdown().convert(entry),
           "form":SearchEntry()
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "msg": msg,
            "form":SearchEntry()
        })
