/**
 * Golden Path Demo Data for Vizzy Prototype.
 * This allows the application to function without a live backend
 * or to demonstrate high-quality results to recruiters instantly.
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
    description: 'Comprehensive sales dataset across 4 regions with product category breakdowns.',
    kpis: [
      { id: 'k1', label: 'Total Revenue', value: '$4.2M', change: '+12.5%', trend: 'up', section: 'Executive Summary' },
      { id: 'k2', label: 'Avg Order Value', value: '$320', change: '-2.1%', trend: 'down', section: 'Executive Summary' },
      { id: 'k3', label: 'Conversion Rate', value: '3.4%', change: '+0.8%', trend: 'up', section: 'Growth' },
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
        ],
        insight: 'Revenue shows a strong upward trend starting in April, likely due to the Spring campaign.'
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
        insight: 'Laptops remain the primary revenue driver, contributing over 35% of total sales.'
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
        insight: 'North America and Asia are nearly tied for lead, while LATAM represents a significant growth opportunity.'
      }
    ]
  },
  'churn-demo': {
    id: 'churn-demo',
    name: 'SaaS Customer Churn Analysis',
    domain: 'churn',
    description: 'Analysis of user retention and churn drivers for a B2B SaaS platform.',
    kpis: [
      { id: 'ck1', label: 'Monthly Churn Rate', value: '2.4%', change: '-0.5%', trend: 'up', section: 'Retention' },
      { id: 'ck2', label: 'Net Revenue Retention', value: '104%', change: '+2.0%', trend: 'up', section: 'Financials' },
      { id: 'ck3', label: 'Customer LTV', value: '$1,200', change: '+15%', trend: 'up', section: 'Financials' },
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
        insight: 'Basic plan users churn at 5x the rate of Enterprise users, suggesting a need for better onboarding for entry-level tiers.'
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
        insight: 'There is a sharp correlation between support ticket volume and churn once users cross the 5-ticket threshold.'
      }
    ]
  }
};
