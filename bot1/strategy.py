#------Do not change those imports------
from pandas import DataFrame
from bot_entity.bot import Bot
import talib.abstract as ta
from technical.util import resample_to_interval, resampled_merge
#---------------------------------------



# Do not change class and methods names

class Strategy(Bot):

    def calc_indicators(self, candles:DataFrame):

        candles[pair] = self.candles[pair].rename(columns={"time": "date"})
        candles[pair]["date"] = to_datetime(self.candles[pair]["date"], unit='s')

        dataframe_long = resample_to_interval(candles, 240)
        dataframe_long['rsi'] = ta.RSI(dataframe_long, timeperiod=9)
        dataframe = resampled_merge(candles, dataframe_long)

        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['ema'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['sma2'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['roc'] = ta.ROC(dataframe, timeperiod=5)

        dataframe['sma1'] = ta.SMA(dataframe, timeperiod=20)
        dataframe['sma3'] = ta.SMA(dataframe, timeperiod=5)
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=166)

        dataframe.fillna(method='ffill', inplace=True)

        return dataframe

    def check_buy_signals(self, indicators):

        buy = False
        # DOWN TREND
        if ((indicators.iloc[-1]['volume'] > 0) &                    
            (indicators.iloc[-1]['close'] > indicators.iloc[-1]['open']) &
            (indicators['rsi'].shift(1).iloc[-1] < indicators.iloc[-1]['rsi']) &
            (((indicators.iloc[-1]['sma'] - indicators['sma'].shift(1).iloc[-1]) / indicators.iloc[-1]['sma']) * 100 > -0.3) &
            (((indicators.iloc[-1]['sma'] - indicators['sma'].shift(1).iloc[-1]) / indicators.iloc[-1]['sma']) * 100 < 0.15)

            ):
            buy = False

        # UP TREND
        if ((indicators.iloc[-1]['volume'] > 0) &
                    (indicators.iloc[-1]['close'] > indicators.iloc[-1]['open']) &
                    (indicators['rsi'].shift(1).iloc[-1] < indicators.iloc[-1]['rsi']) &
                    (((indicators.iloc[-1]['sma'] - indicators['sma'].shift(1).iloc[-1]) / indicators.iloc[-1]['sma']) * 100 >= 0.15)

            ):
            buy = True


        if(
                (indicators.iloc[-1]['resample_240_rsi'] > 110)
            ):

            buy = False
        
        return buy


    def check_sell_signals(self, indicators):
        sell = False
        # UP TREND
        if (
                    (((indicators.iloc[-1]['sma'] - indicators['sma'].shift(1).iloc[-1]) / indicators.iloc[-1]['sma']) * 100 >= 0.15) &
                    (indicators.iloc[-1]['volume'] > 0) &
                    (indicators['rsi'].shift(2).iloc[-1] > indicators['rsi'].shift(1).iloc[-1]) &
                    (indicators['rsi'].shift(1).iloc[-1] > indicators.iloc[-1]['rsi'])

            ):
            sell = True

        if (
                    (indicators['ema'].shift(1).iloc[-1] < indicators.iloc[-1]['ema']) &
                    (indicators['rsi'].shift(1).iloc[-1] > indicators.iloc[-1]['rsi']) &
                    (indicators['sma3'].shift(2).iloc[-1] < indicators['sma3'].shift(1).iloc[-1]) &
                    (indicators['sma3'].shift(1).iloc[-1] < indicators.iloc[-1]['sma3']) &
                    ((indicators.iloc[-1]['rsi'] > 65) |
                     (indicators['rsi'].shift(3).iloc[-1] > 65) |
                     (indicators['rsi'].shift(2).iloc[-1] > 65) |
                     (indicators['rsi'].shift(1).iloc[-1] > 65))
            ):
            dell = True

        # DOWN TREND
        if (
                    (((indicators.iloc[-1]['sma'] - indicators['sma'].shift(1).iloc[-1]) / indicators.iloc[-1]['sma']) * 100 > -0.3) &
                    (((indicators.iloc[-1]['sma'] - indicators['sma'].shift(1).iloc[-1]) / indicators.iloc[-1]['sma']) * 100 < 0.15) &
                    (indicators.iloc[-1]['close'] < indicators.iloc[-1]['open']) &
                    (indicators['close'].shift(1).iloc[-1] < indicators['open'].shift(1).iloc[-1]) &
                    (indicators.iloc[-1]['volume'] > 0) &
                    (indicators['rsi'].shift(1).iloc[-1] > indicators.iloc[-1]['rsi'])
            ):
            sell = True

        if(
                    (indicators['open'].shift(1).iloc[-1] > indicators.iloc[-1]['close']) &
                    (indicators['open'].shift(1).iloc[-1] > indicators['close'].shift(1).iloc[-1]) &
                    (indicators['open'].shift(2).iloc[-1] > indicators['close'].shift(2).iloc[-1]) &
                    (indicators['open'].shift(3).iloc[-1] > indicators['close'].shift(3).iloc[-1]) &
                    (indicators['open'].shift(4).iloc[-1] > indicators['close'].shift(4).iloc[-1]) 
            ):
            sell = True
            
        return sell

