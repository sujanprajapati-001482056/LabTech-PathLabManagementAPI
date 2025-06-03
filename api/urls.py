from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'medical-histories', views.MedicalHistoryViewSet)
router.register(r'test-categories', views.TestCategoryViewSet)
router.register(r'test-items', views.TestItemViewSet)
router.register(r'test-panels', views.TestPanelViewSet)
router.register(r'test-orders', views.TestOrderViewSet)
router.register(r'test-results', views.TestResultViewSet)
router.register(r'reports', views.ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]