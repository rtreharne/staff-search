from django.shortcuts import render
from staff.models import Institute, Profile, Department
from staff.forms import SearchForm
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from staff.models import Profile, Department, Keyword, Banner

def get_banner():
    banner = Banner.objects.order_by('?').first()
    return banner.url


def index(request):

    context = {"banner": get_banner()}

    vector = SearchVector("last_name",
                          "first_name",
                          "role",
                          "about",
                          "research",
                          "teaching",
                          "publications",
                          "professional_activities",
                          "additional_info")

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():

            query = SearchQuery(form.cleaned_data["keyword"])

            department = Department.objects.filter(name=form.cleaned_data["department"])

            if len(department) > 0:
                profiles = Profile.objects.filter(department=department[0])
            else:
                profiles = Profile.objects.all()

            search = profiles.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.01).order_by('-rank')

            if len(search) > 0:
                max_value = max([x.rank for x in search])
                for item in search:
                    score = item.rank*100/max_value
                    item.rank = score

            context["results"] = search
            context["keyword"] = form.cleaned_data["keyword"]
    else:
        form = SearchForm

    keyword = request.GET.get('keyword', None)
    print(keyword)
    print(request)
    if keyword:
        query = SearchQuery(keyword)
        profiles = Profile.objects.all()

        search = profiles.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.01).order_by('-rank')

        if len(search) > 0:
            max_value = max([x.rank for x in search])
            for item in search:
                score = item.rank * 100 / max_value
                item.rank = score

        context["results"] = search
        context["keyword"] = keyword
        context["form"] = form

        return render(request, "index.html", context)

    context["form"] = form

    return render(request, "index.html", context)

def directory(request):
    # get institutes
    institutes = Institute.objects.all().order_by('name')
    departments = Department.objects.all().order_by('name')
    profiles = Profile.objects.all().order_by('last_name')

    context = {'institutes': institutes,
               'departments': departments,
               'profiles': profiles,
               'banner': get_banner()}

    return render(request, "directory.html", context)

def keyword_list(request):
    # get keywords
    keywords = Keyword.objects.filter(visible=True, frequency__gte=1).order_by('-frequency')

    context = {'keywords': keywords,
               'banner': get_banner()}


    return render(request, "keywords.html", context)