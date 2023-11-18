from pymongo import MongoClient

"""Base de Datos local """
#db_client = MongoClient().local

"""Base de Datos local """

db_client = MongoClient("mongodb+srv://Luigino95:The_rg95!$@cluster0.5bw287q.mongodb.net/?retryWrites=true&w=majority").test