from django.shortcuts import render, redirect
from django.contrib import messages
from openai import OpenAI
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

client = OpenAI(api_key="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")


# Create your views here.
def home(request):
    lang_list = [
        "html",
        "css",
        "javascript",
        "aspnet",
        "bash",
        "c",
        "c#",
        "c++",
        "docker",
        "git",
        "go",
        "http",
        "java",
        "json",
        "kotlin",
        "makefile",
        "mongodb",
        "php",
        "python",
        "jsx",
        "ruby",
        "sass",
        "sql",
        "typescript",
    ]

    lang_list.sort()

    if request.method == "POST":
        code = request.POST["code"]
        lang = request.POST["lang"]

        if lang == "Select Programming Languages":
            messages.success(request, "Please choose a proragmming language!")
            return render(
                request,
                "home.html",
                {"lang_list": lang_list, "code": code, "lang": lang},
            )
        else:
            # OpenAI Key

            # Create OpenAI Instance
            client.models.list()

            # Make a request
            try:
                response = client.completions.create(
                    prompt=f"Respond only with code. Fix this {lang} code: {code}",
                    temperature=0,
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    model="gpt-3.5-turbo-instruct",
                )

                # Parse the response
                # Assuming 'response' is the Completion object
                choices = response.choices
                if choices:
                    generated_text = choices[0].text.strip()
                else:
                    generated_text = "No choices found in the response."

                return render(
                    request,
                    "home.html",
                    {"lang_list": lang_list, "response": generated_text, "lang": lang},
                )
            except Exception as e:
                return render(
                    request,
                    "home.html",
                    {"lang_list": lang_list, "response": e, "lang": lang},
                )

    return render(request, "home.html", {"lang_list": lang_list})


def suggest(request):
    lang_list = [
        "html",
        "css",
        "javascript",
        "aspnet",
        "bash",
        "c",
        "c#",
        "c++",
        "docker",
        "git",
        "go",
        "http",
        "java",
        "json",
        "kotlin",
        "makefile",
        "mongodb",
        "php",
        "python",
        "jsx",
        "ruby",
        "sass",
        "sql",
        "typescript",
    ]

    lang_list.sort()

    if request.method == "POST":
        code = request.POST["code"]
        lang = request.POST["lang"]

        if lang == "Select Programming Languages":
            messages.success(request, "Please choose a proragmming language!")
            return render(
                request,
                "suggest.html",
                {"lang_list": lang_list, "code": code, "lang": lang},
            )
        else:
            # Create OpenAI Instance
            client.models.list()

            # Make a request
            try:
                response = client.completions.create(
                    prompt=f"Respond only with code. {code}",
                    temperature=0,
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    model="gpt-3.5-turbo-instruct",
                )

                # Parse the response
                # Assuming 'response' is the Completion object
                choices = response.choices
                if choices:
                    generated_text = choices[0].text.strip()
                else:
                    generated_text = "No choices found in the response."

                return render(
                    request,
                    "suggest.html",
                    {"lang_list": lang_list, "response": generated_text, "lang": lang},
                )
            except Exception as e:
                return render(
                    request,
                    "suggest.html",
                    {"lang_list": lang_list, "response": e, "lang": lang},
                )

    return render(request, "suggest.html", {"lang_list": lang_list})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not NONE:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect("home")
        else:
            messages.success(request, "Error logging in. Please try again.")
            return redirect("home")
    else:
        return render(request, "home.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out. Have a nice day.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Successfully registered.")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form})
