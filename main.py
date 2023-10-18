from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from random import randint
import re

engine = create_engine("postgresql://postgres:1400@localhost:5432/users")


Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)


class Employee(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    father_name = Column(String(30), nullable=False)
    password = Column(String(40), nullable=False)
    amount = Column(Integer)

    def id_generator(self):
        id = randint(1001,9999)
        ids = session.query(Employee).all()
        for item in ids:
            if item.id == id:
                id = randint(1001,9999)
            else:
                pass
        print(f"Your New ID: {id}")
        return id
    
    def login(self):
        while True:
            id1 = int(input("Enter Id: "))
            password1 = input("Enter your password: ")
            user = session.query(Employee).all()
            for item in user:
                if item.id == id1 and item.password == password1:
                    return {'name':item.name, 'fname':item.father_name,'id':item.id,'password':item.password,'amount':item.amount}
            else:
                print("\nInvalid Information\n")

    def menu(self):
        print("Press 1 to create account")
        print("Press 2 to login to an account")
        print("Press 3 to all account")
        print("Press 0 to exit.")
    
    def sub_menu(self):
        print("\nPress 1 deposit Cash")
        print("Press 2 Withdraw Cash")
        print("Press 3 Transfer Cash")
        print("Press 4 to Check Balance")
        print("Press 5 to check all details")
        print("Press 6 to Delete your Account")
        print("Press 0 to log out\n")
    
    @staticmethod
    def pass_check():
        pattern = re.compile("(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*.])(?=.*[0-9])")
        while True:
            password = input("Enter Password: ")
            ok = re.search(pattern, password)
            if len(password) >= 8:
                if ok:
                    return password
                else:
                    print("\nPassword should contain at least:\n1 special character\n1 number!\n1 uppercase letter\n"
                        "1 lowercase letter\n")
            else:
                print("\nPassword length less then 8 characters\n")

class User(Employee):
    def create_account(self):
        _name = input("Enter your Name: ")
        _fname = input("Enter your Father name: ")
        _id = self.id_generator()
        _password = self.pass_check()
        _amount = input("Enter initial deposit amount(OPTIONAL): ")
        if not _amount:
            _amount = 0

        return [_name,_fname,_id,_password,int(_amount)]
    
    def del_account(self,info):
        print("Are you Sure!!\n")
        password = input("Enter You Password: ")
        if info["password"] == password:
            users = session.query(Employee).all()
            for user in users:
                if info["password"] == password and info["id"] == user.id:
                    session.delete(user)
                    session.commit()
                    print("\nAccount Deleted Successfully")
                    input("\npress Enter to continue...\n")
                    break
            else:
                print("Incorrect Password\n")
    
    def Deposit(self,info,cash):
        users = session.query(Employee).all()
        for user in users:
            if info["password"] == user.password and info["id"] == user.id:
                user.amount += cash
                session.commit()
                return True
    
    def Withdraw(self,info,cash):
        users = session.query(Employee).all()
        for user in users:
            if info["password"] == user.password and info["id"] == user.id and user.amount >= cash:
                user.amount -= cash
                session.commit()
                return True


if __name__=="__main__":
    while True:
        obj = User()
        obj.menu()
        ch = int(input("\nChoose: "))
        if ch == 1:
            data = obj.create_account()

            user = Employee( id=data[2], name=data[0], father_name=data[1], password=data[3], amount=data[4])
            session.add(user)
            session.commit()
            print("\nAccount Created Successfully!\n")
            input("\npress Enter to continue...")
        elif ch == 2:
            user = User()
            data = user.login()
            if user:
                while True:
                    user.sub_menu()
                    ch2 = int(input("\nChoose: "))
                    if ch2 == 6:
                        user.del_account(data)
                        break
                    elif ch2 == 4:
                        users = session.query(Employee).all()
                        for item in users:
                            if item.id == data["id"] and item.password == data["password"]:
                                print(f"\nYour Current balance is: {item.amount}")
                                input("\npress Enter to continue...")
                    elif ch2 == 5:
                        users = session.query(Employee).all()
                        for item in users:
                            if item.id == data["id"] and item.password == data["password"]:
                                print("\n"*4)
                                print(f"Name:            {item.name}")
                                print(f"Father name:     {item.father_name}")
                                print(f"Id:              {item.id}")
                                print(f"password:        {item.password}")
                                print(f"Amount:          {item.amount}")
                                input("\npress Enter to continue...")

                    elif ch2 == 1:
                        cash = int(input("Enter amount to deposit: "))
                        if user.Deposit(data,cash):
                            print("Deposit Successfull\n")
                            input("\npress Enter to continue...")

                    elif ch2 == 2:
                        cash = int(input("Enter amount to Withdraw: "))
                        if user.Withdraw(data,cash):
                            print("Withdraw Successfull\n")
                            input("\npress Enter to continue...")
                        else:
                            print("\nInSufficient amount!")
                            input("\npress Enter to continue...")
                            continue

                    elif ch2 == 3:
                        switch = True
                        cash = int(input("Enter amount to transfer: "))
                        if user.Withdraw(data,cash):
                            while switch:
                                rec_id = int(input("Enter receiver Id: "))
                                users = session.query(Employee).all()
                                for item in users:
                                    if item.id == rec_id:
                                        item.amount += cash
                                        print("\nTransfer Successfull\n")
                                        input("\npress Enter to continue...")
                                        switch = False
                                        break
                                else:
                                    print("\nInvalid Receiver Info! Error\n")
                                    input("\npress Enter to continue...")
                        else:
                            print("\nInSufficient amount!")
                            input("\npress Enter to continue...")
                            continue

                    elif ch2 == 0:
                        break       
        elif ch == 3:
            users = session.query(Employee).all()
            for item in users:
                print(f"{item.name} , {item.id} , {item.password} , {item.amount}\n")
        elif ch == 0:
            break
        else:
            print("\nInvalid Choice!\n")
