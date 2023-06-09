import unittest

from main import LoanCalculator


class TestDict(unittest.TestCase):
    def setUp(self):
        self.loan_calculator = LoanCalculator(124, 300, 4.85)

    def test_equal_principal_payments(self):
        """等额本金"""

        self.assertEqual(round(self.loan_calculator.equal_principal_payments(), 2), 75.43)

    def test_equal_principal_and_interest_payment_computer(self):
        """等额本息每月固定支付额"""
        self.assertEqual(round(self.loan_calculator.equal_principal_and_interest_payment_computer(), 2), 0.71)

    def test_equal_principal_and_interest_payment(self):
        """等额本息"""
        self.assertEqual(round(self.loan_calculator.equal_principal_and_interest_payment(), 2), 90.23)

    def test_prepayment(self):
        total_periods, total_interest = self.loan_calculator.prepayment("2022年10月", "2023年05月", 20)
        self.assertEqual((total_periods, round(total_interest, 2)), (223, 54.62))


if __name__ == "__main__":
    unittest.main()
