class Animal:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def call(self,word):
        print(word)

class Dog(Animal):
    def __init__(self,name,age,sex):
        super(Dog,self).__init__(name,age)
        self.sex = sex

dog = Dog("dog",24,"nan")
dog.call("nm")
Dog.call(dog,12)