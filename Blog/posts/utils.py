import re
from django.utils.html import strip_tags

def count_words(html_string):
    string = strip_tags(html_string)
    num_chinese = len(re.findall(u'[\u4e00-\u9fa5]', string))
    num_english = len(re.findall(r'\b[a-zA-Z.,"]+\b',string))
    return num_chinese, num_english
