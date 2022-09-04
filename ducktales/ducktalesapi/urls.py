from django.urls import path
from . import views
from django.urls.conf import include


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('calculators/interest', views.CalculatorView.as_view(), name='home'),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path('auth/logout', views.LogoutUserView.as_view(), name='logout'),
    path('recurringexpenses/add', views.RecurringExpensePOST.as_view(), name='recurringexpenseadd'),
    path('recurringexpenses/get', views.RecurringExpenseGET.as_view(), name='recurringexpenseget'),
    path('singleexpenses/add', views.SingleExpensePOST.as_view(), name='singleexpenseadd'),
    path('singleexpenses/sum', views.SingleExpenseSumGET.as_view(), name='singleexpensesum'),
    path('multipleexpenses/sum', views.MultipleExpenseSumGET.as_view(), name='multipleexpensesum'),
    path('allexpenses/get', views.AllExpensesGET.as_view(), name='allexpenses'),
    path('singleexpenses/get', views.SingleExpenseGET.as_view(), name='singleexpenseget'),
    path('patchexpenses/add', views.PatchExpensePOST.as_view(), name='patch_expense'),
    path('singleexpenses/<int:id>/', views.SingleExpenseDELETE.as_view(), name='single'),
    path('recurringexpenses/<int:id>/', views.RecurringExpenseDELETE.as_view(), name='recurring'),
    path('patchexpenses/<int:id>/', views.PatchExpenseDELETE.as_view(), name='patch'),
    path('recurringexpenses/frompatch/<int:id>/', views.RecurringExpenseFromPatchExpense.as_view(), name='multiplefrompatch'),
    path('allexpenses/getlatest/', views.AllExpensesGETLatest.as_view(), name='alllatest'),
    path('patchexpenses/fromrecurring/<int:id>/', views.PatchExpensesFromRecurring.as_view(), name='patchfrommultiple'),


]