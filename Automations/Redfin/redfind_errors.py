
LOGIN_ERROR_CODE = 'scrapper login error'
SEARCHING_ERROR_CODE = 'scrapper address error'
DATA_FETCHING_ERROR_CODE = 'scrapper image fetching error'
ADDRESS_TYPE_ERROR_CODE = "ADDRESS IDENTIFIER IS NOT 'specific'"

REDFIN_ERROR_CODES = [LOGIN_ERROR_CODE, SEARCHING_ERROR_CODE, DATA_FETCHING_ERROR_CODE, ADDRESS_TYPE_ERROR_CODE]


class RedfinErrors():

    def __init__(self):
        pass

    def match(self, error):
        pass