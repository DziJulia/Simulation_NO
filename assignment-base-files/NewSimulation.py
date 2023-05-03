class Simulation1:
    def __init__(self, close_values, weights):
        self.totalNet = 0
        self.weight = weights
        self.total = 0
        self.list = []
        self.funds = [2000, 2000, 2000, 2000, 2000]

        self.bitcoin_buy_weight = self.weight[0]
        self.dodgecoin_buy_weight = self.weight[2]
        self.ethereum_buy_weight = self.weight[4]
        self.litecoin_buy_weight = self.weight[6]
        self.xrp_buy_weight = self.weight[8]

        self.bitcoin_sell_weight =  self.weight[1]
        self.dodgecoin_sell_weight = self.weight[3]
        self.ethereum_sell_weight = self.weight[5]
        self.litecoin_sell_weight =  self.weight[7]
        self.xrp_sell_weight =  self.weight[9]

        self.coin = [0, 0, 0, 0, 0]
        # Name of currency
        self.nameCurrency = ['BitCoin', 'DogeCoin', 'Ethereum', 'LiteCoin', 'XRP']
        self.price_per_coin = [0, 0, 0, 0, 0]
        self.closing_value = close_values
        self.funds_per_slot = [2000, 2000, 2000, 2000, 2000]
        self.capital_gain = 0
        self.remaining = 0
        # initialize array for adding currency i bought
        self.coin_bought = []
        self.tax = 0

    def determineBuySignals(self, bitcoin, dogecoin, ethereum, litecoin, xrp, day):
        i = 0
        buy = [0, 0, 0, 0, 0]
        while i < len(self.bitcoin_buy_weight):
            if bitcoin[day][i] > self.bitcoin_buy_weight[i]:
                buy[0] += 1
            if dogecoin[day][i] > self.dodgecoin_buy_weight[i]:
                buy[1] += 1
            if ethereum[day][i] > self.ethereum_buy_weight[i]:
                buy[2] += 1
            if litecoin[day][i] > self.litecoin_buy_weight[i]:
                buy[3] += 1
            if xrp[day][i] > self.xrp_buy_weight[i]:
                buy[4] += 1
            i += 1
        return buy

    def determineSellSignals(self, bitcoin, dogecoin, ethereum, litecoin, xrp, day):
        i = 0
        sell = [0, 0, 0, 0, 0]
        while i < len(self.bitcoin_sell_weight):
            if bitcoin[day][i] <= self.bitcoin_sell_weight[i]:
                sell[0] += 1
            if dogecoin[day][i] <= self.dodgecoin_sell_weight[i]:
                sell[1] += 1
            if ethereum[day][i] <= self.ethereum_sell_weight[i]:
                sell[2] += 1
            if litecoin[day][i] <= self.litecoin_sell_weight[i]:
                sell[3] += 1
            if xrp[day][i] <= self.xrp_sell_weight[i]:
                sell[4] += 1
            i += 1
        return sell

    def sellCoin(self, index, close_value):
        return close_value - self.price_per_coin[index]

    def sellCurrency(self, currency, buy_signals, sell_signals, day):
        if buy_signals <= sell_signals:
            if self.nameCurrency[currency] in self.coin_bought:
                current = self.coin[currency]
                self.coin_bought.remove(self.nameCurrency[currency])
                self.funds[currency] += self.coin[currency] * self.closing_value[currency][day]
                profit = self.sellCoin(currency, self.closing_value[currency][day])
                self.capital_gain = profit * self.coin[currency]
                self.price_per_coin[currency] = self.closing_value[currency][day]
                self.coin[currency] = 0
                if profit > 0:
                    calculate = (self.capital_gain / 100) * 33
                    self.tax += calculate
                sell = "->Sold " + str(current) + " for " + str(self.closing_value[currency][day]) + " per coin"
                sellNext = "Profit per coin -> " + str(profit) + " profit total -> " + str(self.capital_gain)
                self.list.append(sell)
                self.list.append(sellNext)

    # def reset(self):
    # method for calculate maximum coins what im able to buy
    def getMaxcoin(self, available, coins):
        mod = (available / coins)
        self.remaining = int(mod) * coins
        # casting it in int due we want full coin
        return int(mod)

    def purchaseCurrency(self, currency, buy_signals, sell_signals, day):
        if buy_signals > sell_signals:
            if self.nameCurrency[currency] not in self.coin_bought:
                if self.closing_value[currency][day] > 0.01:
                    value = self.getMaxcoin(self.funds[currency], self.closing_value[currency][day])
                    purchache = "->Purchased " + str(value) + " for " + str(
                        self.closing_value[currency][day]) + " per coin"
                    self.list.append(purchache)
                    self.coin_bought.append(self.nameCurrency[currency])
                    self.funds[currency] = self.funds[currency] - self.remaining
                    self.coin[currency] = value
                    self.price_per_coin[currency] = self.closing_value[currency][day]

    def profitLoss(self, currency_closing, day):
        profit_loss = []
        i = 1
        while i <= 128:
            if self.closing_value[currency_closing][day - i] == 0:
                profit_loss.append(0)
            else:
                p = (self.closing_value[currency_closing][day] - self.closing_value[currency_closing][day - i]) / \
                    self.closing_value[currency_closing][day - i]
                profit_loss.append(p)
            i *= 2
        return profit_loss

    def precalculateProfitLoss(self, currency_closing):
        my_list = []
        for i in range(128, 2991):
            my_list.append(self.profitLoss(currency_closing, i))
        return my_list

    # def displayValueGraph(self):

    def simulate(self):
        day = 128
        number = 0
        bitCoin = self.precalculateProfitLoss(0)
        dogecoin = self.precalculateProfitLoss(1)
        ethereum = self.precalculateProfitLoss(2)
        litecoin = self.precalculateProfitLoss(3)
        xrp = self.precalculateProfitLoss(4)

        while day in range(128, 2991):
            index = 0
            daystring = '==== day ' + str(day) + ' ===='
            self.list.append(daystring)
            while index < len(self.nameCurrency):
                buy_signals = self.determineBuySignals(bitCoin, dogecoin, ethereum, litecoin, xrp, number)[index]
                sell_signals = self.determineSellSignals(bitCoin, dogecoin, ethereum, litecoin, xrp, number)[index]
                string = self.nameCurrency[index] + " " + str(buy_signals) + " " + str(sell_signals)
                self.list.append(string)
                self.purchaseCurrency(index, buy_signals, sell_signals, day)
                self.sellCurrency(index, buy_signals, sell_signals, day)
                index += 1
            day += 1
            number += 1
        self.calculateTotal()
        self.calculateNetTotal()


    def printPortfolioStrategy(self):
        i = 0
        while i < len(self.list):
            print(self.list[i])
            i += 1

    def totalValue(self):
        return self.total

    def totalNetValue(self):
        return self.totalNet

    def calculateNetTotal(self):
        self.totalNet = self.total - self.tax

    def calculateTotal(self):
        index = 0
        while index < len(self.coin):
            self.total += self.coin[index] * self.price_per_coin[index]
            index += 1

        for i in self.funds:
            self.total += i
