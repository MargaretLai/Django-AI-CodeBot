from django.shortcuts import render
from django.contrib import messages
import openai


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
            openai.api_key = "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"

            # Create OpenAI Instance
            openai.Model.list()

            # Make a request
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Respond only with code. Fix this {lang} code: {code}",
                    temperature=0,
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )

                return render(
                    request,
                    "home.html",
                    {"lang_list": lang_list, "response": response, "lang": lang},
                )
            except Exception as e:
                return render(
                    request,
                    "home.html",
                    {"lang_list": lang_list, "response": e, "lang": lang},
                )

    return render(request, "home.html", {"lang_list": lang_list})
