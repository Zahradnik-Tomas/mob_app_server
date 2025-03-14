import os
import sqlite3


class DB_handler:
    def __init__(self):
        self.dbLoginName = "uzivatele.db"
        self.dbRegisterName = "cekajici.db"
        if not os.path.isdir("DB"):
            os.mkdir("DB")
        cursor = sqlite3.connect(f"DB/{self.dbLoginName}")
        cursor2 = sqlite3.connect(f"DB/{self.dbRegisterName}")
        for i in (cursor, cursor2):
            try:
                i.execute(
                    "CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
            except sqlite3.OperationalError:
                pass
            finally:
                i.close()

    def VlozCekajiciho(self, username: str, password: str) -> bool:
        if (self.JeUsernameCekajici(username) or self.JeUsernameRegistrovan(username)):
            return False
        cursor = sqlite3.connect(f"DB/{self.dbRegisterName}")
        try:
            cursor.execute("INSERT INTO users(username, password) VALUES(:username, :password)",
                           {"username": username, "password": password})
            cursor.commit()
        finally:
            cursor.close()
            return True

    def VlozUzivatele(self, username: str, password: str) -> bool:
        if (self.JeUsernameRegistrovan(username)):
            return False
        cursor = sqlite3.connect(f"DB/{self.dbLoginName}")
        try:
            cursor.execute("INSERT INTO users(username, password) VALUES(:username, :password)",
                           {"username": username, "password": password})
            cursor.commit()
        finally:
            cursor.close()
            return True

    def SmazCekajiciho(self, id: int):
        cursor = sqlite3.connect(f"DB/{self.dbRegisterName}")
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (str(id),))
            cursor.commit()
        finally:
            cursor.close()

    def SmazVsechnyCekajici(self):
        cursor = sqlite3.connect(f"DB/{self.dbRegisterName}")
        try:
            cursor.execute("DELETE FROM users")
            cursor.commit()
        finally:
            cursor.close()

    def JeUsernameRegistrovan(self, username: str) -> bool:
        cursor = sqlite3.connect(f"DB/{self.dbLoginName}")
        temp = False
        try:
            a = cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            temp = len(a.fetchall()) > 0

        finally:
            cursor.close()
            return temp

    def JeUsernameCekajici(self, username: str) -> bool:
        cursor = sqlite3.connect(f"DB/{self.dbRegisterName}")
        temp = False
        try:
            a = cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            temp = len(a.fetchall()) > 0

        finally:
            cursor.close()
            return temp

    def JeUzivatelRegistrovan(self, username: str, password: str) -> bool:
        cursor = sqlite3.connect(f"DB/{self.dbLoginName}")
        temp = False
        try:
            a = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            temp = len(a.fetchall()) > 0

        finally:
            cursor.close()
            return temp

    def JeUzivatelCekajici(self, username: str, password: str) -> bool:
        cursor = sqlite3.connect(f"DB/{self.dbRegisterName}")
        temp = False
        try:
            a = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            temp = len(a.fetchall()) > 0

        finally:
            cursor.close()
            return temp

    def VratCekajici(self) -> list[int, str, str]:
        cursor = sqlite3.connect(f"DB/{self.dbRegisterName}")
        temp = []
        try:
            temp = cursor.execute("SELECT * FROM users").fetchall()
        finally:
            cursor.close()
            return temp

    def VratCekajiciho(self, id: int) -> list[str, str]:
        cursor = sqlite3.connect(f"DB/{self.dbRegisterName}")
        temp = []
        try:
            temp = cursor.execute("SELECT username, password FROM users WHERE id = ?", (id,)).fetchall()
        finally:
            cursor.close()
            return temp

    def PotvrdCekajiciho(self, id: int):
        temp = self.VratCekajiciho(id)
        if len(temp) == 0:
            return
        self.SmazCekajiciho(id)
        self.VlozUzivatele(temp[0][0], temp[0][1])
