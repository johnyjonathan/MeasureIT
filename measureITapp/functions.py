import string
import random
from .models import AllLabs, UserLabs

def generate_id (size = 8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def addCreatedLab(user, id_number):
    add_lab = UserLabs.objects.create(user = user, id_number = id_number)
    add_lab.save()
    pass

