import uuid

import src.models.users.errors as UserErrors
from src.common.database import Database
from src.common.utils import Utils

__author__ = 'Ian'



class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def validate_login(email, password):
        """

        This method verifies that an email/password combo (as sent by the site forms? is valid or not.
        Checks that the email exists, and that the password associated to that email is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one("users", {"email": email})
        if user_data is None:
            raise UserErrors.UserNonexistentError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password is wrong.")

        return True