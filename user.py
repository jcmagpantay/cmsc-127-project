class User:
    def __init__(self, memberId: int, name: str, gender: str, degreeProgram: str, accessLevel: int, username: str, academicYear: str, semester: int):
        self.__memberId = memberId
        self.__name = name
        self.__gender = gender
        self.__degreeProgram = degreeProgram
        self.__accessLevel = accessLevel
        self.__username = username
        self.__academicYear = academicYear
        self.__semester = semester
    
    def getMemberId(self):
        return self.__memberId
    
    def getName(self):
        return self.__name
    
    def getGender(self):
        return self.__gender
    
    def getDegreeProgram(self):
        return self.__degreeProgram
    
    def getAccessLevel(self):
        return self.__accessLevel
    
    def getUsername(self):
        return self.__username
    
    def getAcademicYear(self):
        return self.__academicYear
    
    def getSemester(self):
        return self.__semester
    
    def setAcademicYear(self, academicYear):
        self.__academicYear = academicYear

    def setSemester(self, semester):
        self.__semester = semester
    
    def setName(self, name):
        self.__name = name
    

