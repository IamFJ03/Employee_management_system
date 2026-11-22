class RequestLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
        print(request.method)

        response = self.get_response(request)

        print("Response Status:", response.status_code)

        return response