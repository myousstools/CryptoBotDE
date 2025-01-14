from binance import ThreadedWebsocketManager
import psycopg2

from cryptobot.common import DBUtils
from cryptobot.common.cryptoutils import DBConnector, get_symbol_id

api_key = ''
api_secret = ''

configurations = {}
header = ['open_time','open_price','high_price','low_price',
          'close_price','base_volume','close_time','quote_volume',
          'number_trades','taker_buy_base','taker_buy_quote','ignore']

def handle_socket_message(msg):
    content = msg['k']
    if content['x']:
        interval = content['i']
        # format data to insert it in database (table for real time data)
        symbol_id = get_symbol_id(msg['s'])
        line_db = [content['t'],
                   symbol_id,
                   content['o'],
                   content['h'],
                   content['l'],
                   content['c'],
                   content['v'],
                   content['T'],
                   content['q'],
                   content['n'],
                   content['V'],
                   content['Q']]
        insert_data_table(line_db)


def download_realtime_data():
    """
    Store the klines data coming from the websocket
    :return:
    """
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
    # start is required to initialise its internal loop
    twm.start()
    for pair_conf in DBUtils.get_history_configs():
        #save the configuration in the dict and start the socket
        configurations[pair_conf['symbol']+'_'+pair_conf['interval']] = pair_conf
        twm.start_kline_socket(callback=handle_socket_message, symbol=pair_conf['symbol'], interval=pair_conf['interval'])

    twm.join()



def make_filename(symbol, interval):
    return '{}/{}_{}_realtime.csv'.format(configurations[symbol+'_'+interval].destination_dir, symbol, interval)


def insert_data_table(row):
    """
    Store the klines data coming from the websocket into database (table CandlestickRealTime)
    :param row:
    :return:
    """
    try:
        connection = DBConnector.get_data_db_connection()
        cur = connection.cursor()
        insert_query = f"""INSERT INTO CandleStickHistorical 
            VALUES (to_timestamp({row[0]}/1000),{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},
            to_timestamp({row[7]}/1000),{row[8]},{row[9]},{row[10]},{row[11]}) ON CONFLICT DO NOTHING""";
        cur.execute(insert_query)
        cur.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error
    finally:
        DBConnector.return_data_db_connection(connection)
