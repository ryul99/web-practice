from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
import json
from json.decoder import JSONDecodeError
from .models import *
from .decorator import *


@allow_request(['POST'])
def signup(request: HttpRequest):
    try:
        req_data = json.loads(request.body.decode())
        username = req_data['username']
        password = req_data['password']
    except (JSONDecodeError, KeyError):
        return HttpResponseBadRequest()

    try:
        User.objects.create_user(
            username=username, password=password)
    except IntegrityError:
        return HttpResponseBadRequest()

    return HttpResponse()


@allow_request(['POST'])
def signin(request: HttpRequest):
    try:
        req_data = json.loads(request.body.decode())
        username = req_data['username']
        password = req_data['password']
    except (JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    
    user = authenticate(request, username=username, password=password)

    if user is None:
        return HttpResponseForbidden()
    
    login(request, user)
    return JsonResponse(user.as_dict())


@allow_request(['GET'])
@authenticate
def signout(request: HttpRequest):
    logout(request)

    return HttpResponse()


@allow_request(['GET', 'POST'])
@authenticate
def post_list(request: HttpRequest):
    if request.method == 'GET':
        posts = [post.as_dict() for post in Post.objects.all()]
        return JsonResponse(posts, safe=False)
    else: # POST
        try:
            req_data = json.loads(request.body.decode())
            title = req_data['title']
            content = req_data['content']
            user = request.user
        except (JSONDecodeError, KeyError, ValueError):
            return HttpResponseBadRequest()

        post = Post(title=title, content=content, user=user)
        post.save()

        return JsonResponse(post.as_dict(), safe=False)


@allow_request(['GET', 'DELETE'])
@authenticate
def post_detail(request: HttpRequest, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()
    if request.method == 'GET':
        return JsonResponse(post.as_dict(), safe=False)
    else: # DELETE
        if post.user != request.user:
            return HttpResponseForbidden()
        post.delete()
        return HttpResponse()


@allow_request(['POST'])
@authenticate
def comment(request: HttpRequest, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponseNotFound()
    try:
        req_data = json.loads(request.body.decode())
        content = req_data['content']
    except (JSONDecodeError, KeyError):
        return HttpResponseBadRequest()
    comment = Comment(user=request.user, content=content, post_id=post_id)
    comment.save()
    return JsonResponse(comment.as_dict(), safe=False)


@allow_request(['DELETE'])
@authenticate
def comment_detail(request: HttpRequest, comment_id):
    try:
        comment = Comment.Objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponseNotFound()
    if comment.user != request.user:
        return HttpResponseForbidden()
    comment.delete()
    return HttpResponse()
    