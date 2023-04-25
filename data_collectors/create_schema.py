from data_collectors.cryptoutils import DBTools

def create_schema():
    try:
        connection = DBTools.get_connection()
        cursor = connection.cursor()
        #create Symbol table and its objects (sequence, index..)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Symbol (
            SymbolId integer,
            Name varchar(50),
            Description varchar(50),
            PRIMARY KEY (SymbolId)
        );
        """)
        cursor.execute("CREATE SEQUENCE  IF NOT EXISTS SEQ_SYMBOL;")
        cursor.execute("CREATE INDEX  IF NOT EXISTS IDX_SYMBOL_NAME ON SYMBOL(NAME);")
        #History data table and its objects
        cursor.execute("""
         CREATE TABLE  IF NOT EXISTS CandleStickHistorical (
            OpenTime timestamp, 
            SymbolId integer NOT NULL,
            OpenPrice FLOAT,
            HighPrice FLOAT,
            LowPrice FLOAT,
            ClosePrice FLOAT,
            BaseVolume FLOAT,
            CloseTime timestamp,
            QuoteVolume FLOAT,
            NumberTrades FLOAT,
            TakerBuyBase FLOAT,
            TakerBuyQuote FLOAT,
            PRIMARY KEY (OpenTime, SymbolId),
            FOREIGN KEY (SymbolId) REFERENCES Symbol(SymbolId)
        );
        """)
        cursor.execute("SELECT create_hypertable('CandleStickHistorical', 'opentime', if_not_exists => TRUE);")
        cursor.execute("CREATE INDEX  IF NOT EXISTS IDX_HIST_OPENTIME ON CandleStickHistorical(OPENTIME)")
        cursor.execute("CREATE INDEX  IF NOT EXISTS IDX_HIST_CLOSETIME ON CandleStickHistorical(CLOSETIME)")
        #real time data table and its objects
        cursor.execute("""
         CREATE TABLE  IF NOT EXISTS CandleStickRealTime (
            OpenTime timestamp, 
            SymbolId integer NOT NULL,
            OpenPrice FLOAT,
            HighPrice FLOAT,
            LowPrice FLOAT,
            ClosePrice FLOAT,
            BaseVolume FLOAT,
            CloseTime timestamp,
            QuoteVolume FLOAT,
            NumberTrades FLOAT,
            TakerBuyBase FLOAT,
            TakerBuyQuote FLOAT,
            PRIMARY KEY (OpenTime, SymbolId),
            FOREIGN KEY (SymbolId) REFERENCES Symbol(SymbolId)
        );
        """)
        cursor.execute("SELECT create_hypertable('CandleStickRealTime', 'opentime', if_not_exists => TRUE);")
        cursor.execute("CREATE INDEX  IF NOT EXISTS IDX_HIST_OPENTIME ON CandleStickRealTime(OPENTIME)")
        cursor.execute("CREATE INDEX  IF NOT EXISTS IDX_HIST_CLOSETIME ON CandleStickRealTime(CLOSETIME)")
        connection.commit()
    finally:
        DBTools.return_connection(connection)


create_schema()
