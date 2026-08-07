import random
import string

codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
print(codigo)