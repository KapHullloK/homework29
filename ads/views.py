from django.http import JsonResponse
from django.views import View


class MainView(View):
    def get(self, request):
        try:
            return JsonResponse({"status": "ok"}, status=200)
        except:
            return JsonResponse({"status": "bad"}, status=404)
