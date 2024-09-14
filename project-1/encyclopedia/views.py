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

    entries = util.search_entries(query)

    if len(entries) == 0:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries found."
        })
    elif len(entries) == 1:
        return redirect("entry", entries[0])
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": entries
        })


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        if title == "":
            return render(request, "encyclopedia/error.html", {
                "message": "Please enter a title for your new entry."
            })
        elif content == "":
            return render(request, "encyclopedia/error.html", {
                "message": "Please enter a description for your new entry."
            })
        elif title.lower().capitalize() in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })

        util.create_entry(title, content)

        return redirect("/wiki/" + title)


def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        if content == None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry does not exist."
            })
        else:
            return render(request, "encyclopedia/edit.html",
            {
                "title": title,
                "content": content
            })
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        if not content.startswith(f"# {title}"):
            content = f"# {title}\n\n{content}"

        util.save_entry(title, content)
        return redirect("/wiki/" + title)


def random_entry(request):
    title = util.get_random_entry()
    return redirect("/wiki/" + title)