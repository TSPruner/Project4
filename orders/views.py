from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

from .models import ChristmasGreen, TreeStand, Bow, Bells, Angel, Star, Bulb, Ribbon, Lights, TableRunner, TreeSkirt, Review, Order

# Create your views here.
def index(request):
    count = 0
    total = 0
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        username = None
        reg_user = False

    if reg_user:
        request.session['order_id'] = 0

        order = Order.objects.filter(username=username).filter(status=1)
        if order.exists():
            request.session['order_id'] = order.first().orderId
            for item in order:
                total = total + item.price
                count = count + 1
            request.session['order_count'] = count
            request.session['order_total'] = str(total)
        else:        
            request.session['order_count'] = 0
            request.session['order_total'] = 0
            found = True
            try:
                order_all = Order.objects.all().order_by('orderId')
            except Order.DoesNotExist:
                request.session['order_id'] = 1
                found = False

            if found:
                if order_all.exists():
                    order_last = order_all.last()
                    request.session['order_id'] =  order_last.orderId + 1
                else:
                    request.session['order_id'] = 1

    menus = [1, 2, 3, 4, 5, 6, 7]
    context = {
        "user": username,
        "reg_user": reg_user,
        "count": count,
        "menus": menus,
        "trees": ChristmasGreen.objects.filter(item="Tree").order_by('greenChoice'),
        "wreaths": ChristmasGreen.objects.filter(item="Wreath").order_by('greenChoice'),
        "garland": ChristmasGreen.objects.filter(item="Garland").order_by('greenChoice'),
        "minitree": ChristmasGreen.objects.filter(item="Minitree").order_by('greenChoice'),
        "centerpieces": ChristmasGreen.objects.filter(item="Centerpiece").order_by('greenChoice'),
        "stands": TreeStand.objects.all(),
        "angel": Angel.objects.exclude(size="Topper"),
        "star": Star.objects.exclude(size="Topper"),
        "bow": Bow.objects.exclude(size="Topper"),
        "bells": Bells.objects.exclude(size="Topper"),
        "bulbs": Bulb.objects.all(),
        "skirts": TreeSkirt.objects.all(),
        "toppersAngel": Angel.objects.filter(size="Topper"),
        "toppersStar": Star.objects.filter(size="Topper"),
        "toppersBow": Bow.objects.filter(size="Topper"),
        "toppersBells": Bells.objects.filter(size="Topper"),
        "ribbon": Ribbon.objects.all(),
        "lights": Lights.objects.all(),
        "runner": TableRunner.objects.all(),
    }
    return render(request, "orders/index.html", context)

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first = request.POST["first"]
        last = request.POST["last"]
        try:
            user = User.objects.get(username=username)
            return render(request, "users/register.html", {"message": "Username already exists."})
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password, first_name=first, last_name=last)
            user.save()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/register.html", {"message": None})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "users/login.html", {"message": "Login with your credentials."})
       
def logout_view(request):
    request.session['order_count'] = 0
    request.session['order_total'] = 0
    request.session['order_id'] = 0
    logout(request)
    return render(request, "users/success.html", {"message": "User has been logged out."})

def review(request, item_id):
    if request.method == "POST":
        username = str(request.user)
        order_id = request.session.get('order_id')

        item_choice = int(request.POST["item-choice"])

        rating = request.POST["rating"]
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        new_review = Review.objects.create(itemChoice=item_choice, rating=rating, comment=comment, username=username, orderId=order_id, itemId=item_id)
        new_review.save()
        return render(request, "orders/success.html", {"message": "Your review has been successfully submitted."})
    else:
        username = request.user
        order_id = request.session.get('order_id')
        submitReview = False
        try:
            reviewFound = Review.objects.get(orderId=order_id, itemId=item_id, username=username)
        except Review.DoesNotExist:
            submitReview = True

        if not submitReview:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Review for this item in this order already submitted by this user. Please try again.",
            }
            return render(request, "orders/error.html", context)  

        itemFound = Order.objects.filter(orderId=order_id).filter(itemId=item_id)
        context = {
            "item_choice": itemFound.first().itemChoice,
            "item_id": item_id,
        }
        return render(request, "orders/review.html", context)

def tree(request):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["treeType"])

        # add tree to order table
        try:
            tree = ChristmasGreen.objects.get(pk=selection)
        except ChristmasGreen.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Tree type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(tree)
        new_order = Order(username=username, itemId=tree.id, price=tree.price, itemChoice=0, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(tree.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "tree": ChristmasGreen.objects.filter(item="Tree").order_by('greenChoice'),
            "reviews": Review.objects.filter(itemChoice=0),
        }

        return render(request, "orders/tree.html", context)
  
def wreath(request):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["wreathType"])

        # add wreath to order table
        try:
            wreath = ChristmasGreen.objects.get(pk=selection)
        except ChristmasGreen.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Wreath type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(wreath)
        new_order = Order(username=username, itemId=wreath.id, price=wreath.price, itemChoice=1, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(wreath.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        wreaths = ChristmasGreen.objects.filter(item="Wreath").order_by('greenChoice')
        context = {
            "wreath": ChristmasGreen.objects.filter(item="Wreath").order_by('greenChoice'),
            "reviews": Review.objects.filter(itemChoice=1),
        }

        return render(request, "orders/wreath.html", context)
  
def garland(request):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["garlandType"])

        # add wreath to order table
        try:
            garland = ChristmasGreen.objects.get(pk=selection)
        except ChristmasGreen.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Garland type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(garland)
        new_order = Order(username=username, itemId=garland.id, price=garland.price, itemChoice=2, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(garland.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "garland": ChristmasGreen.objects.filter(item="Garland").order_by('greenChoice'),
            "reviews": Review.objects.filter(itemChoice=2),
        }

        return render(request, "orders/garland.html", context)
  
def centerpiece(request):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["centerpieceType"])

        # add centerpiece to order table
        try:
            centerpiece = ChristmasGreen.objects.get(pk=selection)
        except ChristmasGreen.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Centerpiece type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(centerpiece)
        new_order = Order(username=username, itemId=centerpiece.id, price=centerpiece.price, itemChoice=3, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(centerpiece.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "centerpiece": ChristmasGreen.objects.filter(item="Centerpiece").order_by('greenChoice'),
            "reviews": Review.objects.filter(itemChoice=3),
        }

        return render(request, "orders/centerpiece.html", context)
  
def miniTree(request):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["miniTreeType"])

        # add MiniTree to order table
        try:
            miniTree = ChristmasGreen.objects.get(pk=selection)
        except ChristmasGreen.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "MiniTree type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(miniTree)
        new_order = Order(username=username, itemId=miniTree.id, price=miniTree.price, itemChoice=4, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(miniTree.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "minitree": ChristmasGreen.objects.filter(item="Minitree").order_by('greenChoice'),
            "reviews": Review.objects.filter(itemChoice=4),
        }

        return render(request, "orders/miniTree.html", context)
  
def stand(request):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["standType"])

        # add stand to order table
        try:
            stand = TreeStand.objects.get(pk=selection)
        except TreeStand.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Tree stand type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(stand)
        new_order = Order(username=username, itemId=stand.id, price=stand.price, itemChoice=5, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(stand.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "stand": TreeStand.objects.order_by('item'),
            "reviews": Review.objects.filter(itemChoice=5),
        }

        return render(request, "orders/stand.html", context)
  
def lights(request, size):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["lightType"])

        # add lights to order table
        try:
            lights = Lights.objects.get(pk=selection)
        except Lights.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Light string type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(lights)
        new_order = Order(username=username, itemId=lights.id, price=lights.price, itemChoice=6, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(lights.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "lights": Lights.objects.filter(size=size).order_by('item'),
            "reviews": Review.objects.filter(itemChoice=6),
            "size": size,
        }

        return render(request, "orders/lights.html", context)
  
def treeSkirt(request):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["skirtType"])

        # add treeSkirt to order table
        try:
            treeSkirt = TreeSkirt.objects.get(pk=selection)
        except TreeSkirt.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Tree Skirt type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(treeSkirt)
        new_order = Order(username=username, itemId=treeSkirt.id, price=treeSkirt.price, itemChoice=7, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(treeSkirt.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "treeSkirt": TreeSkirt.objects.order_by('item'),
            "reviews": Review.objects.filter(itemChoice=7),
        }

        return render(request, "orders/treeSkirt.html", context)
  
def runner(request, size):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["runnerType"])

        # add runner to order table
        try:
            runner = TableRunner.objects.get(pk=selection)
        except TableRunner.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Runner type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(runner)
        new_order = Order(username=username, itemId=runner.id, price=runner.price, itemChoice=8, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(runner.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "runner": TableRunner.objects.filter(size=size).order_by('item'),
            "reviews": Review.objects.filter(itemChoice=8),
            "size": size,
        }

        return render(request, "orders/runner.html", context)

def ribbon(request, size):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["ribbonType"])

        # add ribbon to order table
        try:
            ribbon = Ribbon.objects.get(pk=selection)
        except Ribbon.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Ribbon type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(ribbon)
        new_order = Order(username=username, itemId=ribbon.id, price=ribbon.price, itemChoice=9, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(ribbon.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "ribbon": Ribbon.objects.filter(size=size).order_by('item'),
            "reviews": Review.objects.filter(itemChoice=9),
            "size": size,
        }

        return render(request, "orders/ribbon.html", context)

def angel(request, size):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["angelType"])

        # add angel to order table
        try:
            angel = Angel.objects.get(pk=selection)
        except Angel.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Angel type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(angel)
        new_order = Order(username=username, itemId=angel.id, price=angel.price, itemChoice=10, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(angel.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        if size == "Topper":
            angel = Angel.objects.filter(size="Topper").order_by('item')
            context = {
                "angel": Angel.objects.filter(size="Topper").order_by('item'),
                "reviews": Review.objects.filter(itemChoice=10),
                "size": size,
            }
        else:
            angel = Angel.objects.exclude(size="Topper").order_by('item')
            context = {
                "angel": Angel.objects.exclude(size="Topper").order_by('item'),
                "reviews": Review.objects.filter(itemChoice=10),
                "size": size,
            }

        return render(request, "orders/angel.html", context)

def star(request, size):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["starType"])

        # add star to order table
        try:
            star = Star.objects.get(pk=selection)
        except Star.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Star type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(star)
        new_order = Order(username=username, itemId=star.id, price=star.price, itemChoice=11, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(star.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        if size == "Topper":
            context = {
                "star": Star.objects.filter(size="Topper").order_by('item'),
                "reviews": Review.objects.filter(itemChoice=10),
                "size": size,
            }
        else:
            context = {
                "star": Star.objects.exclude(size="Topper").order_by('item'),
                "reviews": Review.objects.filter(itemChoice=10),
                "size": size,
            }

        return render(request, "orders/star.html", context)

def bow(request, size):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["bowType"])

        # add bow to order table
        try:
            bow = Bow.objects.get(pk=selection)
        except Bow.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Bow type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(bow)
        new_order = Order(username=username, itemId=bow.id, price=bow.price, itemChoice=12, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(bow.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        if size == "Topper":
            context = {
                "bow": Bow.objects.filter(size="Topper").order_by('item'),
                "reviews": Review.objects.filter(itemChoice=10),
                "size": size,
            }
        else:
            context = {
                "bow": Bow.objects.exclude(size="Topper").order_by('item'),
                "reviews": Review.objects.filter(itemChoice=10),
                "size": size,
            }

        return render(request, "orders/bow.html", context)

def bells(request, size):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["bellsType"])

        # add bells to order table
        try:
            bells = Bells.objects.get(pk=selection)
        except Bells.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Bells type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(bells)
        new_order = Order(username=username, itemId=bells.id, price=bells.price, itemChoice=13, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(bells.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        if size == "Topper":
            context = {
                "bells": Bells.objects.filter(size="Topper").order_by('item'),
                "reviews": Review.objects.filter(itemChoice=10),
                "size": size,
            }
        else:
            context = {
                "bells": Bells.objects.exclude(size="Topper").order_by('item'),
                "reviews": Review.objects.filter(itemChoice=10),
                "size": size,
            }

        return render(request, "orders/bells.html", context)

def bulb(request):
    if request.method == "POST":
        username = request.user
        selection = int(request.POST["bulbType"])

        # add bulb to order table
        try:
            bulb = Bulb.objects.get(pk=selection)
        except Bulb.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Bulb type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(bulb)
        new_order = Order(username=username, itemId=bulb.id, price=bulb.price, itemChoice=14, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(bulb.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,            
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "bulb": Bulb.objects.order_by('item'),
            "reviews": Review.objects.filter(itemChoice=14),
        }

        return render(request, "orders/bulb.html", context)

def view_order(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

    username = request.user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "users/register.html", {"message": "User does not exists."})

    found = False
    admin_user = user.is_superuser
    reg_user = not admin_user
    if admin_user:
        order = Order.objects.exclude(status=0).exclude(status=1).order_by('orderId')
        if order.exists():
            found = True
    else:
        order = Order.objects.filter(username=username).exclude(status=0).exclude(status=1).order_by('orderId')
        if order.exists():
            found = True

    if found:
        context = {
            "user": request.user,
            "reg_user": reg_user,
            "submitted": order.filter(status=2).order_by('orderId'),
            "inProgress": order.filter(status=3).order_by('orderId'),
            "assembling": order.filter(status=4).order_by('orderId'),
            "shipped": order.filter(status=5).order_by('orderId'),
            "received": order.filter(status=6).order_by('orderId'),
            "completed": order.filter(status=7).order_by('orderId'),
        }
        return render(request, "orders/viewOrder.html", context)

    context = {
        "reg_user": reg_user,
        "tab": "view",
        "message": "No orders found for user.",
    }
    return render(request, "orders/error.html", context)

def view_cart(request):
    order_id = request.session['order_id'] 
    total = float(request.session['order_total'])
    count = request.session['order_count']

    if request.method == "POST":
        username = request.user
        remove_item = request.POST.get('remove')
        
        item_count = 0
        if remove_item is not None:
            try:
                order = Order.objects.get(pk=remove_item)
            except Order.DoesNotExist:
                context = {
                    "reg_user": True,
                    "tab": "cart",
                    "message": "Item to remove does not exist.",
                }
                return render(request, "orders/error.html", context)

            order.status = 0
            order.save()
            item_count = item_count + 1
            total = total - float(order.price)
            request.session['order_total'] = str(total)
            request.session['order_count'] = count - 1

            if request.session['order_count'] < 1:
                request.session['order_id'] = 0
                return HttpResponseRedirect(reverse("index"))

        return HttpResponseRedirect(reverse("viewCart"))
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

        if count <= 0:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "No items found in cart. Please try again.",
            }
            return render(request, "orders/error.html", context)

        context = {
            "user": request.user,
            "count": count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).filter(status=1).order_by('id'),
            "total": total,
            "reviews": Review.objects.filter(orderId=order_id),
        }
        return render(request, "orders/viewCart.html", context)

def place_order(request):
    username = request.user

    if request.method == "POST":
        order_id = request.session['order_id'] 
        total = float(request.session['order_total'])
        count = request.session['order_count']
        
        try:
            order = Order.objects.filter(orderId=order_id).filter(status=1)
        except Order.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "order",
                "message": "Items to order cannot be found.",
            }
            return render(request, "orders/error.html", context)

        if order.exists():
            for order_next in order:
                if (order_next.status != 0):
                    order_next.status = 2
                    order_next.save()

            request.session['order_id'] = 0
            request.session['order_total'] = 0
            request.session['order_count'] = 0
            return render(request, "orders/success.html", {"message": "Your order has been successfully submitted."})

            context = {
                "reg_user": True,
                "tab": "order",
                "message": "Items to order cannot be found.",
            }
            return render(request, "orders/error.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        
        order_id = request.session['order_id'] 
        total = float(request.session['order_total'])
        count = request.session['order_count']
        
        if count <= 0:
            context = {
                "reg_user": True,
                "tab": "order",
                "message": "No items found in cart. Please try again.",
            }
            return render(request, "orders/error.html", context)

        context = {
            "user": request.user,
            "count": count,
            "orderId": order_id,
            "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": total,
        }
        return render(request, "orders/placeOrder.html", context)

def order_status(request, order_id):
    if request.method == "POST":
        username = request.user
        update_item = request.POST.get('update')
        order_id = request.POST.get('orderId')

        item_count = 0
        if update_item is not None:
            try:
                order = Order.objects.get(pk=update_item)
            except Order.DoesNotExist:
                context = {
                    "reg_user": True,
                    "tab": "status",
                    "message": "Item to remove does not exist.",
                }
                return render(request, "orders/error.html", context)

            index = order.id
            order_id = order.orderId
            order.status = order.status + 1
            order.save()

            if order.status == 7:
                return HttpResponseRedirect(reverse("viewOrder"))

        if order_id is not None:
            return HttpResponseRedirect(reverse("orderStatus", args=(order_id,)))

        context = {
            "user": request.user,
        }
        return render(request, "orders/viewOrder.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})

        if order_id > 0:
            context = {
                "user": request.user,
                "order_id": order_id,
                "order": Order.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            }
        else:
            context = {
                "user": request.user,
                "order_id": order_id,
            }
        return render(request, "orders/orderStatus.html", context)
