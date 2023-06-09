# -*- coding: utf-8 -*-

"""计算个人住房商业贷款"""

from sympy import *
from datetime import datetime


# TODO 实现初次还款不足整月计算

class LoanCalculator(object):
    def __init__(self, amount, periods, rate):
        """
        :param amount: 还款总额
        :param period: 还款期数
        :param rate: 还款年利率
        """
        self.amount = amount
        self.periods = periods
        self.rate = rate
        self._rate = rate / 12 / 100

    def equal_principal_payments(self):
        """
        等额本金，单位：万元
        :return: 总利息
        """
        A = self.amount / self.periods  # 每月固定还本金额度
        remain, total_interest = self.amount, 0
        for _ in range(self.periods):
            cur_interest = self._rate * remain
            total_interest += cur_interest
            remain -= A
        return total_interest

    # equal_principal_and_interest_payment

    def equal_principal_payments_printer(self):
        total_interest = self.equal_principal_payments()
        print(f"等额本金法总利息：{total_interest} 元")

    def equal_principal_and_interest_payment_computer_using_sympy(self):
        """
        计算等额本息还款方式每月固定还款额，单位：万元
        :return: 每月固定还款额
        """
        A, exp = symbols('A'), self.amount
        for _ in range(self.periods):
            exp = (1 + self._rate) * exp - A
        return solveset(Eq(exp, 0))._args[0]

    def equal_principal_and_interest_payment_computer(self):
        """
        计算等额本息还款方式每月固定还款额，单位：万元
        假设贷款金额为12万元, 12期还清，设a为剩余还款数，A为每月固定还款额，则：
        a0 = 12
        a1 = a0 * (1 + rate) - A
        a2 = a1 * (1 + rate) - A
        a3 = a2 * (1 + rate) - A
        ...
        a12 = a11 * (1 + rate) - A = 0
        根据上述表达式我们得到一个仅有A的一元一次方程：
        ax + b = c
        (1 + _rate) * amount - A
        (1 + _rate) * ((1 + _rate) * amount - A) - A
        (1 + _rate) * ((1 + _rate) * ((1 + _rate) * amount - A) - A) - A
        ...
        :return: 每月固定还款额
        """
        coef, cons = 1, (1 + self._rate) * self.amount
        for _ in range(self.periods - 1):
            coef, cons = (1 + self._rate) * coef + 1, (1 + self._rate) * cons
        return cons / coef

    def equal_principal_and_interest_payment(self) -> float:
        """
        等额本息，单位：万元
        :return: 总利息
        """
        A = self.equal_principal_and_interest_payment_computer()

        # 计算每月还本金和利息
        remain, total_interest = self.amount, 0
        for _ in range(self.periods):
            total_interest += self._rate * remain
            remain = (1 + self._rate) * remain - A
        return total_interest

    def equal_principal_and_interest_payment_printer(self) -> None:
        A = self.equal_principal_and_interest_payment_computer()
        print(f"等额本息法还款 {self.amount} 万元，{self.periods} 期还清，利率 {self.rate}%")
        print(f"每月固定还款: {A} 万元")

        # 计算每月还本金和利息
        remain, total_interest = self.amount, 0
        for i in range(self.periods):
            total_interest += self._rate * remain
            print(
                f"第 {i + 1} 个月还 {A * 10000} 元，其中包含本金：{(A - self._rate * remain) * 10000} 元，利息：{(self._rate * remain) * 10000} 元")
            remain = (1 + self._rate) * remain - A
        print(f"等额本息法总利息：{total_interest * 10000} 元")

    @staticmethod
    def month_delta(start: datetime, end: datetime) -> int:
        """
        计算日期间相差月份
        :param start: 开始时间
        :param end: 结束时间
        :return: 间隔月数
        """
        year_diff = end.year - start.year
        end_month = year_diff * 12 + end.month
        delta = end_month - start.month
        return delta

    def prepayment(self, first_payment_date: str, prepayment_date: str, prepayment_amount: int) -> (int, float):
        """
        提前还款，提前还款方式（一次全部还清、部分还清，默认每月还款额不变缩短年限）（在实际的提前还款操作中，因为利息是按天计算的，所以进行提前还款时需要将已产生的利息还清，此部分内容暂时忽略）
        :param first_payment_date: 首次还款年月
        :param prepayment_date: 提前还款年月
        :param prepayment_amount: 提前还款金额
        :return: 提前还款之后还款时间，提前还款利息总额
        """
        # 计算每月固定还款额度A
        A = self.equal_principal_and_interest_payment_computer()

        # 计算已还款期数 20xx年xx月
        first_payment_datetime = datetime.strptime(first_payment_date, "%Y年%m月")
        prepayment_datetime = datetime.strptime(prepayment_date, "%Y年%m月")
        months = self.month_delta(first_payment_datetime, prepayment_datetime)

        # 计算截止到提前还款时已还款期数，与已还款总额，剩余还款额
        remain, total_interest = self.amount, 0
        for _ in range(months):
            total_interest += self._rate * remain
            remain = (1 + self._rate) * remain - A
        # 进行提前还款
        remain -= prepayment_amount
        remain_periods = 0
        while remain > 0:
            total_interest += self._rate * remain
            remain = (1 + self._rate) * remain - A
            remain_periods += 1
        return months + remain_periods, total_interest

    def prepayment_printer(self, first_payment_date: str, prepayment_date: str, prepayment_amount: int):
        total_periods, prepayment_total_interest = self.prepayment(first_payment_date, prepayment_date,
                                                                   prepayment_amount)
        total_interest = self.equal_principal_and_interest_payment()
        print(
            f"如进行提前还款，总还款期数：{total_periods}，减少 {self.periods - total_periods} 期，总利息：{prepayment_total_interest}，减少 {total_interest - prepayment_total_interest} 万元")


if __name__ == "__main__":
    loan_calculator = LoanCalculator(124, 300, 4.85)
    # loan_calculator.equal_principal_payments_printer()
    # print(loan_calculator.equal_principal_and_interest_payment_computer())
    # loan_calculator.equal_principal_and_interest_payment_printer()
    print(loan_calculator.prepayment("2022年10月", "2023年05月", 20))
    # loan_calculator.prepayment_printer("2022年10月", "2023年05月", 20)
