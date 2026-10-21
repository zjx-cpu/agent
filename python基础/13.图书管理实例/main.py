from abc import ABC,abstractmethod
import json
from random import choice


#图书
class Book:
    def __init__(self, book_id, title, author, total_num):
        self.book_id = book_id  # 书籍编号
        self.title = title  # 书籍标题
        self.author = author  # 作者
        self.total_num = total_num  # 总数
        self.__avilable = total_num
    def jieshu(self):
        print("借书")
        if self.__avilable >0:
            self.__avilable -= 1
            return  True
        return False
    def huanshu(self):
        print("还书")
        self.__avilable += 1

    def get_avilable(self):
        return self.__avilable
#会员类
#抽象类：只能被继承，不能实例化，规定子类必须实现某些方法
class Human(ABC):
    def __init__(self, id,username,password):
        self.id = id
        self.username = username
        self.__password = password
        self.__books = [] #会员借阅的书籍 **实例自带的内部属性，不需要外部传参**，创建对象的时候，会员一开始**还没有借阅任何书**

    def jieshu(self,book:Book):
        if len(self.__books) >= self.human_bookmax():
            print("借阅上限")
            return False
        if book.jieshu():
            self.__books.append(book)
            print(f"{self.username}{book.title}借阅成功")
            return True
        else:
            print("图书不足")
            return False

    def huanshu(self,book:Book):
        if book in self.__books:
            self.__books.remove(book)
            print(f"成功还书{book.title}")
        else:
            print("还书失败")

    def get_password(self):#获取密码
        return self.__password
    def get_books(self):#获取借书列表
        return self.__books

    # 获取会员获得最大图书数量 必须实现
    @abstractmethod  # 装饰器
    def human_bookmax(self) -> int:
        pass

#普通会员
class Person(Human):
    def human_bookmax(self) -> int:
        return 3


#vip会员
class VIP(Human):
    def __init__(self, id,username,password, vip=1):
        Human.__init__(self,id,username,password)
        self.vip = vip

    def human_bookmax(self)->int:
        return 6+self.vip

#图书管理系统类
class System():
    def __init__(self):
        self.books = {  # 书籍列表----》字典 key:book_id
            "B001": Book("B001", "三体", "刘慈欣", 10),
            "B002": Book("B002", "围城", "钱钟书", 5),
            "B003": Book("B003", "活着", "余华", 8)
        }
        self.persons = {  # 成员列表---》字典 key:user_id
            "U001": Person("U001", "zhangsan", "123456"),
            "U002": VIP("U002", "lisi", "654321", 1)
        }
        self.current_member:Human|None = None  #当前会员

    def login(self):
        while True:
            print("登录")
            id = input("请输入卡号")
            passward = input("输入密码")

            if id not in self.persons:
                print("用户不存在")
                continue
            member = self.persons[id]
            if member.get_password() == passward:
                self.current_member = member
                print(f"登录成功欢迎{member.username}")
                return True
            else:
                print("密码错误")
                continue
    def jieshu(self):
        for book in self.books.values():
            print(f"编号{book.book_id}，作者：{book.title}，总数：{book.total_num}，可用：{book.get_avilable()}")
        id=input("请输入借书编号")
        if id not in self.books:
            print("不存在")
            return
        self.current_member.jieshu(self.books[id])


    def huanshu(self):
        print("已经借的图书：")
        for book in self.current_member.get_books():
            print(f"编号{book.book_id},标题{book.title}")
        id=input("请输入要还的id")
        if id not in self.books:
            print("还书失败")
            return
        self.current_member.huanshu(self.books[id])

    def show(self):
        if len(self.current_member.get_books())>0:
            for book in self.current_member.get_books():
                print(f"编号{book.book_id},标题{book.title}")
        else:
            print("你没有借")
    def run(self):
        if self.login():
            while True:
                print("\n1.借书")
                print("2.还书")
                print("3.已借阅")
                print("4.退出")
                choice=int(input("请选择: "))
                match choice:
                    case 1:
                        self.jieshu()
                    case 2:
                        self.huanshu()
                    case 3:
                        self.show()
                    case 4:
                        print("bye")
                        break
                    case _:
                        print("无效")
if __name__ == '__main__':
    ls=System()
    ls.run()
