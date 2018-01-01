import os
if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    import google
    google.__path__.append('/home/darthvaddr/Downloads/google-cloud-sdk/platform/google_appengine/google')
from google.appengine.ext import ndb
class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    email = ndb.StringProperty()

class TestSet(ndb.Model):
    testcode = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    batch = ndb.StringProperty()

class FlexQuestion(ndb.Expando):
    testsetkey = ndb.KeyProperty(kind=TestSet)
    marks = ndb.IntegerProperty()
    negativemarks = ndb.IntegerProperty()
    partialmarks = ndb.IntegerProperty()
    attempted = ndb.BooleanProperty(default=False)
