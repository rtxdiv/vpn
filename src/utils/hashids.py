from hashids import Hashids
import os

hashids = Hashids(
    salt=os.environ['HASHIDS_SALT']
)