from pymongo import MongoClient

"""Base de Datos local """
#db_client = MongoClient().local

"""Base de Datos local """

db_client = MongoClient("mongodb+srv://Username:<password>@cluster0.5bw287q.mongodb.net/?retryWrites=true&w=majority").test
