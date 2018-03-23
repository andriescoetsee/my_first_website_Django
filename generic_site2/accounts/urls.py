from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'
urlpatterns = [
    url(r"login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"),name='login'),
    url(r"login/tutor/$", auth_views.LoginView.as_view(template_name="accounts/login_tutor.html"),name='login_tutor'),
    url(r"login/bible_study/$", auth_views.LoginView.as_view(template_name="accounts/login_bible_study.html"),name='login_bible_study'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
	# url(r"signup/ubf_conf/$", views.UBFConfSignUp.as_view(), name="ubf_signup"),
	# url(r"signup/tutor/$", views.TutorSignUp.as_view(), name="tutor_signup"),
	# url(r"signup/bible_study/$", views.BibleStudySignUp.as_view(), name="bible_study_signup"),
	# url(r"signup/ubf_conf/admin/$", views.UBFConfSignUpAdmin.as_view(), name="ubf_signup_admin"),
	# url(r"signup/tutor/admin/$", views.TutorSignUpAdmin.as_view(), name="tutor_signup_admin"),
	# url(r"signup/bible_study/admin/$", views.BibleStudySignUpAdmin.as_view(), name="bible_study_signup_admin"),
]
