import md5

from sqlalchemy import create_session

from zookeepr.lib.base import BaseController, c, redirect_to, session
from zookeepr.models import Person

class retcode:
    """Enumerations of authentication return codes"""
    # daily wtf eat your heart out
    SUCCESS = True
    FAILURE = False
    TRY_AGAIN = 3

class PersonAuthenticator(object):
    """Look up the Person in the data store"""

    def authenticate(self, username, password):
        objectstore = create_session()
        
        ps = objectstore.query(Person).select_by(email_address=email_address)
        
        if len(ps) <> 1:
            return retcode.FAILURE

        password_hash = md5.new(password).hexdigest()
        
        if password_hash == ps[0].password_hash:
            result = retcode.SUCCESS
        else:
            result = retcode.FAILURE
        
        objectstore.close()

        return result


# class AuthenticateValidator(formencode.FancyValidator):
#     def _to_python(self, value, state):
#         if state.authenticate(value['email_address'], value['password']):
#             return value
#         else:
#             raise formencode.Invalid('Incorrect password', value, state)

# class ExistingEmailAddress(formencode.FancyValidator):
#     def _to_python(self, value, state):
#         auth = state.auth
#         if not value:
#             raise formencode.Invalid('Please enter a value',
#                                      value, state)
#         elif not auth.user_exists(value):
#             raise formencode.Invalid('No such user', value, state)
#         return value
    
# class SignIn(formencode.Schema):
#     go = formencode.validators.String()
#     email_address = ExistingEmailAddress()
#     password = formencode.validators.String(not_empty=True)
#     chained_validators = [
#         AuthenticateValidator()
#         ]

# class UserModelAuthStore(object):
#     def __init__(self):
#         self.status = {}
        
#     def user_exists(self, value):
#         session = create_session()
#         ps = session.query(Person).select_by(email_address=value)
#         result = len(ps) > 0
#         return result

#     def sign_in(self, username):
#         self.status[username] = ()

#     def sign_out(self, username):
#         if self.status.has_key(username):
#             del self.status[username]

#     def authorise(self, email_address, role=None, signed_in=None):
#         if signed_in is not None:
#             is_signed_in = False
#             if self.status.has_key(email_address):
#                 is_signed_in = True

#             return signed_in and is_signed_in
        
#         return True

class SecureController(BaseController):
    """Restrict controller access to people who are logged in.

    Controllers that require someone to be logged in can inherit
    from this class instead of `BaseController`.

    As a bonus, they will have access to `c.person` which is a
    `skypanel.model.Person` object that will identify the user
    who is currently logged in.
    """

    def logged_in(self):
        # check that the user is logged in.
        # We can tell if someone is logged in by the presence
        # of the 'person_id' field in the browser session.
        return 'person_id' in session

    def __before__(self, **kwargs):
        # Call the parent __before__ method to ensure the common pre-call code
        # is run
        BaseController.__before__(self, **kwargs)

        if self.logged_in():
            # Retrieve the Person object from the object store
            # and attach it to the magic 'c' global.
            c.person = self.objectstore.get(Person, session['person_id'])
        else:
            # No-one's logged in, so send them to the signin
            # page.
            # If we were being nice and WSGIy, we'd raise a 403 or 401 error
            # (depending) and let a security middleware layer take care
            # of the redirect.  Save that for a rainy day...
            redirect_to(controller='account',
                        action='signin',
                        id=None)
