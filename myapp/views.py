from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView,ListView,UpdateView,DetailView,DeleteView
from django.urls import reverse_lazy
from myapp.models import Product, Cart
from myapp.forms import ProductForm, SignInForm, SignUpForm
from django.contrib.auth.models import User

class RegistrationView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Account has been created!!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create an account")
        return super().form_invalid(form)

class SignInView(FormView):
    form_class=SignInForm
    template_name="login.html"
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login succesfully")
                return redirect("list")
            messages.error(request,"invalid credentail")
            return render(request,self.template_name,{"form":form})
        
class ProductCreateView(CreateView):
    form_class=ProductForm
    template_name="add_products.html"
    model=Product
    success_url=reverse_lazy("list")

class ProductListView(ListView):
    model=Product
    template_name="list_product.html"
    context_object_name="products"

class ProductDetailView(DetailView):
    model=Product
    template_name="detail_product.html"
    context_object_name="product"

class ProductEditView(UpdateView):
    model=Product
    form_class=ProductForm
    template_name="update_product.html"
    success_url=reverse_lazy("list")

class ProductDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Product.objects.get(id=id).delete()
        return redirect("list")


@login_required
class CartView(View):
    template_name = "cart_view.html"

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, self.template_name, {"cart_items": cart_items})

@login_required
class ManageProductsView(TemplateView):
    template_name = "manage_products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        return context

@login_required
class AddToCartView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            messages.success(request, f"{product.name} added to your cart.")
        except Product.DoesNotExist:
            messages.error(request, "Product does not exist.")
        return redirect("cart_view")

@login_required
class RemoveFromCartView(View):
     def get(self, request, cart_id):
        try:
            cart_item = Cart.objects.get(pk=cart_id, user=request.user)
            cart_item.delete()
            messages.success(request, "Product removed from your cart.")
        except Cart.DoesNotExist:
            messages.error(request, "Cart item does not exist.")
        return redirect("cart_view")
@login_required
class UpdateCartQuantityView(View):
   class UpdateCartQuantityView(View):
    def get(self, request, cart_id, quantity):
        try:
            cart_item = Cart.objects.get(pk=cart_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart item quantity updated.")
        except Cart.DoesNotExist:
            messages.error(request, "Cart item does not exist.")
        return redirect("cart_view")