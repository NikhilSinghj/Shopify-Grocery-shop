from django.http import HttpResponse, HttpResponseBadRequest , JsonResponse
from django.shortcuts import get_object_or_404
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
    

# -----------------------------------------------------Category-----------------------------------------------

from datetime import datetime

def add_category(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            
            category_name = request.POST.get('category_name')
            category_image = request.FILES.get('category_image')
            
            
            if not category_name or not category_image :
                return JsonResponse({'message': 'Missing required field'})
            else:
                Category.objects.create( category_image=category_image,category_name=category_name )
                return JsonResponse({'message': 'Category uploaded successfully'},status=201)
        else:
            return JsonResponse({'message': 'You Are not authenticated'},status=401)
    
    
    
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user.is_superuser:
            load = json.loads(request.body)
            id=load['id']
        
            if not id:
                return JsonResponse({'message': 'Missing required field'}, status=400)
            else:
                category = Category.objects.get(id=id)
                if Category.objects.filter(id=id).exists():  
                    category.deleted_status = True
                    category.category_deleted_date = datetime.now()
                    category.save()
                    return JsonResponse({'message': 'Category deleted successfully'})
                else:
                    return JsonResponse({'message': 'Category id does not exists'})

        return JsonResponse({'message': 'Unauthorized'}, status=401)
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
    
def edit_category(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            
            
            id=request.POST.get('id')
            new_category_name = request.POST.get('category_name')
            # print(new_category_name)
            new_category_image = request.FILES.get('category_image')
            # print(new_category_image)
            
                
            if Category.objects.filter(id=id).exists():
                    
                if new_category_name is not None and new_category_image is not None:
                    category=Category.objects.get(id=id)
                    category.category_name=new_category_name
                    category.category_image=new_category_image
                    category.category_edited_date = datetime.now()
                    category.save()
                    return JsonResponse({'message': 'Category updated successfully'})
                elif new_category_image is not None:
                    category=Category.objects.get(id=id)
                    category.category_image=new_category_image
                    category.category_edited_date = datetime.now()
                    category.save()
                    return JsonResponse({'message': 'Category image updated successfully'})
                else:
                    category=Category.objects.get(id=id)
                    category.category_name=new_category_name
                    
                    
                    category.category_edited_date = datetime.now()
                    category.save()
                    return JsonResponse({'message': 'Category name updated successfully'})
            else:
                return JsonResponse({'message': 'No category found for this id'})
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)
    

def get_category(request):
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            category=list(Category.objects.filter(deleted_status=False).values('id','category_name','category_image'))
            return JsonResponse(category,safe=False)
        else:
            return JsonResponse({'message': 'You Are not authenticated'},status=401)
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)  



# -----------------------------------------------------Items-----------------------------------------------



def add_items(request):
    if request.method == "POST":
        try:
            items_data = {
                
                "product_category": Category.objects.get(id=int(request.POST.get("product_category"))),
                "product_name": request.POST.get("product_name"),
                "price": request.POST.get("price"),
                "unit": request.POST.get("unit"),
                "image": request.FILES.get("image"),
                "product_quantity": request.POST.get("product_quantity"),
                "description": request.POST.get("description"),
                "product_expiry_date": request.POST.get("product_expiry_date"),
                "product_manufacture_date": request.POST.get("product_manufacture_date"),
            }
            
            item = Items(**items_data)
            item.save()

            response_data = {"message": "Item added successfully"}
            return JsonResponse(response_data, status=201)
        
        except Exception as e:
            response_data = {"error": str(e)}
            return JsonResponse(response_data, status=400)
        
    elif request.method == 'DELETE':
        if request.user.is_authenticated and request.user.is_superuser:
            load = json.loads(request.body)
            id=load['id']
        
            if not id:
                return JsonResponse({'message': 'Missing required field'}, status=400)
            else:
                item = Items.objects.get(id=id)
                if Items.objects.filter(id=id).exists():  
                    item.deleted_status = True
                    item.save()
                    return JsonResponse({'message': 'Item deleted successfully'})
                else:
                    return JsonResponse({'message': 'Item id does not exists'})

        return JsonResponse({'message': 'Unauthorized'}, status=401)
    
    elif request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            item=list(Items.objects.filter(deleted_status=False).values())
            return JsonResponse(item,safe=False)
        else:
            return JsonResponse({'message': 'You Are not authenticated'},status=401)
    
    
    else:
        response_data = {"message": "Invalid Request method"}
        return JsonResponse(response_data, status=405)



def get_item(request):
    if request.method == 'GET' :
       
       items=list(Items.objects.filter(deleted_status=False).values())
       return JsonResponse(items,safe=False)
    else:
        return JsonResponse({'messege':'Invalid Request Method'},status=400)



# -----------------------------------------------------Cart-----------------------------------------------

def add_to_cart(request,id):
    product = get_object_or_404(Items,id=id)
    user =request.user
    if request.method=='POST':
        quantity= int(request.post.get('quantity'))
        user_product,created= Order.objects.get_or_create(user=user,product=product)

        if created:
            user_product.ordered_quantity= quantity
        else:
            user_product.ordered_quantity+= quantity

        user_product.save()
        return JsonResponse({'message':'Product added to cart successfully.'})
    elif request.method == 'GET':
        cart_items = Order.objects.filter(user=user)
        cart_data = [{'product_id': item.product.id, 'quantity': item.quantity} for item in cart_items]
        return JsonResponse({'cart_items': cart_data})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)            
    

    





    



def edit_item(request):
    if request.method == "PUT":
        try:
            item_id = int(request.POST.get("item_id"))  
            item = Items.objects.get(id=item_id)

            
            if request.POST.get("product_category"):
                item.product_category = Category.objects.get(id=int(request.POST.get("product_category")))
            if request.POST.get("product_name"):
                item.product_name = request.POST.get("product_name")
            if request.POST.get("price"):
                item.price = request.POST.get("price")
            if request.POST.get("unit"):
                item.unit = request.POST.get("unit")
            if request.FILES.get("image"):
                item.image = request.FILES.get("image")
            if request.POST.get("product_quantity"):
                item.product_quantity = request.POST.get("product_quantity")
            if request.POST.get("description"):
                item.description = request.POST.get("description")
            if request.POST.get("product_expiry_date"):
                item.product_expiry_date = request.POST.get("product_expiry_date")
            if request.POST.get("product_manufacture_date"):
                item.product_manufacture_date = request.POST.get("product_manufacture_date")

            item.save()

            response_data = {"message": "Item updated successfully"}
            return JsonResponse(response_data, status=200)

        except Items.DoesNotExist:
            response_data = {"message": "Item not found"}
            return JsonResponse(response_data, status=404)
        except Exception as e:
            response_data = {"error": str(e)}
            return JsonResponse(response_data, status=400)
    else:
        return JsonResponse({'message': 'Invalid Request Method'}, status=400)








# def add_item(request):
#     if request.method == 'POST':
#         if request.user.is_authenticated and request.user.is_superuser:
#             items=request.POST.get('user_id')
#             product_category= request.POST.get('Product_category')
#             product_name=request.POST.get('product_name')
#             price=request.POST.get('price')
#             unit=request.POST.get('unit')
#             image = request.FILES.get('image')
#             product_quantity=request.POST.get('product_quantity')
#             description=request.POST.get('description')
            

        
#             if not items or not product_category or not product_name or not price or not unit or not image or not product_quantity or not description:
#                 return JsonResponse({'message': 'Missing required field'})
#             else:
        
#                 Items.objects.create(items=items,
#                                      product_category=product_category,
#                                      product_name=product_name,
#                                      price=price,
#                                      unit=unit,
#                                      image=image,
#                                      product_quantity=product_quantity,
#                                      description=description)
#                 return JsonResponse({'message': 'Item uploaded successfully'})
    
#     elif request.method == 'PUT':
#         if request.user.is_authenticated and request.user.is_superuser:
#             items=request.POST.get('user_id')
#             product_category= request.POST.get('Product_category')
#             product_name=request.POST.get('product_name')
#             price=request.POST.get('price')
#             unit=request.POST.get('unit')
#             image = request.FILES.get('image')
#             product_quantity=request.POST.get('product_quantity')
#             description=request.POST.get('description')
#             if not items or not product_category or not product_name or not price or not unit or not image or not product_quantity or not description:
#                 return JsonResponse({'message': 'Missing required field'}, status=400)
#             else:
        
#                 Items.objects.update(items=items,product_category=product_category,product_name=product_name,price=price,unit=unit,image=image,product_quantity=product_quantity,description=description)
#                 return JsonResponse({'message': 'Category uploaded successfully'})
    
            
    
#     elif request.method == 'DELETE':
#         if request.user.is_authenticated and request.user.is_superuser:
#             load = json.loads(request.body)
#             id = load('id')
        
#             if not id:
#                 return JsonResponse({'message': 'Missing required field'}, status=400)
#             else:
        
#                 item = Items.objects.get(id=id)
#                 if Items.objects.filter(id=id).exists():  
#                     item.deleted_status = True
                    
#                     item.save()
#                     return JsonResponse({'message': 'Item deleted successfully'})
#                 else:
#                     return JsonResponse({'message': 'Item id does not exists'})
        
#         return JsonResponse({'message': 'Unauthorized'}, status=401)
#     else:
#         return JsonResponse({'messege':'Invalid Request Method'},status=400)



# import base64


# def get_all_categories(request):
#     categories = Category.objects.all()
#     category_list = []

#     for category in categories:
#         try:
#             category_image = category.category_image
#             if category_image:
#                 with category_image.open() as img:
#                     image_base64 = base64.b64encode(img.read()).decode('utf-8')
#             else:
#                 image_base64 = None
#         except ValueError: 
#             image_base64 = None

#         category_data = {
#             'category_id': category.category_id,
#             'category_name': category.category_name,
#             'category_image': image_base64,
#             'category_added_date': category.category_added_date,
#             'category_deleted_date': category.category_deleted_date,
#             'category_edited_date': category.category_edited_date,
#             'deleted_status': category.deleted_status,
#         }
#         category_list.append(category_data)

#     return JsonResponse(category_list, safe=False)
       





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




