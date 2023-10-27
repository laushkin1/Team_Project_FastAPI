import re

def extract_tags(text):
    tags = re.findall(r'#\w+', text)
    return tags
