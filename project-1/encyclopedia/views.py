from django.shortcuts import render
from django.shortcuts import redirect

from . import util
import markdown

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    query = request.GET.get("q")

    if query == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Please enter a search term."
        })

    entries, is_exact_match = util.search_entries(query)

    if len(entries) == 0:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries found."
        })
    elif is_exact_match:
        return redirect("entry", entries[0])
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": entries
        })

def create(request):
    return render(request, "encyclopedia/create.html")