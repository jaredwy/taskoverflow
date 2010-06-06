def search_tasks(request):
    # TODO: make this JSON serialization more robust
    return HttpResponse(simplejson.dumps(errors))