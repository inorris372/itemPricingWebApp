import uuid
import src.models.users.constants as UserConstants
import src.models.users.errors as UserErrors
from src.common.database import Database
from src.common.utils import Utils
from src.models.alerts.alert import Alert


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
        hashed_password = Utils.hash_password(password).hexdigest()
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserNonexistentError("Your user does not exist.")
        if not Utils.check_encrypted_password(hashed_password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password is wrong.")

        return True

    # if __name__ == '__main__':
    @staticmethod
    def register_user(email, password):
        """
        This method registers a user using e-mail and password.
        The password already comes hashed as sha-512.
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        hashed_password = Utils.hash_password(password)
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        User(email, Utils.encrypt_password(hashed_password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one('users', {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
