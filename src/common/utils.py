from passlib.hash import pbkdf2_sha512
import hashlib
import re
__author__ = 'Ian'


class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False


    @staticmethod
    def hash_password(password):
        return hashlib.sha512(password.encode('utf-8'))


    @staticmethod
    def encrypt_password(hashed_password):
        """
        Encrypts a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512-pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(hashed_password.hexdigest())


    @staticmethod
    def check_encrypted_password(hashed_password, encrypted_password):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param hashed_password: sha512-hashed password
        :param encrypted_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """

        return pbkdf2_sha512.verify(hashed_password, encrypted_password)

