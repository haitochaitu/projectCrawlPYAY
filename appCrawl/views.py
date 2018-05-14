from django.shortcuts import render

def pageCrawl(request):
  return render(request, "pageCrawl.html")

def pageResult(request):
    crawling_url = request.POST["name_seed_url"]
    depth = request.POST["name_traverse_depth"]
    return render(request, "pageResult.html", {'url': crawling_url, 'depth' : depth})