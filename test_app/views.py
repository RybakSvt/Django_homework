from django.http import HttpRequest, HttpResponse


from django.http import HttpRequest, HttpResponse


def home_page(request: HttpRequest):
    return HttpResponse(f"""
        <h1 style="color: #008080;">Hello, Guest!</h1>
    """)

def user_page(request: HttpRequest, user_name):
    return HttpResponse(f"""
        <h1 style="color: #008080;">We are glad to see you, {user_name}!</h1>
    """)