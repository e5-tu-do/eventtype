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

    information = {}

    if "event_number_input" in request.GET:
        information["has_event_number"] = True
        event_number = request.GET["event_number_input"]

        information["event_number"] = event_number

        g = int(event_number[0])
        s = int(event_number[1])
        d = int(event_number[2])
        c = int(event_number[3])
        t = int(event_number[4])
        n = int(event_number[5])
        x = int(event_number[6])
        u = int(event_number[7])

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
    else:
        information["has_event_number"] = False

    template = loader.get_template('resolver/resolve.html')
    context = RequestContext(request, information)
    return HttpResponse(template.render(context))


def builder(request):

    # first we build a dict of the flags we already figure out
    known_flags = request.GET.keys()

    if "g_flag" not in known_flags:
        # this is the easiest flag to figure out.
        single_choice = [
            {"name" : 1, "meaning" : "Event contains a b quark, extracted from a minimum bias sample"},
            {"name" : 2, "meaning" : "Event contains a c quark, extracted from a minimum bias sample"},
            {"name" : 3, "meaning" : "Other events, extracted from a minimum bias sample"},
            {"name" : 4, "meaning" : "non-flavour physics with special generator settings"},
            {"name" : 5, "meaning" : "particle guns"} ,
            {"name" : 6, "meaning" : "machine induced background (MIB) events"},
            {"name" : 9, "meaning" : "real data"}
        ]

        description = "Choose which of the following  choices applies to your decay."
        template = loader.get_template('builder/single_choice.html')
        context = RequestContext(request, {
                                            "single_choice" : single_choice, 
                                            "description" : description, 
                                            "flag_name" : "g_flag", 
                                            "get_dict" : request.GET.items()
                                            })
        return HttpResponse(template.render(context))

    if "s_flag" not in known_flags and "g_flag" in known_flags:
        s_choices = get_s_info_dict(g_flag=int(request.GET["g_flag"]))
        single_choice = []
        for s_flag, values in s_choices.items():
            if values["type"] == "info":
                single_choice.append({"name" : s_flag, "meaning" : values["meaning"]})
        description = "Choose which of the following choices applies to your decay."
        template = loader.get_template('builder/single_choice.html')
        context = RequestContext(request, {
                                            "single_choice" : single_choice, 
                                            "description" : description, 
                                            "flag_name" : "s_flag", 
                                            "get_dict" : request.GET.items()
                                            })
        return HttpResponse(template.render(context))


    if "c_flag" not in known_flags and "g_flag" in known_flags:
        c_choices = get_c_info_dict(g_flag=int(request.GET["g_flag"]))
        single_choice = []
        for flag, values in c_choices.items():
            if values["type"] == "info":
                single_choice.append({"name" : flag, "meaning" : values["meaning"]})
        description = "Choose which of the following choices applies to your decay."
        template = loader.get_template('builder/single_choice.html')
        context = RequestContext(request, {
                                            "single_choice" : single_choice, 
                                            "description" : description, 
                                            "flag_name" : "c_flag", 
                                            "get_dict" : request.GET.items()
                                            })
        return HttpResponse(template.render(context))

    if "d_flag" not in known_flags and "c_flag" in known_flags and "g_flag" in known_flags:
        d_choices = get_d_info_dict(g_flag=int(request.GET["g_flag"]), c_flag=int(request.GET["c_flag"]))
        single_choice = []
        for flag, values in d_choices.items():
            if values["type"] == "info":
                single_choice.append({"name" : flag, "meaning" : values["meaning"]})
        description = "Choose which of the following choices applies to your decay."
        template = loader.get_template('builder/single_choice.html')
        context = RequestContext(request, {
                                            "single_choice" : single_choice, 
                                            "description" : description, 
                                            "flag_name" : "d_flag", 
                                            "get_dict" : request.GET.items()
                                            })
        return HttpResponse(template.render(context))

    if "t_flag" not in known_flags and "c_flag" in known_flags and "g_flag" in known_flags:
        if request.GET["g_flag"] == 6 :
            single_choice = [
                {"meaning" : "Events are produced for both beams", "name" : "0"},
                {"meaning" : "Events are produced for beam 1 (traveling from VeLo to Muon system)", "name" : "1"},
                {"meaning" : "Events are produced for beam 2 (traveling from Muon system to VeLo)", "name" : "2"}
            ]
            template = loader.get_template('builder/single_choice.html')
            context = RequestContext(request, {
                                            "single_choice" : single_choice, 
                                            "description" : "Choose which of the following choices applies to your decay.", 
                                            "flag_name" : "t_flag", 
                                            "get_dict" : request.GET.items()
                                            })
            return HttpResponse(template.render(context))
            
        elif request.GET["g_flag"] == 5: 
                if c_flag == 0:
                    template = loader.get_template('builder/get_four_momentum.html') #gives the last 4 digits -> afterwards we are done
                    # get the four-digit value of the momentum of the particle (The momentum is given in GeV,rounded up)
                    context = RequestContext(request, {"get_dict" : request.GET.items()})
                    return HttpResponse(template.render(context))

                elif c_flag == 1:
                    template = loader.get_template('builder/get_eta_range.html') #gives the last 4 digits -> afterwards we are done
                    context = RequestContext(request, {"get_dict" : request.GET.items()})
                    return HttpResponse(template.render(context))
                elif c_flag in [2,3]:
                    # "flag must be zero"
                    request.GET["c_flag"] = 0
                else:
                    pass # the flag is not defined
        else:
            template = loader.get_template('builder/get_number_charged_particles.html') #gives the last 4 digits -> afterwards we are done
            context = RequestContext(request, {"get_dict" : request.GET.items()})
            return HttpResponse(template.render(context))
    if "n_flag" not in known_flags and  "g_flag" in known_flags  and "c_flag" in known_flags and "s_flag" in known_flags:
        if request.GET["g_flag"] == 6 and request.GET["c_flag"] in [0,1]:  
            template = loader.get_template('builder/get_gas_type.html') #gives the last 4 digits -> afterwards we are done
            context = RequestContext(request, {"get_dict" : request.GET.items()})
            return HttpResponse(template.render(context))
        elif request.GET["g_flag"] == 5 and request.GET["c_flag"] in [2,3]:
            request.GET["n_flag"] = 0
        else:
            template = loader.get_template('builder/get_neutral_decays.html') #gives the last 4 digits -> afterwards we are done
            context = RequestContext(request, {"get_dict" : request.GET.items()})
            return HttpResponse(template.render(context))

    if "x_flag" not in known_flags and "g_flag" in known_flags and "s_flag" in known_flags and "n_flag" in known_flags and "t_flag" in known_flags:
        if not (request.GET["g_flag"] == 5 and (request.GET["t_flag"]!=0 or request.GET["n_flag"]!=0)):
            x_choices = get_x_info_dict(g_flag=int(request.GET["g_flag"]), s_flag=int(request.GET["s_flag"]))
            if x_choices:
                single_choice = []
                for flag, values in x_choices.items():
                    if values["type"] == "info":
                        single_choice.append({"name" : flag, "meaning" : values["meaning"]})
                template = loader.get_template('builder/single_choice.html')
                context = RequestContext(request, {
                                                    "single_choice" : single_choice, 
                                                    "description" : "Choose which of the following choices applies to your decay.", 
                                                    "flag_name" : "x_flag", 
                                                    "get_dict" : request.GET.items()
                                                    })
                return HttpResponse(template.render(context))            
    return render(request, "builder/end.html")

