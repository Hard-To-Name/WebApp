from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.forms import SearchForm, RemoveForm
import app.Websoc as websoc

# Create your views here.
def index(request):
    return render(request, "index.html")

def selected(request):
    return render(request, "selected.html", {'courses':update_selected("", "", "")})

def schedule(request):
    return render(request, "schedule.html")

def toolbox(request):
    return render(request, "toolbox.html")

def deptcode_list(dept_or_index, c_code):
    # add course and return the list of course codes
    # dept + c_code combination / index alone / both default
    cache = open("app/static/cache.txt", "r+")
    text = cache.readlines()
    if dept_or_index != "" and c_code != "": # combination
        form = dept_or_index + " " + c_code + "\n"
        print(form, '\n', text)
        if form not in text:
            text.append(form)
            cache.writelines(text)
    elif c_code == "" and dept_or_index != "": # index
        del text[dept_or_index - 1]
        cache.writelines(text)
    cache.close()
    return text

def generate_template(info:list, dept:str, c_index:int):
    template = open("app/static/template.txt", "r")
    html_text = "".join(template.readlines())
    # course_num, course_code, type, waitlist, status
    return html_text.format(c_index, dept, info[0], info[1], info[2], info[3], info[4], c_index)

def update_selected(dept, c_num, c_code):
    db = websoc.MySQLdb.connect(host = "localhost",
                         user = "root",
                         passwd = "1a2b3c4d5e!",
                         db = "uci_course")
    cur = db.cursor()

    #info_list = websoc.search(dept, c_num, c_code, cur)
    #db.commit()

    result  = []
    c_index = 0
    dc_list = deptcode_list(dept, c_code)
    for dc in dc_list:
        c_index += 1
        dc_pair = [dc[0:-6], dc[-6:-1]]
        cur.execute("SELECT * FROM {} WHERE course_code = '{}'"\
            .format(websoc.dept_format(dc_pair[0]), dc_pair[1]))
        search_result = cur.fetchall()[0]
        result.append(generate_template(search_result, dc_pair[0], c_index))

    db.close()

    result_text = "\n".join(result)
    return result_text
    

def search(request):
    dept = ""
    c_num = ""
    c_code = ""

    if request.method == "POST":
        # Get the posted search form
        sf = SearchForm(request.POST)
        if sf.is_valid():
            dept = sf.cleaned_data["dept"]
            c_num = sf.cleaned_data["c_num"]
            c_code = sf.cleaned_data["c_code"]
    else:
        sf = SearchForm()

    return render(request, "selected.html", {'courses':update_selected(dept, c_num, c_code)})

@csrf_exempt
def remove_element(request):
    if request.method == "POST":
        # Get the posted remove form
        rf = RemoveForm(request.POST)
        if rf.is_valid():
            index = rf.cleaned_data["index"]
    else:
        rf = RemoveForm()
    return render(request, "selected.html", {'courses':update_selected(index, "", "")})