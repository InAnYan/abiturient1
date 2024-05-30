from datetime import datetime
import urllib.request
from lxml.html import parse

from fake_useragent import UserAgent

ua = UserAgent()


text = """
https://www.djangoproject.com/
https://www.javatpoint.com/django-mvt
https://docs.djangoproject.com/en/5.0/intro/tutorial03/
https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
https://opensource.com/article/17/11/django-orm
https://en.wikipedia.org/wiki/Regular_expression
https://medium.com/@alex.kirkup/integerchoices-in-django-models-working-seamlessly-from-the-backend-and-the-frontend-using-labels-a3e77b86d419
https://django-formtools.readthedocs.io/en/latest/wizard.html
https://docs.djangoproject.com/en/5.0/topics/forms/formsets/
https://getbootstrap.com/
https://django-crispy-forms.readthedocs.io/en/latest/
https://jquery.com/
https://en.wikipedia.org/wiki/Ajax_(programming)
https://docxtpl.readthedocs.io/en/latest/
""".strip()


def get_title(link):
    req = urllib.request.Request(
        link, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    page = urllib.request.urlopen(req)
    p = parse(page)
    return p.find(".//title").text


for line in text.split("\n"):
    print(
        f"{get_title(line)}. URL: {line} (дата звернення {datetime.today().strftime('%d.%m.%Y')})."
    )
