from fastapi import HTTPException
import psycopg
from infra.models.user import UserCreateDTO, UserReadDTO, LoginDTO


class UserRepo:
    def __init__(self, connection: psycopg.Connection):
        self.conn = connection


    def create_user(self, user: UserCreateDTO):

        query = """
        CALL create_new_user(%s, %s, %s, %s, %s);
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute("SAVEPOINT savepoint_create_user")
            
            cursor.execute(query, (user.name, user.email, user.sex, user.password, "User"))
        except psycopg.errors.UniqueViolation:
            cursor.execute("ROLLBACK TO SAVEPOINT savepoint_create_user")
            raise HTTPException(status_code=409, detail="Пользователь с таким email или login уже существует.")
        except Exception as e:
            cursor.execute("ROLLBACK TO SAVEPOINT savepoint_create_user")
            print(e)
        else:
            cursor.execute("RELEASE SAVEPOINT savepoint_create_user")
        finally:
            cursor.connection.commit()
            cursor.close()

    def get_user_by_id(self, id):
        query = """
        SELECT * FROM users WHERE idUser = %s
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (id,))
        user = cursor.fetchone()
        user = UserReadDTO(**user)
        cursor.close()
        return user
    
    def validate_user(self, data: LoginDTO):
        query = """
        SELECT * FROM autorizarion(%s, %s)
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (data.email, data.password))
        check = cursor.fetchone()
        cursor.close()
        if not check:
            return
        
        query = """
        SELECT iduser FROM users WHERE email = %s
        """

        cursor = self.conn.cursor()
        cursor.execute(query, (data.email,))
        user = cursor.fetchone()
        cursor.close()
        if not user:
            return
        return user
    

    def get_cart(self):
        query = """
        SELECT * FROM cart_user
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        return items
    
    