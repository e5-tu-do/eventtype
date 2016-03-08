from django.shortcuts import render
from resolver.event_type_parser import *
from django.template import loader, RequestContext
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,"resolver/index.html")

def about(request):
    return render(request, "resolver/about.html")


def resolve(request):
    event_number = request.GET["event_number_input"]
    g = int(event_number[0])
    s = int(event_number[1])
    d = int(event_number[2])
    c = int(event_number[3])
    t = int(event_number[4])
    n = int(event_number[5])
    x = int(event_number[6])
    u = int(event_number[7])

    information = {}

    information["g"] = get_g_info(g)
    information["s"] = get_s_info(s_flag=s, g_flag=g)
    information["d"] = get_d_info(d_flag=d, g_flag=g, c_flag=c)
    information["c"] = get_c_info(c_flag=c, g_flag=g)
    information["t"] = get_t_info(t_flag=t, g_flag=g, c_flag=c)
    information["n"] = get_n_info(n_flag=n, g_flag=g, c_flag=c, s_flag=s)
    information["x"] = get_x_info(x_flag=x, g_flag=g, s_flag=s)
    information["u"] = get_u_info()

    information["g"]["flag"] = g
    information["s"]["flag"] = s
    information["d"]["flag"] = d
    information["c"]["flag"] = c
    information["t"]["flag"] = t
    information["n"]["flag"] = n
    information["x"]["flag"] = x
    information["u"]["flag"] = u


    template = loader.get_template('resolver/resolve.html')
    context = RequestContext(request, information)
    return HttpResponse(template.render(context))
