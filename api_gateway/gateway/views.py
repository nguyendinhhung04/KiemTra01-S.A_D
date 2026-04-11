import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import SERVICE_REGISTRY

@csrf_exempt
def proxy_view(request, service_name, path):
    service_config = SERVICE_REGISTRY.get(service_name)
    if not service_config:
        return JsonResponse({"error": f"Service {service_name} not found"}, status=404)

    target_url = f"{service_config['url']}/{path}"
    if request.GET:
        target_url += f"?{request.GET.urlencode()}"

    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}
    
    try:
        response = requests.request(
            method=request.method,
            url=target_url,
            data=request.body,
            headers=headers,
            timeout=service_config['timeout']
        )
        
        # Create a Django response
        proxy_response = HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type')
        )
        
        # Copy relevant headers
        excluded_headers = [
            'content-encoding', 
            'transfer-encoding', 
            'content-length',
            'connection',
            'keep-alive',
            'proxy-authenticate',
            'proxy-authorization',
            'te',
            'trailers',
            'upgrade'
        ]
        for k, v in response.headers.items():
            if k.lower() not in excluded_headers:
                proxy_response[k] = v
                
        return proxy_response

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=502)
