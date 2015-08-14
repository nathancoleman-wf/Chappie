from lib.chappie import Chappie
from settings import CHECK_MESSAGES_INTERVAL
from settings import CHECK_PULL_REQUESTS_INTERVAL

chappie = Chappie('Chappie', CHECK_MESSAGES_INTERVAL, CHECK_PULL_REQUESTS_INTERVAL)
chappie.start()
