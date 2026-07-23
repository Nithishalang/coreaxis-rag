from src.database.mysql_connection import MySQLConnection
from src.auth.password import PasswordManager
class AuthService:
    def __init__(self):
        self.db = MySQLConnection()
        self.password_manager = PasswordManager()
    def register_user(
        self,
        email: str,
        password: str
    ):
        """
        Register a new user.

        Returns:
            {
                "success": True/False,
                "user_id": int or None,
                "message": str
            }
        """
        connection = self.db.get_connection()
        if connection is None:
            return {
                "success": False,
                "user_id": None,
                "message": "Database connection failed."
            }
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = %s
                """,
                (email,)
            )
            existing_user = cursor.fetchone()
            if existing_user:
                return {
                    "success": False,
                    "user_id": None,
                    "message": "An account with this email already exists."
                }
            password_hash = (
                self.password_manager.hash_password(
                    password
                )
            )
            cursor.execute(
                """
                INSERT INTO users
                (
                    email,
                    password_hash
                )
                VALUES
                (
                    %s,
                    %s
                )
                """,
                (
                    email,
                    password_hash
                )
            )
            connection.commit()
            user_id = cursor.lastrowid
            return {
                "success": True,
                "user_id": user_id,
                "message": "Registration successful."
            }
        except Exception as e:
            connection.rollback()
            print(
                "Registration error:",
                e
            )
            return {
                "success": False,
                "user_id": None,
                "message": "Registration failed."
            }
        finally:
            cursor.close()
            connection.close()
    def login_user(
        self,
        email: str,
        password: str
    ):
        """
        Authenticate an existing user.
        Returns:
            {
                "success": True/False,
                "user_id": int or None,
                "message": str
            }
        """
        connection = self.db.get_connection()
        if connection is None:
            return {
                "success": False,
                "user_id": None,
                "message": "Database connection failed."
            }
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                SELECT
                    id,
                    password_hash
                FROM users
                WHERE email = %s
                """,
                (email,)
            )
            user = cursor.fetchone()
            if user is None:
                return {
                    "success": False,
                    "user_id": None,
                    "message": "Invalid email or password."
                }
            user_id = user[0]
            stored_password_hash = user[1]
            password_valid = (
                self.password_manager.verify_password(
                    password,
                    stored_password_hash
                )
            )
            if not password_valid:
                return {
                    "success": False,
                    "user_id": None,
                    "message": "Invalid email or password."
                }
            return {
                "success": True,
                "user_id": user_id,
                "message": "Login successful."
            }
        except Exception as e:
            print(
                "Login error:",
                e)
            return {
                "success": False,
                "user_id": None,
                "message": "Login failed."
            }
        finally:
            cursor.close()
            connection.close()
