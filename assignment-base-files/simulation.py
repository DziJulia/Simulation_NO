import random  # need a random number generator


class Simulation:
    def __init__(self, weights):
        # money for investing 2000 for each cuurency
        self.funds = [2000, 2000, 2000, 2000, 2000]

        # tax
        self.tax = 0
        # day difference
        self.days = [1, 2, 4, 8, 16, 32, 64, 128]
        # Name of currency
        self.coin = ['BitCoin', 'DogeCoin', 'Ethereum', 'LiteCoin', 'XRP']
        self.price_per_coin = 0
        # initialize buy weight for current day
        self._buy_weights = [0, 0, 0, 0, 0]
        # initialize sell weight for current day
        self._sell_weights = [0, 0, 0, 0, 0]
        # initialize array for adding currency i bought
        self.coin_bought = []
        # calculate remaining value in my value list
        self.remaining = 0
        self.value_bought = [0, 0, 0, 0, 0]
        self.buySignal = [0, 0, 0, 0, 0]
        self.sellSignal = [0, 0, 0, 0, 0]

        self.bitcoin_buy_weight = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.dodgecoin_buy_weight = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.ethereum_buy_weight = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.litecoin_buy_weight = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.xrp_buy_weight = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

        self.bitcoin_sell_weight = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        self.dodgecoin_sell_weight = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        self.ethereum_sell_weight = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        self.litecoin_sell_weight = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        self.xrp_sell_weight = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]

    def buyorSell(self, list, index, day, minusdate):
        # cant divide by 0
        x = day - minusdate
        if list[index][day - minusdate] == 0:
            return 0
        else:
            # (currency closing today−currency closing previous)/currency closing previous
            # self.buyorSell(close_list, index, startDay, i)
            return (list[index][day] - list[index][x]) / list[index][x]

    # method for calculate maximum coins what im able to buy
    def getMaxcoing(self, available, coins):
        mod = (available / coins)
        self.remaining = int(mod) * coins
        # casting it in int due we want full coin
        return int(mod)

    # method for calculate sell of the coins
    # in the end it get multiplied with value i have
    # this is to figure out value of coin
    def sellCoin(self, index, close_value):
        return close_value - self._buy_weights[index]

    def buySignal(self, close_list, startDay):
        buySignal = [0, 0, 0, 0, 0]
        print("here")
        for i in self.days:
            if self.buyorSell(close_list, 0, startDay, i) > self.bitcoin_buy_weight[i]:
                self.buySignal[0] += 1
            if self.buyorSell(close_list, 1, startDay, i) > self.dodgecoin_buy_weight[i]:
                self.buySignal[1] += 1
            if self.buyorSell(close_list, 2, startDay, i) > self.ethereum_buy_weight[i]:
                self.buySignal[2] += 1
            if self.buyorSell(close_list, 3, startDay, i) > self.litecoin_buy_weight[i]:
                self.buySignal[3] += 1
            if self.buyorSell(close_list, 4, startDay, i) > self.xpr_buy_weight[i]:
                self.buySignal[4] += 1
        return buySignal

    def sellSignal(self, close_list, startDay):
        sellSignal = [0, 0, 0, 0, 0]

        for i in self.days:
            if self.buyorSell(close_list, 0, startDay, i) > self.bitcoin_sell_weight[i]:
                self.sellSignal[0] += 1
            if self.buyorSell(close_list, 1, startDay, i) > self.dodgecoin_sell_weight[i]:
                self.sellSignal[1] += 1
            if self.buyorSell(close_list, 2, startDay, i) > self.ethereum_sell_weight[i]:
                self.sellSignal[2] += 1
            if self.buyorSell(close_list, 3, startDay, i) > self.litecoin_sell_weight[i]:
                self.sellSignal[3] += 1
            if self.buyorSell(close_list, 4, startDay, i) > self.xpr_sell_weight[i]:
                self.sellSignal[4] += 1
        return sellSignal

    # method for main calculation
    def calculation(self, close_list, startDay, index):
        print('==== day ', startDay, ' ====')
        print(self.buySignal(close_list, startDay))
        while index < len(close_list):
            buy = 0
            sell = 0
            print(self.coin[index], buy, sell)
            # principal of buying
            # - the currency has a closing value of 0.01 or more
            # - there are more buy signals than sell signals (same number of signals
            # we will not purchase)
            # - we haven’t purchased this currency already
            # print(self.weights)
            if buy > sell:
                if close_list[index][startDay] > 0.01:
                    if self.coin[index] not in self.coin_bought:
                        value = self.getMaxcoing(self.funds[index], close_list[index][startDay])
                        print("->Purchased", value, self.coin[index], " for", close_list[index][startDay], "per coin")
                        self.coin_bought.append(self.coin[index])
                        self.value_bought[index] = value
                        self.funds[index] = self.funds[index] - self.remaining
                        self._buy_weights[index] = close_list[index][startDay]
            # principal of sell
            # - – We have coins to sell
            # - – There are more sell signals than buy signals (or equal)
            elif sell >= buy:
                if self.coin[index] in self.coin_bought:
                    print("->Sold", self.value_bought[index], self.coin[index], " for", close_list[index][startDay],
                          "per coin")
                    self.coin_bought.remove(self.coin[index])
                    self._sell_weights[index] = close_list[index][startDay]
                    profit = self.sellCoin(index, close_list[index][startDay])
                    self.total = profit * self.value_bought[index]
                    self.funds[index] += self.value_bought[index] * close_list[index][startDay]
                    self.value_bought[index] = 0
                    if profit > 0:
                        calculate = (self.total / 100) * 33
                        self.tax += calculate
                    print("Profit per coin -> ", profit, " profit total -> ", self.total)
                    # print(self.funds)
            index += 1

    # method for counting all available fund in my array after all transaktions
    def totalValue(self):
        self.final = 0
        index = 0
        while index < len(self.value_bought):
            self.final += self.value_bought[index] * self._buy_weights[index]
            index += 1

        for i in self.funds:
            self.final += i
        return self.final

    # method for my simulation

    def simulation(self, close_list, startDay):
        index = 0
        self.calculation(close_list, startDay, index)

    def totalNetValue(self):
        return self.totalValue() - self.tax

    def rouletteWheel(self, a, b):
        number = random.random()
        if (number > 0.5):
            return a
        else:
            return b
