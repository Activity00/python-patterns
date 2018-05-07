# coding: utf-8

"""
@author: Activity00
@time: 2018/4/19 15:13
"""
from patterns.behavioral.mediator import IColleague, IMediator

"""
example source: https://blog.csdn.net/ChenVast/article/details/79193049

中介者模式

手机仓储管理系统，使用者有三方：销售、仓库管理员、采购。
需求是：销售一旦达成订单，销售人员会通过系统的销售子系统部分通知仓储子系统，
仓储子系统会将可出仓手机数量减少，同时通知采购管理子系统当前销售订单；
仓储子系统的库存到达阈值以下，会通知销售子系统和采购子系统，并督促采购子系统采购；
采购完成后，采购人员会把采购信息填入采购子系统，采购子系统会通知销售子系统采购完成，并通知仓库子系统增加库存。
引入一个新的角色-中介者-来将“网状结构”精简为“星形结构”。
"""


class PurchaseColleague(IColleague):
    """采购子系统"""
    def buy_stuff(self, num):
        print("采购: 买 %s" % num)
        self.mediator.execute("buy", num)

    def get_notice(self, content):
        print("采购: 接到通知--%s" % content)


class WarehouseColleague(IColleague):
    """仓库子系统"""
    total = 0
    threshold = 100

    def set_threshold(self, threshold):
        self.threshold = threshold

    def is_enough(self):
        if self.total < self.threshold:
            print(" 仓库:警告……库存较低... ")
            self.mediator.execute("警告", self.total)
            return False
        else:
            return True

    def inc(self, num):
        self.total += num
        print("仓库:增加 %s" % num)
        self.mediator.execute("增加", num)
        self.is_enough()

    def dec(self, num):
        if num > self.total:
            print("仓库:错误……库存是不够的")
        else:
            self.total -= num
            print("仓库:减少 %s" % num)
            self.mediator.execute("减少", num)
        self.is_enough()


class SalesColleague(IColleague):
    """销售子系统"""
    def sell_stuff(self, num):
        print("销售:销售 %s" % num)
        self.mediator.execute("sell", num)

    def get_notice(self, content):
        print("销售:获取通知--%s" % content)


class StockMediator(IMediator):
    """中间者"""
    def register_purchase(self, purchase):
        self.purchase = purchase

    def register_warehose(self, warehose):
        self.warehouse = warehose

    def register_sales(self, sales):
        self.sales = sales

    def execute(self, content, num):
        print("中介者:获取信息--%s" % content)
        if content == "buy":
            self.warehouse.inc(num)
            self.sales.get_notice("买 %s" % num)
        elif content == "increase":
            self.sales.get_notice("Inc %s" % num)
            self.purchase.getNotice("Inc %s" % num)
        elif content == "decrease":
            self.sales.get_notice("Dec %s" % num)
            self.purchase.get_notice("Dec %s" % num)
        elif content == "warning":
            self.sales.get_notice("库存较低.%s 左边." % num)
            self.purchase.get_notice("库存很低。请购买更多!!! %s 左边" % num)
        elif content == "sell":
            self.warehouse.dec(num)
            self.purchase.get_notice("售出 %s" % num)
        else:
            pass


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # 1. 中间者
    mediator = StockMediator()
    # 2. 子系统 - 包含一个中间者引用
    purchase = PurchaseColleague(mediator)
    warehouse = WarehouseColleague(mediator)
    sales = SalesColleague(mediator)

    mediator.register_purchase(purchase)
    mediator.register_warehose(warehouse)
    mediator.register_sales(sales)
    # 3. 子系统执行
    warehouse.set_threshold(200)
    purchase.buy_stuff(300)
    sales.sell_stuff(120)
