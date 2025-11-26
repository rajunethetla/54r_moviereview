from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from review.models import Movie_details
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def basic(request):
    return HttpResponse("hello world")


def  movie_info(request):
    movie=request.GET.get("movie")
    date=request.GET.get("date")
    return  JsonResponse({"status":"success","result":{"movie_name":movie,"release_date":date}},status=200)
    
@csrf_exempt
def movies(request):
    if request.method=="GET":
        Movie_info=Movie_details.objects.all()
        movie_list=[]
        for movie in Movie_info:
            movie_list.append({
                "movie_name":movie.movie_name,
                "release_date":movie.release_date,
                "budget":movie.budget,
                "rating":movie.rating
            })
        return JsonResponse({"status":"success","data":movie_list},status=200)
    elif  request.method=="PUT":
        data=json.loads(request.body)
        print("put data:",data)
        ref_id=data.get("id")
        print("referennce id:",ref_id)
        existing_movie=Movie_details.objects.get(id=ref_id)
        if data.get("movie_name"):
            
            new_movie_name=data.get("movie_name")
            existing_movie.movie_name=new_movie_name
            existing_movie.save()
        elif data.get("release_date"):
            
            new_release_date=data.get("release_date")
            existing_movie.release_date=new_release_date
            existing_movie.save()
        elif data.get("budget"):
            
            new_budget=data.get("budget")
            existing_movie.budget=new_budget
            existing_movie.save()
        elif data.get("rating"):
            
            new_rating=data.get("rating")
            existing_movie.rating=new_rating
            existing_movie.save()
        return JsonResponse({"status":"success","message":"movie record updated successfully","data":data},status=200)
    elif request.method=="DELETE":
        data=request.GET.get("id")
        ref_id=int(data)
        existing_movie=Movie_details.objects.get(id=ref_id)
        existing_movie.delete()
        return JsonResponse({"status":"success","message":"movie record deleted succesfully"},status=200)

            
    elif request.method=="POST":
        #data=json.loads(request.body)#whenever  wessed the dataa in jjssson format  we have  to use this
        data=request.POST#when we senddd the daataa in form format we haave to use this
        print(data.get("movie_name"),"hello")
        movie=Movie_details.objects.create(movie_name=data.get("movie_name"),release_date=data.get("release_date"),budget=data.get("budget"),rating=data.get("rating"))
        return JsonResponse({"status":"success","message":"movie record inserted successfully","data":data},status=200)
    return JsonResponse({"error":"error occured"},status=400)

