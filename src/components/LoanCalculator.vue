<script>
export default {
  data() {
    return {
      repaymentModeEnum: {
        EPP: "0", //等额本金
        EPIP: "1", // 等额本息
        PREP: "2", // 提前还款
      },
      repaymentMode: "0", // 还款方式：0: 等额本金, 1: 等额本息, 2: 提前还款
      amount: null, // 贷款总额
      periods: null, // 贷款期数
      annualRate: 4.85, // 年利率
      monthlyRate: 0.0, // 月利率
      totalInterest: null, // 总利息
      A: null, // 等额本息每月固定还款额
    };
  },
  methods: {
    init() {
      this.repaymentMode = this.repaymentModeEnum.EPP;
      this.amount = null;
      this.periods = null;
      this.annualRate = 4.85;
      this.monthlyRate = 0;
      this.totalInterest = null;
      this.A = null;
    },

    equal_principal_payments() {
      // 等额本金
      const tempA = this.amount / this.periods; // 每月固定还本金额度
      let remain = this.amount;
      let tempInterest = 0;
      let curInterest = 0;
      for (let i = 0; i < this.periods; i++) {
        curInterest = this.monthlyRate * remain;
        tempInterest += curInterest;
        remain -= tempA;
      }
      return tempInterest;
    },

    equal_principal_and_interest_payment_computer() {
      /**
       * 等额本息每月固定还款额
       * 计算等额本息还款方式每月固定还款额，单位：万元
       * 假设贷款金额为12万元, 12期还清，设a为剩余还款数，A为每月固定还款额，则：
       * a0 = 12
       * a1 = a0 * (1 + rate) - A
       * a2 = a1 * (1 + rate) - A
       * a3 = a2 * (1 + rate) - A
       * ...
       * a12 = a11 * (1 + rate) - A = 0
       * 根据上述表达式我们得到一个仅有A的一元一次方程：
       * ax + b = c
       * (1 + _rate) * amount - A
       * (1 + _rate) * ((1 + _rate) * amount - A) - A
       * (1 + _rate) * ((1 + _rate) * ((1 + _rate) * amount - A) - A) - A
       */
      let coef = 1;
      let cons = (1 + this.monthlyRate) * this.amount;
      for (let i = 0; i < this.periods - 1; i++) {
        coef = (1 + this.monthlyRate) * coef + 1;
        cons = (1 + this.monthlyRate) * cons;
      }
      return cons / coef;
    },

    equal_principal_and_interest_payment() {
      // 等额本息
      this.A = this.equal_principal_and_interest_payment_computer();
      let remain = this.amount;
      let total_interest = 0;
      for (let i = 0; i < this.periods; i++) {
        total_interest += this.monthlyRate * remain;
        remain = (1 + this.monthlyRate) * remain - this.A;
      }
      return total_interest;
    },

    month_delta() {
      // TODO 计算时间间隔月数
    },

    prepayment(first_payment_date, prepayment_date, prepayment_amount) {
      // TODO 提前还款
    },

    checklegal() {
      if (
        this.amount === null ||
        this.amount <= 0 ||
        this.annualRate === null ||
        this.annualRate <= 0 ||
        this.periods === null ||
        this.periods <= 0
      ) {
        alert("内容填写错误");
        return false;
      } else {
        return true;
      }
    },

    doCalculate() {
      if (!this.checklegal()) return;
      this.setMonthlyRate();
      switch (this.repaymentMode) {
        case this.repaymentModeEnum.EPP:
          console.log("等额本金");
          this.totalInterest = this.equal_principal_payments();
          break;
        case this.repaymentModeEnum.EPIP:
          console.log("等额本息");
          this.totalInterest = this.equal_principal_and_interest_payment();
          break;
        case this.repaymentModeEnum.PREP:
          console.log("提前还款");
          this.totalInterest = this.prepayment();
          break;
        default:
          console.log(`还款方式：${this.repaymentMode} 错误`);
      }
    },

    setMonthlyRate() {
      this.monthlyRate = this.annualRate / 12 / 100;
    },
  },
  mounted() {
    this.setMonthlyRate();
  },
};
</script>
<template>
  <div class="card text-center" style="max-width: 40%">
    <div class="card-header">购房贷款计算器</div>
    <div class="card-header">
      <ul class="nav nav-tabs card-header-tabs">
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{
              active:
                repaymentMode === repaymentModeEnum.EPP ||
                repaymentMode === repaymentModeEnum.EPIP,
            }"
            @click="repaymentMode = repaymentModeEnum.EPP"
            href="#"
            >商业贷款</a
          >
        </li>
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: repaymentMode === repaymentModeEnum.PREP }"
            @click="repaymentMode = repaymentModeEnum.PREP"
            href="#"
            >提前还款</a
          >
        </li>
        <li class="nav-item">
          <a class="nav-link">其他</a>
        </li>
      </ul>
    </div>
    <div class="card-body">
      <div
        class="input-group mb-3"
        v-if="
          repaymentMode === repaymentModeEnum.EPP ||
          repaymentMode === repaymentModeEnum.EPIP
        "
      >
        <select
          class="form-select"
          aria-label="还款方式"
          v-model="repaymentMode"
        >
          <option :value="repaymentModeEnum.EPP" selected>等额本金</option>
          <option :value="repaymentModeEnum.EPIP">等额本息</option>
        </select>
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">贷款总额</span>
        <input type="number" class="form-control" v-model="amount" />
        <span class="input-group-text">万元</span>
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">贷款期数</span>
        <input type="number" class="form-control" v-model="periods" />
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">年利率</span>
        <input type="number" class="form-control" v-model="annualRate" />
        <span class="input-group-text">%</span>
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">总利息</span>
        <input
          type="text"
          class="form-control"
          readonly
          disabled
          v-model="totalInterest"
        />
        <span class="input-group-text">万元</span>
      </div>
      <div
        class="input-group mb-3"
        v-if="repaymentMode === repaymentModeEnum.EPIP"
      >
        <span class="input-group-text">每月固定还款额</span>
        <input type="text" class="form-control" disabled readonly v-model="A" />
        <span class="input-group-text">万元</span>
      </div>
      <div class="col-auto">
        <button @click="init()" type="button" class="btn btn-primary mb-3">
          重置
        </button>
        <button
          @click="doCalculate()"
          type="button"
          class="btn btn-primary mb-3"
        >
          计算
        </button>
      </div>
    </div>
  </div>
</template>
