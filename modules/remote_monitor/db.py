"""
This is the consumer class which is writing the
data into the influxdb database server
"""
from influxdb import InfluxDBClient
from abc import ABC
from abc import abstractmethod
from SeriesHelper import RemoteMonitor


class Database(ABC):
    """
    Basic database class that
    can support any database
    """

    def __init__(self, database, **kwargs):
        self.database = database
        # self.attributes = kwargs
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        if not self.validate_database():
            raise NotImplementedError("{} database support is not present yet!!".format(database))

    @property
    def get_database(self):
        """
        Returns the database attributes
        """
        return self.database

    def validate_database(self):
        """
        Check database validity
        """
        if self.database.lower() in ['mongodb', 'influxdb', 'cassandra']:
            return True
        return False

    @abstractmethod
    def write(self, cols, data):
        """
        Creating the database in the derived class
        """
        pass


class Influx(Database):
    db = None

    def __init__(self, database, user, passcode, dbname, **kwargs):
        super(self.__class__, self).__init__(database, **kwargs)
        if self.get_database.lower() != 'influxdb':
            raise AttributeError('Wrong instantiation of database class')
        Influx.db = InfluxDBClient(self.host, self.port, user, passcode, dbname)
        Influx.db.create_database(dbname)
        # // TODO replace with logging
        print("Created database '{0}' at http://{1} named '{2}'".format(self.get_database, self.host, dbname))

    def write(self, cols, data):
        raw_data = dict(zip(cols, data))
        RemoteMonitor(host='test_oztron', **raw_data)
        RemoteMonitor.commit()
