from django.shortcuts import *
from django.http import HttpResponse, Http404 ,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from bookmarks.forms import RegistrationForm , BookmarkSaveForm ,SearchForm , MessageForm
from bookmarks.models import Link , Bookmark , Tag , SharedBookmark , Friendship , Message
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime , timedelta
# Create your views here.

def home(request) :
    
    shared_bookmarks=SharedBookmark.objects.order_by('-date')[:10]
    variables=RequestContext(request,{'user':request.user,'shared_bookmarks':shared_bookmarks})
    return render_to_response(u'index.html',variables)





def user_page(request,username):
    
    if request.GET.has_key("message"):
        send_message2(request)
        
    user=get_object_or_404(User,username=username)
    
    friends=[]
    if request.user.is_authenticated():
        friends=get_friends(request)
    bookmarks=user.bookmark_set.order_by('-id')
    
    variables=RequestContext(request,{'user':request.user,'username':user.username,
                                                'bookmarks':bookmarks,
                                                'show_tags':True,
                                                'show_edit':username==request.user.username,
                                                'friends':friends,
                                                })
    
    return render_to_response(u'userPage.html',variables)

def user_redirect(request) :
    if request.user.is_authenticated() :
        return HttpResponseRedirect("/user/"+request.user.username)
    
    return HttpResponseRedirect("/")


def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")

def register_page(request):
    if request.method=='POST' :
        form=RegistrationForm(request.POST)
        
        if form.is_valid() :
            user=User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],\
                                          email=form.cleaned_data['email'])
            return HttpResponseRedirect("/login/")
    else :
        form=RegistrationForm()
    variables=RequestContext(request,{'form':form})

    return render_to_response('registration/register.html',variables)



    
@login_required(login_url='/login/')
def bookmark_save_page(request):
    ajax=request.GET.has_key('ajax')
    if request.method=='POST' :
        form=BookmarkSaveForm(request.POST)
        print request.POST
        if form.is_valid():
            bookmark=_bookmark_save(request,form)
            if ajax:
                variables=RequestContext(request,{'bookmarks':[bookmark],'show_edit':True ,'show_tags':True})
                return render_to_response('bookmarkList.html',variables)
            else :
                return HttpResponseRedirect("/user/%s/" % request.user.username)
        else :
            if ajax :
                return HttpResponse("failure")
    
    elif request.GET.has_key('url'):
        url=request.GET['url']
        title=''
        tags=''
        try :
            link=Link.objects.get(url=url)
            bookmark=Bookmark.objects.get(link=link,user=request.user)
            title=bookmark.title
            tags=''.join(tag.name for tag in bookmark.tag_set.all())
            
            
        except ObjectDoesNotExist :
            pass
        
        form=BookmarkSaveForm({'title':title,'tags':tags,'url':url})
    else :        
        form=BookmarkSaveForm()
    
    variables=RequestContext(request,{'form':form,'user':request.user})
    
    return render_to_response("bookmark_save.html",variables)

    
def _bookmark_save(request,form):
     #create or get link based on url , flag denotes whether link is created or previously existed
    link,flag=Link.objects.get_or_create(url=form.cleaned_data['url'])
            
    #create or get bookmark based on user and link, not checked title 
    bookmark,created=Bookmark.objects.get_or_create(user=request.user ,link=link)
            
    #update title
    bookmark.title=form.cleaned_data['title']
    
    if 'tags' in form.cleaned_data :
        # clear previous tag list
        #if not created :
        #   bookmark.tag_set.clear()
        tag_names=form.cleaned_data['tags'].split()
            
        for tag_name in tag_names :
            tag,created=Tag.objects.get_or_create(name=tag_name)
            tag.save()
            bookmark.tag_set.add(tag)
    
    if form.cleaned_data['share'] :
        shared_bookmark,created=SharedBookmark.objects.get_or_create(bookmark=bookmark)
        
        if created :
            shared_bookmark.users_voted.add(request.user)
            shared_bookmark.save()
                
    bookmark.save()
    
    return bookmark

    
def tag_page(request,tag_name):
    tag=get_object_or_404(Tag,name=tag_name)
    
    bookmarks=tag.bookmarks.order_by("-id")
    
    variables=RequestContext(request,{'bookmarks':bookmarks,'tag_name':tag_name,'show_user':True,'show_tags':False,'user':request.user})
    
    return render_to_response('tag_page.html',variables)

    
    
        
        

def tag_cloud_page(request):
    MAX_WEIGHT=5
    tags=Tag.objects.order_by("name")
    
    min_count=tags[0].bookmarks.count()
    max_count=tags[0].bookmarks.count()
    
    for tag in tags:
        if tag.bookmarks.count() < min_count :
            min_count=tag.bookmarks.count()
        if tag.bookmarks.count() > max_count :
            max_count=tag.bookmarks.count()
        
    count_range = max_count - min_count
    if count_range == 0:
        count_range=1
    
    
    for tag in tags :
        tag.weight=int(1.0*MAX_WEIGHT*(tag.bookmarks.count()-min_count)/count_range)
    
    
    variables=RequestContext(request,{'tags':tags})
    
    return render_to_response('tag_cloud_page.html',variables)
    
    
    
    
def search_page(request):

    bookmarks=[]
    form = None
    show_results = False
    
    if request.GET.has_key('query'):
        show_results=True
        query=request.GET['query'].strip()
        if query:
            form=SearchForm({'query':query})
            bookmarks=Bookmark.objects.filter(title__icontains=query)[:10]
            
    if not form :
        form=SearchForm()
    
    
    variables=RequestContext(request,{'form':form,'bookmarks':bookmarks,'show_results':show_results,
                                      'show_tags':True,'show_user':True})
    
    if request.GET.has_key('ajax'):
        return render_to_response('bookmarkList.html',variables)
    return render_to_response('search_page.html',variables)

@login_required(login_url='/login/')
def vote_page(request):
    if request.GET.has_key('id'):
        try :
            id=request.GET['id']
            shared_bookmark=SharedBookmark.objects.get(id=id)
            user_voted=shared_bookmark.users_voted.filter(username=request.user.username)
            
            if not user_voted:
                shared_bookmark.votes+=1
                shared_bookmark.users_voted.add(request.user)
                shared_bookmark.save()
            
        except ObjectDoesNotExist:
            raise Http404('Bookmark not found.')
        
    if request.META.has_key('HTTP_REFERER'):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    return HttpResponseRedirect("/")


def popular_page(request):
    today=datetime.today()
    yesterday=today-timedelta(1)
    shared_bookmarks=SharedBookmark.objects.filter(date__gt=yesterday)
    shared_bookmarks = shared_bookmarks.order_by('-votes')[:10]
    variables= RequestContext(request,{'shared_bookmarks':shared_bookmarks,'user':request.user})
    
    return render_to_response('popular_page.html',variables)


@login_required(login_url="/login/")
def friend_page(request):
   
    user=request.user
    friends1=Friendship.objects.filter(from_friend=user,invite_status=True)
    friends2=Friendship.objects.filter(to_friend=user,invite_status=True)
    friends=[]
    
    for friend in friends1 :
        friends.append(friend.to_friend)
    
    for friend in friends2 :
        friends.append(friend.from_friend)
    
    
    friend_bookmarks=Bookmark.objects.filter(user__in=friends).order_by('-id')
    
    variables=RequestContext(request,{'bookmarks':friend_bookmarks,'user':request.user,
                                      'friends':friends,'show_tags':True,'show_user':True})
    
    return render_to_response('friend_page.html',variables)

@login_required(login_url="/login/")
def get_friends(request):
    user=request.user
    
    #friends=[ friendship.to_friend for friendship in user.friend_set.all() ]
    
    friend_set=user.friend_set.all()
    friend_set2=user.to_friend_set.all()
    friends=[]
    
    for friendship in friend_set:
        if friendship.invite_status == True :
            friends.append(friendship.to_friend)
    
    for friendship in friend_set2:
        if friendship.invite_status == True :
            friends.append(friendship.to_friend)
    
    
    return friends

def user_list_page(request):
    add_option=False
    flag=False
    if request.user.is_authenticated():
        flag=True
    
    add_option=flag
    
    users=User.objects.exclude(username =request.user.username).order_by("username")
    user_list=[]
    
    friends={}
    friends2={}
    if flag:
        friendships=request.user.friend_set.all()

        for friendship in friendships :
            friends[friendship.to_friend]=friendship.invite_status
      
        friendships2=request.user.to_friend_set.all()
        
        for friendship in friendships2 :
            friends2[friendship.from_friend]=friendship.invite_status
        
        
        
    
    for user in users :
        if user in friends.keys() :
            if friends[user]==True :
                user_list.append((user.username,True,"Friend"))
            else :
                user_list.append((user.username,True,"Invited"))
        
        elif user in friends2.keys() :
            if friends2[user]==True :
                user_list.append((user.username,True,"Friend"))
            else :
                user_list.append((user.username,False,"Accept"))
                
            
        else :
            user_list.append((user.username,False,"Add"))
            
    
    print user_list
    variables=RequestContext(request,{'user_list':user_list,'user':request.user,'add_option':add_option})
    
    return render_to_response("user_list_page.html",variables)
        
@login_required(login_url="/login/")    
def add_friend(request):
    from_user=request.user
    if request.GET.has_key('username'):
        username=request.GET['username']
        
        
        
        to_user=get_object_or_404(User,username=username)
        
        
        friendship = None
        created=False
        
        try :
            friendship=Friendship.objects.get(from_friend=from_user,to_friend=to_user)
        except ObjectDoesNotExist :
            try :
                friendship=Friendship.objects.get(from_friend=to_user,to_friend=from_user)
            except ObjectDoesNotExist :
                friendship=Friendship(from_friend=from_user,to_friend=to_user)
                created=True
        
        
        if not created:
            friendship.invite_status=True
            
        
        friendship.save()       
        
    if request.META.has_key("HTTP_REFERER"):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    return HttpResponseRedirect("/")
    
@login_required(login_url="/login/")    
def send_message(request):
    from_user=request.user
    
    if request.method=="POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            
                to_user=form.cleaned_data['to_user']
            
               
        
                message=Message(content=form.cleaned_data['content'],from_user=from_user,to_user=to_user)
                
                message.save()
                return HttpResponseRedirect("/")
    
    else :
        form=MessageForm({"from_user":from_user.username})
    
    variables=RequestContext(request,{'form':form,'user':request.user})
    
    return render_to_response("message.html",variables)




@login_required(login_url="/login/")  
def send_message2(request):
    #print request
    if request.method=="POST":
        if request.GET.has_key("username"):
            username=request.GET['username']
            to_user=User.objects.get(username=username)
            from_user=request.user
            content=request.POST["content"]
            content=content.strip()
            message=Message(content=content,from_user=from_user,to_user=to_user)
            message.save()
            
            if request.META.has_key("HTTP_REFERER") :
                return HttpResponseRedirect(request.META["HTTP_REFERER"])
            
            return HttpResponseRedirect("/user/"+from_user.username)
            
            
    
    variables=RequestContext(request,{})
    return render_to_response("message_form.html",variables)



@login_required(login_url="/login/")
def received_messages(request):
    user=request.user
    friends=user.to_friend_set.all()
    start=0
    if request.GET.has_key("start"):
        start=int(request.GET["start"])
    
    print start
    
    
    start=max(0,start)
    end=start+5
    
    message_list=Message.objects.filter(to_user=request.user).order_by("-send_time")
    
    end=min(end,len(message_list))
    if start > end :
        start=start-5 
    message_list=message_list[start:end]
    
    variables=RequestContext(request,{'user':request.user,
                                      'message_list':message_list,'start':start
        })
    
    return render_to_response("received_messages.html",variables)
    
@login_required(login_url="/login/")
def chat_page(request):
    friends=get_friends(request)
    
    variables=RequestContext(request,{'user':request.user,
                                      'friends':friends})
    
    return render_to_response("chat_page.html",variables)
    
