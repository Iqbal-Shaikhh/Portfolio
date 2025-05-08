from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import Contact
from blog.models import Post

# Create your views here.


def about(request):
    return render(request, "home/about.html")


def index(request):
    return render(request, "home/index.html")


def contact(request):
    # messages.success(request, "Welcome to Contact Us !")
    # messages.warning(request, "this is a Warning")
    # messages.error(request, "This is Error")
    # messages.info(request, "This is Information")

    if request.method == 'POST':
        print("WE ARE USING POST REQUEST")

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        # if len(name)<2 or len(email)<2 or len(content)<4 or len(phone)<10:
        if name == "" or email == "" or content == "" or phone == "":
            messages.error(
                request, "Error Encountered. Please Enter the form correctly !")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(
                request, "Your message has been sent Successfully !")
    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']

    if len(query) > 50:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)

        allPosts = allPostsContent.union(allPostsTitle)

    if allPosts.count() == 0:
        print(allPosts.count())
        messages.error(
            request, "No search Result Found! Please Refine your Query")

    context = {'query': query, 'allPosts': allPosts}
    return render(request, 'home/search.html', context)


def handleSignup(request):
    if request.method == 'POST':
        # messages.success(request, "Your Code Paper Account Has been Successfully Created !")
        # get the post parameters
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['passwordConfirm']

        user_name = str(email)

        print(first_name, last_name, email, password, password_confirm)

        # Error during user registration inputs
        if len(user_name) > 20:
            messages.error(request, "User name Must be under 20 words !")
            return redirect('/')

        if password != password_confirm:
            messages.error(request, "Password Confirmation Doesn't matches !")
            return redirect('/')

        # Registering the user

        myuser = User.objects.create_user(user_name, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        messages.success(
            request, "Your Code Paper Account Has been Successfully Created !")
        return redirect("/")
    else:
        return HttpResponse("404 Not Found !")


def handleLogin(request):
    if request.method == 'POST':
        # get the post parameters
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials, Please try Again !")
            return redirect("/")

    return HttpResponse("404 - Not Found !")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out !")
    return redirect("/")
    return HttpResponse("This is Log Out !")