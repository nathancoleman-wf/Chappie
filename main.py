from lib.chappie import Chappie
from settings import CHECK_MESSAGES_INTERVAL
from settings import CHECK_PULL_REQUESTS_INTERVAL
from settings import USERS

chappie = Chappie(USERS[0], CHECK_MESSAGES_INTERVAL, CHECK_PULL_REQUESTS_INTERVAL)
chappie.start()
