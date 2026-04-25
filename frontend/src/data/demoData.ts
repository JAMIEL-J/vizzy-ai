/**
 * Golden Path Demo Data for Vizzy Prototype.
 * High-fidelity data to ensure no NaN values and a rich visual experience.
 */

export interface DemoChart {
  id: string;
  title: string;
  type: 'bar' | 'line' | 'pie' | 'donut' | 'area';
  section: string;
  metric: string;
  dimension: string;
  data: any[];
  insight: string;
}

export interface DemoKPI {
  id: string;
  label: string;
  value: string;
  change: string;
  trend: 'up' | 'down';
  section: string;
}

export interface DemoDataset {
  id: string;
  name: string;
  domain: 'sales' | 'marketing' | 'churn' | 'finance';
  description: string;
  kpis: DemoKPI[];
  charts: DemoChart[];
}

export const DEMO_DATA: Record<string, DemoDataset> = {
  'sales-demo': {
    id: 'sales-demo',
    name: 'Global Electronics Sales 2024',
    domain: 'sales',
    description: 'Enterprise sales data across 4 regions with deep category breakdowns.',
    kpis: [
      { id: 'k1', label: 'Total Revenue', value: '$4,250,000', change: '+12.5%', trend: 'up', section: 'Executive Summary' },
      { id: 'k2', label: 'Avg Order Value', value: '$320', change: '-2.1%', trend: 'down', section: 'Executive Summary' },
      { id: 'k3', label: 'Conversion Rate', value: '3.4%', change: '+0.8%', trend: 'up', section: 'Growth' },
      { id: 'k4', label: 'Net Profit', value: '$840,000', change: '+5.2%', trend: 'up', section: 'Financials' },
    ],
    charts: [
      {
        id: 'c1',
        title: 'Monthly Revenue Trend',
        type: 'line',
        section: 'Revenue Analysis',
        metric: 'Revenue',
        dimension: 'Month',
        data: [
          { Month: 'Jan', Revenue: 200000 }, { Month: 'Feb', Revenue: 220000 },
          { Month: 'Mar', Revenue: 210000 }, { Month: 'Apr', Revenue: 250000 },
          { Month: 'May', Revenue: 280000 }, { Month: 'Jun', Revenue: 310000 },
          { Month: 'Jul', Revenue: 340000 }, { Month: 'Aug', Revenue: 320000 },
        ],
        insight: 'Revenue shows a strong upward trend starting in April, correlating with the Q2 Spring campaign.'
      },
      {
        id: 'c2',
        title: 'Revenue by Product Category',
        type: 'pie',
        section: 'Product Performance',
        metric: 'Revenue',
        dimension: 'Category',
        data: [
          { Category: 'Laptops', Revenue: 1500000 }, { Category: 'Phones', Revenue: 1200000 },
          { Category: 'Accessories', Revenue: 800000 }, { Category: 'Tablets', Revenue: 700000 },
        ],
        insight: 'Laptops remain the primary revenue driver, contributing 35% of total sales.'
      },
      {
        id: 'c3',
        title: 'Regional Sales Distribution',
        type: 'bar',
        section: 'Geographic Insights',
        metric: 'Sales',
        dimension: 'Region',
        data: [
          { Region: 'North America', Sales: 1200000 }, { Region: 'Europe', Sales: 900000 },
          { Region: 'Asia', Sales: 1100000 }, { Region: 'LATAM', Sales: 400000 },
        ],
        insight: 'North America and Asia are nearly tied for lead, while LATAM represents the fastest growing region.'
      },
      {
        id: 'c4',
        title: 'Category Growth Rate',
        type: 'bar',
        section: 'Growth',
        metric: 'Growth%',
        dimension: 'Category',
        data: [
          { Category: 'Laptops', Growth: 12 }, { Category: 'Phones', Growth: 8 },
          { Category: 'Accessories', Growth: 25 }, { Category: 'Tablets', Growth: -5 },
        ],
        insight: 'Accessories are seeing explosive growth (25%), while tablet sales are slightly declining.'
      },
      {
        id: 'c5',
        title: 'Sales vs Target',
        type: 'line',
        section: 'Executive Summary',
        metric: 'Value',
        dimension: 'Month',
        data: [
          { Month: 'Jan', Actual: 200000, Target: 180000 }, { Month: 'Feb', Actual: 220000, Target: 210000 },
          { Month: 'Mar', Actual: 210000, Target: 220000 }, { Month: 'Apr', Actual: 250000, Target: 230000 },
        ],
        insight: 'The team has outperformed targets in 3 out of 4 months of the first quarter.'
      }
    ]
  },
  'churn-demo': {
    id: 'churn-demo',
    name: 'SaaS Customer Churn Analysis',
    domain: 'churn',
    description: 'Deep dive into user retention and churn drivers for a B2B SaaS platform.',
    kpis: [
      { id: 'ck1', label: 'Monthly Churn Rate', value: '2.4%', change: '-0.5%', trend: 'up', section: 'Retention' },
      { id: 'ck2', label: 'Net Revenue Retention', value: '104%', change: '+2.0%', trend: 'up', section: 'Financials' },
      { id: 'ck3', label: 'Customer LTV', value: '$1,200', change: '+15%', trend: 'up', section: 'Financials' },
      { id: 'ck4', label: 'Active Users', value: '12.5k', change: '+4.1%', trend: 'up', section: 'Growth' },
    ],
    charts: [
      {
        id: 'cc1',
        title: 'Churn Rate by Subscription Plan',
        type: 'bar',
        section: 'Plan Analysis',
        metric: 'Churn Rate',
        dimension: 'Plan',
        data: [
          { Plan: 'Basic', Churn: 0.05 }, { Plan: 'Pro', Churn: 0.02 }, { Plan: 'Enterprise', Churn: 0.01 },
        ],
        insight: 'Basic plan users churn at 5x the rate of Enterprise users, suggesting onboarding gaps.'
      },
      {
        id: 'cc2',
        title: 'Churn vs Support Tickets',
        type: 'line',
        section: 'Driver Analysis',
        metric: 'Churn',
        dimension: 'Tickets',
        data: [
          { Tickets: '0-2', Churn: 0.01 }, { Tickets: '3-5', Churn: 0.04 }, { Tickets: '6+', Churn: 0.12 },
        ],
        insight: 'A critical threshold exists at 5 tickets; churn increases exponentially beyond this point.'
      },
      {
        id: 'cc3',
        title: 'User Activity Distribution',
        type: 'pie',
        section: 'Engagement',
        metric: 'Users',
        dimension: 'Activity Level',
        data: [
          { Level: 'Power User', Users: 2000 }, { Level: 'Active', Users: 5000 },
          { Level: 'Occasional', Users: 3000 }, { Level: 'Inactive', Users: 2500 },
        ],
        insight: 'Only 16% of users are "Power Users", indicating a potential for better feature discovery.'
      }
    ]
  }
};
