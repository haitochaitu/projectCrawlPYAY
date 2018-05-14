from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
import requests, re
from django.http import JsonResponse

class Crawl(APIView):
   def post(self, request):
    """read the content from the url"""
    crawling_url = request.data["url"]
    links_list = []
    images_list = []
    combo_dict = {}
    try:
        response = requests.get(crawling_url)
        """Validate the url, skip url's that download files"""
        if ('application' not in response.headers['Content-Type']):
            data = response.text
            soup = BeautifulSoup(data, features="lxml")
            for link in soup.findAll('a', attrs={'href': re.compile("^http[s]?://")}):
                """Skip duplicate url's"""
                if (link.get('href') not in links_list):
                    links_list.append(link["href"])

            for image in soup.findAll('img', attrs={'src': re.compile("(^http[s]?://|/)")}):
                """Skip duplicate images"""
                if (image.get('src') not in images_list):
                    """Validate image has full path or relative path"""
                    if "http" not in image.get('src'):
                        image_url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', crawling_url)
                        image_response = requests.get(str(image_url[0]) + image["src"])
                        """Validate created image path is valid"""
                        if image_response.status_code == 200:
                           images_list.append(str(image_url[0]) + image["src"])
                    else:
                        images_list.append(image["src"])
            """Handling webpage that has no img tags"""
            if not images_list:
                images_list.append("No Images")

            combo_dict["url"] = links_list
            combo_dict["image"] = images_list
            return JsonResponse(combo_dict,  status=status.HTTP_200_OK)
    except Exception as err:
        return Response(str(err), status=status.HTTP_400_BAD_REQUEST)





