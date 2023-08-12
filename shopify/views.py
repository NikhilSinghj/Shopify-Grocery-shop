from django.http import HttpResponse, HttpResponseBadRequest , JsonResponse

import json
import re
from .models import User 
from .models import Category
from .models import Items
from .models import Order

from django.contrib.auth import authenticate,login,logout




def register_user(request):
    if request.method == 'POST':

        load=json.loads(request.body)

        username = load['username']
        email = load['email']
        password = load['password']
        

        if not username or not email or not email:
            return HttpResponseBadRequest('Missing required fields')
        else:
            if not  re.match("^[a-zA-Z0-9_.-]+$", username):
                return JsonResponse({'message':'Match Your username Requirements'})
            elif not re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',email):
                return JsonResponse({'message':'Match Your email Requirements'})
            
            elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$",password):
                return JsonResponse({'message':'Match Your Password Requirements'})
        
            else:
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'message':'Username Already exists'})
                elif User.objects.filter(email=email).exists():
                    return JsonResponse({'message':'Email Already exists'})
                else:
                    User.objects.create_user(username=username,email=email,password=password)
                    return JsonResponse({'message':'You Are Registered Now'})
               
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)

       
        



def login_user(request):
    
    if request.method == 'POST':

        load=json.loads(request.body)
        username = load['username']
        password = load['password']
        user=authenticate(username=username,password=password)
       
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return JsonResponse({'message':'Superuser logged in','is_superuser':user.is_superuser})
                
            else:
                login(request,user)
                return JsonResponse({'message':'User logged in','is_superuser':user.is_superuser})
            
        else:
            return JsonResponse({'message':'Incorrect Username Or password'},status=401)
        
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
        

def logout_user(request):   
    
    if request.method == 'GET':
        
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message':'User Logged Out Succesfully'})
        else:
            return JsonResponse({'message':'User Is Not Authenticated'},status=401) 
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
    



from datetime import datetime

def add_category(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            # request.COOKIES.get('cookies')
            load=json.loads(request.body.decode('utf-8'))
            category_name = load.get['category_name']
            category_image = request.FILES.get('category_image')
            category_id = load.get['category_id']
            
            if not category_name or not category_image or not category_id:
                return JsonResponse({'message': 'Missing required field'})
            else:
                Category.objects.create( category_image=category_image )
                return JsonResponse({'message': 'Category uploaded successfully'})
        else:
            return JsonResponse({'message': 'You Are not authenticated'},status=401)
    
    elif request.method == 'PUT':
        if request.user.is_authenticated and request.user.is_superuser:
            load = json.loads(request.body)
            category_id=load['category_id']
            new_category_name = load['new_category_name']
            new_category_image = request.FILES.get['new_category_image']
        
            if not new_category_name or not new_category_image or not category_id:
                return JsonResponse({'message': 'Missing required field'}, status=400)
            else:
                if Category.objects.filter(category_id=category_id).exists():
                    Category.objects.create(category_name=new_category_name, category_image=new_category_image,category_edited_date = datetime.now())
                    return JsonResponse({'message': 'Category updated successfully'})
                else:
                    return JsonResponse({'message': 'No category found for thi id'})
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user.is_superuser:
            load = json.loads(request.body)
            category_id=load['category_id']
        
            if not category_id:
                return JsonResponse({'message': 'Missing required field'}, status=400)
            else:
                category = Category.objects.get(category_id=category_id)
                if category.category_id==category_id:  
                    category.deleted_status = True
                    category.category_deleted_date = datetime.now()
                    category.save()
                    return JsonResponse({'message': 'Category deleted successfully'})
                else:
                    return JsonResponse({'message': 'Category id does not exists'})

    return JsonResponse({'message': 'Unauthorized'}, status=401)




def add_item(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            items=request.POST.get('user_id')
            product_category= request.POST.get('Product_category')
            product_name=request.POST.get('product_name')
            price=request.POST.get('price')
            unit=request.POST.get('unit')
            image = request.FILES.get('image')
            product_quantity=request.POST.get('product_quantity')
            description=request.POST.get('description')
            

        
            if not items or not product_category or not product_name or not price or not unit or not image or not product_quantity or not description:
                return JsonResponse({'message': 'Missing required field'})
            else:
        
                Items.objects.create(items=items,product_category=product_category,product_name=product_name,price=price,unit=unit,image=image,product_quantity=product_quantity,description=description)
                return JsonResponse({'message': 'Item uploaded successfully'})
    
    elif request.method == 'PUT':
        if request.user.is_authenticated and request.user.is_superuser:
            items=request.POST.get('user_id')
            product_category= request.POST.get('Product_category')
            product_name=request.POST.get('product_name')
            price=request.POST.get('price')
            unit=request.POST.get('unit')
            image = request.FILES.get('image')
            product_quantity=request.POST.get('product_quantity')
            description=request.POST.get('description')
            if not items or not product_category or not product_name or not price or not unit or not image or not product_quantity or not description:
                return JsonResponse({'message': 'Missing required field'}, status=400)
            else:
        
                Items.objects.update(items=items,product_category=product_category,product_name=product_name,price=price,unit=unit,image=image,product_quantity=product_quantity,description=description)
                return JsonResponse({'message': 'Category uploaded successfully'})
    
            
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user.is_superuser:
            load = json.loads(request.body)
            deleted_status = load('deleted_status')
        
            if not deleted_status:
                return JsonResponse({'message': 'Missing required field'}, status=400)
            else:
        
                item = Items.objects.get()  
                item.deleted_status = True
                item.save()
        
            return JsonResponse({'message': 'Category deleted successfully'})

    return JsonResponse({'message': 'Unauthorized'}, status=401)




def order_item(request):
    if request.method == 'POST':
         load = json.loads(request.body)
         user=load['user_id']
         item=load['item_id']

         

        


# from django.conf import settings
# import os

def get_item(request):
    if request.method == 'GET' :
       items=list(Items.objects.values())
       return JsonResponse(items,safe=False)
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
    

def get_category(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            load=json.loads(request.body)
            cataegory_id=load['category_id']
            # if Category.objects.filter(category_id=cataegory_id).exists():
                






       





# def serve_image(request, image_name):
#     image_path = os.path.join(settings.BASE_DIR, 'static', 'images', image_name)

#     try:
#         with open(image_path, 'rb') as f:
#             image_data = f.read()
#             return HttpResponse(image_data, content_type='image/jpeg')  
#     except FileNotFoundError:
#         return HttpResponse("Image not found", status=404)















# def add_category(request):
#         if request.method == 'POST':
#             if request.user.is_authenticated and request.user.is_superuser:
#                 load=json.loads(request.body)
#                 category_name=load['category_name']
#                 category_image=load['category_image']
#                 if not category_name or not category_image:
#                     return JsonResponse({'message':'Missing required field'})
#                 else:
#                     Category.objects.create(category_name=category_name,category_image=category_image)
#                     return JsonResponse({'message':'Category uploaded Succesfully'})
#         elif request.method == 'PUT':
#             if request.user.is_authenticated and request.user.is_superuser:
#                 load=json.loads(request.body)
#                 deleted_status=load['new_category_name']
            
#                 if not deleted_status:
#                     return JsonResponse({'message':'Missing required field'})
#                 else:
#                     Category.objects.create(deleted_status=True,deleted_date=datetime.now())
#                     return JsonResponse({'message':'Category updated Succesfully'})   
#             else:
#                 return JsonResponse({'message':'User Is Not Authenticated'},status=401)
#         elif request.method == 'DELETE':
#             if request.user.is_authenticated and request.user.is_superuser:
#                 load=json.loads(request.body)
#                 deleted_status=load['Deleted_status']
            
#                 if not deleted_status:
#                     return JsonResponse({'message':'Missing required field'})
#                 else:
#                     Category.objects.create(deleted_status=True,deleted_date=datetime.now())
#                     return JsonResponse({'message':'Category updated Succesfully'})   

#             else:
#                 return JsonResponse({'message':'User Is Not Authenticated'},status=401)
        

        
        
        
# from django.http import JsonResponse
# from .models import Category

# def get_all_categories(request):
#     categories = Category.objects.all()
#     category_list = []
    
#     for category in categories:
#         category_data = {
#             'category_id': category.category_id,
#             'category_name': category.category_name,
#             'category_image': category.category_image.url,
#             'category_added_date': category.category_added_date,
#             'category_deleted_date': category.category_deleted_date,
#             'category_edited_date': category.category_edited_date,
#             'deleted_status': category.deleted_status,
#         }
#         category_list.append(category_data)
    
#     return JsonResponse(category_list, safe=False)


