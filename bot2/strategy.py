#------Do not change those imports------
from pandas import DataFrame
from bot_entity.bot import Bot
import talib.abstract as ta
from technical.util import resample_to_interval, resampled_merge
#---------------------------------------



# Do not change class and methods names

class Strategy(Bot):

    def calc_indicators(self, candles:DataFrame):
        candles['rsi'] = ta.RSI(candles, timeperiod=14)
        return candles

    def check_buy_signals(self, indicators):
        if indicators.iloc[-1]['rsi'] > 70:
            return True
        else:
            return False
        

    def check_sell_signals(self, indicators):
        if indicators.iloc[-1]['rsi'] < 30:
            return True
        else:
            return False

