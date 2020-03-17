from .models import Category


def cats(context):
    return {'cats': Category.objects.all()}


