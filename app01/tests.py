from django.test import TestCase
import re

a = "/index/"
b = '^"/index/"$'
ret = re.match(b, a)
print(ret)
