from jug.lib.logger import logger
from jug.dbo.dbc import Dbc


class RankDb():

    def __init__(self):
        # self.config = {}
        # self.html = ''
        # self.url_page = ''  # what url are we at?

        self.db_result = []

    def get_db_result(self):
        return self.db_result

    # public
    def getBSListDb(self, category):

        logger.info("---begin getBSListDb")

        dbo = Dbc()
        dbo.doConnect()

        # category = self.url_page

        query = f"SELECT TITLE, AUTHOR, IMGURL, AMAZONURL, DATETIME FROM IPBRANK WHERE CATEGORY = '{category}' ORDER BY DATETIME DESC, RANK ASC LIMIT 100"

        #$result = dbo::doQuery($query);
        #if (!$result) return false;
        # curs.fetchone()
        # curs.fetchall()
        # curs.fetchmany(size)
        # number_of_rows = cur.rowcount

        try:
            curs = dbo.doQuery(query)
            # While fetchone appears to return in correct format, the type returned is datetime.date, not string;
            # So can't do a comparison later when I convert to a string with same format;
            # What's more, it's a date, not datetime; leaves out hour:minute:second
            # date_str1 = curs.fetchone()[1].date()  # return datetime.date
            result_list = []

            # Do the first row; get the datetime
            f_row = curs.fetchone()
            date_str1 = f_row[4].strftime("%Y-%m-%d %H:%M:%S")
            result_list.append(f_row)

            logger.info(f"db_result: {type(date_str1)}")

            # This continues from 2nd row, not first; Not sure how to reset to first row;
            for row in curs:
                # result_list.append(datetime.datetime.date(row[1]))  # date
                # date_str = row[1].datetime()

                # Get the datetime as string; if the next date is different, then stop
                date_str = row[4].strftime("%Y-%m-%d %H:%M:%S")

                if date_str != date_str1:
                    # logger.info(f"db_result: {date_str} not equal")
                    break
                # result_list.append(row)
                # date_string = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
                # date_string = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                # result_list.append(date_string)
                # result_list.append(date_obj)
                result_list.append(row)


            # This should be all the fiction/nonfiction for a particular day
            # logger.info(f"db_result: {result_list}")

            # reverse our list;
            # self.db_result = result_list.reverse()
            self.db_result = result_list

            # Extract these fields and put in this specific order

            # titleXX
            # XXauthor
            # imgurlXX
            # amazonurlXX

            # for n in len(result_list):
            #   title = result_list[4]
            #   author = result_list[5]
            #   amazonurl = result_list[6]
            #   imgurl = result_list[7]


            '''
              # Strange date in raw format; it has to be translated with strftime;
              # Below is the raw output from the curs after appended to a list;
              # result_list.append(row):
              # Returns a list; each row is a tuple;
              # db_result: [
              (52104, datetime.datetime(2021, 8, 3, 6, 0, 7), 'fiction', 1, 'The Last Thing He Told Me', ' Laura Dave', 'https://www.amazon.com/dp/B08LDY1MKW/', 'https://m.media-amazon.com/images/I/81BdMSuI5ZS.jpg'),
              (52105, datetime.datetime(2021, 8, 3, 6, 0, 7), 'fiction', 2, 'Black Ice', 'Brad Thor', 'https://www.amazon.com/ dp/B08LDWSKZT/', 'https://m.media-amazon.com/images/I/81JFwwMELdL.jpg'),
              (52106, datetime.datetime(2021, 8, 3, 6, 0, 7), 'fiction', 3, 'The Paper Palace', 'Miranda Cowley Heller', 'https://www.amazon.com/dp/B08R96D5FF/', ' https://m.media-amazon.com/images/I/81XXxS1L4iS.jpg'),
              (52107, datetime.datetime(2021, 8, 3, 6, 0, 7), 'fiction ', 4, 'The Cellist', 'Daniel Silva', 'https://www.amazon.com/dp/B08L3NB7FL/', 'https://m.media-amazon.com/image s/I/71LfMuoD+7S.jpg'),
              (52108, datetime.datetime(2021, 8, 3, 6, 0, 7), 'fiction', 5, 'False Witness', 'Karin Sl aughter', 'https://www.amazon.com/dp/B09239CX27/', 'https://m.media-amazon.com/images/I/81-fM8bLdNS.jpg'),
              (521 09, datetime.datetime(2021, 8, 3, 6, 0, 7), 'fiction', 6, 'People We Meet On Vacation', 'Emily Henry', 'https:/ /www.amazon.com/dp/B08FZNYQJC/', 'https://m.media-amazon.com/images/I/81yUZUVyOcS.jpg'),
            '''

        except Exception as e:
            # print(f"Error committing transaction: {e}")
            logger.info(f"XXX!!!!! getBSListDb exception: {e}")

        finally:
            curs.close()
            dbo.doDisconnect()

    # public
    def getAlltimeRankDb(self):

        logger.info("---begin getAlltimeDb")

        dbo = Dbc()
        dbo.doConnect()

        query = "SELECT TITLE, AUTHOR, IMGURL, AMAZONURL FROM ALLTIMERANK ORDER BY RANK ASC"

        try:
            curs = dbo.doQuery(query)
            self.db_result = curs.fetchall()
            # logger.info(f"xxxxxxxxxx {self.db_result}")

            # for n in len(result_list):
            #   title = result_list[2]
            #   author = result_list[3]
            #   amazonurl = result_list[8]
            #   imgurl = result_list[4]


        except Exception as e:
            # print(f"Error committing transaction: {e}")
            logger.info(f"XXX!!!!! getAlltimeRankDb exception: {e}")

        finally:
            curs.close()
            dbo.doDisconnect()