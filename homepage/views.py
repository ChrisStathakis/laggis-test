from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponseRedirect, redirect, HttpResponse
from django.core.mail import send_mail
from django.views.generic import View, RedirectView, ListView, DetailView
from django.views.generic.edit import FormView
from recipes.models import Recipe, RecipeCategory
from blog.models import *
from .models import *
from newsletter.forms import NewsLetterForm
from contact.models import ReservationInfo, Contact, ContactInfoPage
from contact.forms import ContactFormGr, ContactInfoForm
from django.template.context_processors import csrf
from django.contrib import messages
from django.core.cache import cache
from django.contrib.admin.views.decorators import staff_member_required

CURRENCY = '€'


def initial_data_page():
    currency = CURRENCY
    open_hours = OpenHours.objects.filter(active=True)
    index_page = IndexPage.objects.filter(active=True).last()
    return [currency, open_hours, index_page]


def check_language(request, template_gr, template_en):
    try:
        lang = request.COOKIES['lang']
        if lang == 'en':
            template = '%s'%(template_en)
        else:
            template = '%s'%(template_gr)
    except:
        template = '%s'%(template_gr)
    return template


def throw_cookie(request, template_gr, template_eng, context):
     try:
        lang = request.COOKIES['lang']
        if lang == 'en':
            return render_to_response('%s'%(template_eng), context)
        return render_to_response('%s'%(template_gr), context)
     except:
        response = render_to_response('%s'%(template_gr), context)
        response.set_cookie('lang','gr')
        return response


def switch_to_English_link(request):
    respose = HttpResponseRedirect('/')
    respose.set_cookie('lang', 'en')
    return respose

def switch_to_Greek_link(request):
    respose = HttpResponseRedirect('/')
    respose.set_cookie('lang', 'gr')
    return respose


class Homepage(View):
    form_class = ContactFormGr
    template_name = 'resto/index.html'

    def get(self, request, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        banner = Banner.objects.filter(active=True).last()
        recipes_special = Recipe.my_query.special_item()
        blog = Post.my_query.show_homepage()
        announcements = Post.my_query.active_announcements().last()
        table_open_times = TableOpenTimes.objects.all()
        title, seo_keywords, seo_description = index_page.title, index_page.seo_keywords, index_page.seo_description
        context = locals()
        context.update(csrf(request))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'newsletter' in request.POST:
            form_news = NewsLetterForm(request.POST)
            if form_news.is_valid():
                form_news.save()
                messages.success(request, 'Το email σας αποθηκεύτηκε!')
                return redirect('homepage')
        form = ContactFormGr(request.POST)
        if form.is_valid():
            form.save()
            send_mail('New Reservation', 'Όνομα %s- Ημερομηνία %s -Τηλεφωνο %s'%(form.cleaned_data.get('name'),form.cleaned_data.get('resever_date'), form.cleaned_data.get('phone')),
                      recipient_list=['lirageika@hotmail.gr'],
                      fail_silently=True,
                      from_email='Ημερομηνία %s, Τηλεφ. %s'%(form.cleaned_data.get('resever_date'), form.cleaned_data.get('phone')))
            messages.success(request, 'Σας ευχαριστούμε για την κράτηση, η οποία θα επιβεβαιωθεί με τηλεφωνική επικοινωνία για την καλύτερη εξυπηρέτηση σας .')
            return HttpResponseRedirect('/#my_messages')
        context = locals()
        context.update(csrf(request))
        return render(request, self.template_name, context)


class HomepageEng(View):
    form_class = ContactFormGr
    template_name = 'english/index-en.html'

    def get(self, request, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        banner = Banner.objects.filter(active=True).last()
        recipes_special = Recipe.my_query.special_item()
        blog = Post.my_query.show_homepage_eng()
        announcements = Post.my_query.active_and_english_announcement().last()
        table_open_times = TableOpenTimes.objects.all()
        title, seo_keywords, seo_description = index_page.title_eng, index_page.seo_keywords_eng, index_page.seo_description_eng
        context = locals()
        context.update(csrf(request))
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'newsletter' in request.POST:
            form_news = NewsLetterForm(request.POST)
            if form_news.is_valid():
                form_news.save()
                messages.success(request, 'Thank you for the newsletter sign up!!')
                return HttpResponseRedirect('/en/#my_messages')
        form = ContactFormGr(request.POST)
        if form.is_valid():
            form.save()
            send_mail('New Reservation', 'Όνομα %s- Ημερομηνία %s -Τηλεφωνο %s'%(form.cleaned_data.get('name'),form.cleaned_data.get('resever_date'), form.cleaned_data.get('phone')),
                      recipient_list=['lirageika@hotmail.gr'],
                      fail_silently=True,
                      from_email='Ημερομηνία %s, Τηλεφ. %s'%(form.cleaned_data.get('resever_date'), form.cleaned_data.get('phone')))
            messages.success(request, 'Thank you for the reservation. We will contact you shortly with a  phone confirmation.')
            return HttpResponseRedirect('/en/#my_messages')
        context = locals()
        context.update(csrf(request))
        return render(request, self.template_name, context)


class MenuPage(ListView):
    model = Recipe
    template_name = 'resto/menu.html'

    def get_context_data(self, **kwargs):
        menu_info = MenuPageinfo.objects.filter(active=True).last()
        currency, open_hours, index_page = initial_data_page()
        recipe_categories = RecipeCategory.my_query.active_categories()
        context = locals()
        context.update(super(MenuPage, self).get_context_data(**kwargs))
        return context


class MenuPageEng(ListView):
    model = Recipe
    template_name = 'english/menu_eng.html'
    def get_context_data(self, **kwargs):
        currency = CURRENCY
        menu_info = MenuPageinfo.objects.filter(active=True).last()
        currency, open_hours, index_page = initial_data_page()
        recipe_categories = RecipeCategory.my_query.active_categories()
        context = locals()
        context.update(super(MenuPageEng, self).get_context_data(**kwargs))
        return context


class MenuPageDetails(DetailView):
    model = Recipe
    slug_field = 'slug'
    template_name = 'resto/menu-detail.html'
    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        object = self.object
        recipes = Recipe.my_query.specific_category(id=object.category.id)
        context = locals()
        context.update(super(MenuPageDetails, self).get_context_data(**kwargs))
        return context


class MenuPageDetailsEng(DetailView):
    model = Recipe
    template_name = 'english/menu-detai-eng.html'
    slug_field = 'slug'
    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        object = self.object
        recipes = Recipe.my_query.specific_category(id=object.category.id)
        context = locals()
        context.update(super(MenuPageDetailsEng, self).get_context_data(**kwargs))
        return context


class BlogPageGre(ListView):
    model = Post
    paginate_by = 5
    template_name = 'resto/blog-left-sidebar.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        category = self.request.GET.getlist('category')
        tags = self.request.GET.getlist('tags')
        object_list = self.model.objects.all()
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
        if category:
            object_list = self.model.objects.filter(category__id__in=category)
        if tags:
            object_list = self.model.objects.filter(tags__id__in = tags)
        return object_list

    def get_context_data(self, **kwargs):
        blog_info = BlogPageinfo.objects.filter(active=True).last()
        currency, open_hours, index_page = initial_data_page()
        announcements = self.object_list.filter(announcement=True)
        tags = PostTags.objects.all()
        post_cat = PostCategory.objects.all()
        post_tags = PostTags.objects.all()
        query_filter = self.request.GET.get('query')
        category_filter = self.request.GET.getlist('category')
        tags_filter = self.request.GET.getlist('tags')
        context = locals()
        context.update(super(BlogPageGre, self).get_context_data(**kwargs))
        return context


class BlogPageEng(ListView):
    model = Post
    paginate_by = 10
    template_name = 'english/blog.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        object_list = self.model.my_query.active_and_english_post()
        category = self.request.GET.getlist('category')
        tags = self.request.GET.getlist('tags')
        if query:
            object_list = object_list.filter(title_eng__contains=query)
        if category:
            object_list = self.model.objects.filter(category__id__in=category)
        if tags:
            object_list = self.model.objects.filter(tags__id__in=tags)
        return object_list

    def get_context_data(self, **kwargs):
        blog_info = BlogPageinfo.objects.filter(active=True).last()
        currency, open_hours, index_page = initial_data_page()
        announcements =self.object_list.filter(announcement=True)
        tags = PostTags.objects.all()
        post_cat = PostCategory.objects.all()
        post_tags = PostTags.objects.all()
        category_filter = self.request.GET.getlist('category')
        tags_filter = self.request.GET.getlist('tags')
        context = locals()
        context.update(super(BlogPageEng, self).get_context_data(**kwargs))
        return context


class BlogDetail(DetailView):
    model = Post
    slug_field = 'slug'
    template_name = 'resto/blog-detail.html'

    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        recent_posts = Post.objects.filter(active=True)[0:5]
        context = locals()
        context.update(super(BlogDetail, self).get_context_data(**kwargs))
        return context


class BlogDetailEng(DetailView):
    model = Post
    slug_field = 'slug'
    template_name = 'english/blog-detail.html'

    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        recent_posts = Post.objects.filter(active=True)[0:5]
        context = locals()
        context.update(super(BlogDetailEng, self).get_context_data(**kwargs))
        return context


class ReservationPage(FormView):
    form_class = ContactFormGr
    success_url = '/reservation/'
    template_name = 'resto/reservation.html'
    def send_email(self):
        pass
    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        res_info = ReservationInfo.objects.filter(active=True).last()
        context = locals()
        context.update(csrf(self.request))
        return context
    def form_valid(self, form):
        form.save()
        send_mail('New Reservation', 'Όνομα %s- Ημερομηνία %s -Τηλεφωνο %s'%(form.cleaned_data.get('name'),form.cleaned_data.get('resever_date'), form.cleaned_data.get('phone')),
                      recipient_list=['lirageika@hotmail.gr'],
                      fail_silently=True,
                      from_email='Αυτόματο μήνυμα')
        messages.success(self.request, 'Σας ευχαριστούμε για την κράτηση, η οποία θα επιβεβαιωθεί με τηλεφωνική επικοινωνία για την καλύτερη εξυπηρέτηση σας .')
        return super(ReservationPage, self).form_valid(form)


class ReservationPageEng(FormView):
    form_class = ContactFormGr
    success_url = '/en/reservation/'
    template_name = 'english/reservation-en.html'
    def send_email(self):
        pass
    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        res_info = ReservationInfo.objects.filter(active=True).last()
        context = locals()
        context.update(csrf(self.request))
        return context
    def form_valid(self, form):
        form.save()
        print('here')
        send_mail('New Reservation', 'Όνομα %s- Ημερομηνία %s -Τηλεφωνο %s'%(form.cleaned_data.get('name'),form.cleaned_data.get('resever_date'), form.cleaned_data.get('phone')),
                      recipient_list=['lirageika@hotmail.gr'],
                      fail_silently=True,
                      from_email='Αυτόματο μήνυμα')
        messages.success(self.request, 'Thank you for the reservation. We will contact you shortly with a  phone confirmation.')
        return super(ReservationPageEng, self).form_valid(form)


class ContactPage(FormView):
    form_class = ContactInfoForm
    success_url = '/contact/#my_message'
    template_name = 'resto/contact.html'

    def get_context_data(self, **kwargs):
        contact_info = ContactInfoPage.objects.last()
        currency, open_hours, index_page = initial_data_page()
        context = locals()
        return context

    def form_valid(self, form):
        form.save()
        send_mail('New Contact', 'Όνομα %s - Email %s'%(form.cleaned_data.get('name'), form.cleaned_data.get('email')),
                      recipient_list=['lirageika@hotmail.gr'],
                      fail_silently=True,
                      from_email='%s') % (form.cleaned_data.get('email'))
        messages.success(self.request, 'Σας Ευχαριστούμε για την ερώτηση θα σας απαντήσουμε όσο πιο σύντομα γίνετε!')
        return super(ContactPage, self).form_valid(form)


class ContactPageEng(FormView):
    form_class = ContactInfoForm
    success_url = '/contact'
    template_name = 'english/contact.html'

    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        contact_info = ContactInfoPage.objects.last()
        open_hours = OpenHours.objects.filter(active=True)
        context = locals()
        return context

    def form_valid(self, form):
        form.save()
        send_mail('New Contact', 'Όνομα %s - Email %s'%(form.cleaned_data.get('name'), form.cleaned_data.get('email')),
                      recipient_list=['lirageika@hotmail.gr'],
                      fail_silently=True,
                      from_email='%s') % (form.cleaned_data.get('email'))
        messages.success(self.request, 'Thank you!,We will answer your question shortly')
        return super(ContactPageEng, self).form_valid(form)


@staff_member_required
def cache_clear(request):
    cache.clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


'''
class AboutUs(ListView):
    model = AboutSkills
    template_name = 'resto/about.html'

    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        about = AboutPage.objects.filter(active=True).last()
        services = AboutSkills.objects.filter(active=True, page_related=about)
        banner = AboutBanner.objects.filter(active=True, page_related=about)
        staff = Staff.objects.filter(active=True, page_related=about)
        title, seo_keywords, seo_description = '%s | %s' % (index_page.title, about.title),\
                                               index_page.seo_keywords,\
                                               index_page.seo_description
        context = locals()
        context.update(super(AboutUs, self).get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('about')
        context = locals()
        context.update(csrf(request))
        return render(request, 'resto/about.html', context)


class AboutUsEng(ListView):
    model = AboutSkills
    template_name = 'english/about-en.html'
    def get_context_data(self, **kwargs):
        currency, open_hours, index_page = initial_data_page()
        about = AboutPage.objects.filter(active=True).last()
        services  = AboutSkills.objects.filter(active=True, page_related=about)
        banner = AboutBanner.objects.filter(active=True, page_related=about)
        print(banner)
        staff = Staff.objects.filter(active=True, page_related=about)
        context = locals()
        context.update(super(AboutUsEng, self).get_context_data(**kwargs))
        return context
    def post(self, request, *args, **kwargs):
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('about')
        context = locals()
        context.update(csrf(request))
        return render(request, 'resto/about.html', context)
'''


