import re

def migrate_admin_analytics():
    path = r"d:\Vizzy Redesign\Vizzy Redesign\frontend\src\pages\admin\AdminAnalytics.tsx"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Imports
    content = re.sub(r"import\s+\{\s*LineChart,[^\}]*\}\s*from\s*'recharts';", """import {
    Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip as ChartTooltip, Legend as ChartLegend, Filler
} from 'chart.js';
import { Bar, Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, ChartTooltip, ChartLegend, Filler
);""", content)

    # Charts
    content = re.sub(r'<ResponsiveContainer.*?<AreaChart data=\{dailyActiveUsers\}>.*?</AreaChart>\s*</ResponsiveContainer>', """<div style={{ height: 250, width: '100%' }}>
                        <Line
                            data={{
                                labels: dailyActiveUsers.map(d => d.date),
                                datasets: [{
                                    label: 'Users',
                                    data: dailyActiveUsers.map(d => d.users),
                                    fill: true,
                                    backgroundColor: 'rgba(124, 58, 237, 0.2)',
                                    borderColor: '#7c3aed',
                                    tension: 0.4
                                }]
                            }}
                            options={{ maintainAspectRatio: false }}
                        />
                    </div>""", content, flags=re.DOTALL)

    content = re.sub(r'<ResponsiveContainer.*?<BarChart data=\{queryTypes\}>.*?</BarChart>\s*</ResponsiveContainer>', """<div style={{ height: 250, width: '100%' }}>
                        <Bar
                            data={{
                                labels: queryTypes.map(d => d.type),
                                datasets: [{
                                    label: 'Count',
                                    data: queryTypes.map(d => d.count),
                                    backgroundColor: queryTypes.map(d => d.color),
                                    borderRadius: 4
                                }]
                            }}
                            options={{ maintainAspectRatio: false }}
                        />
                    </div>""", content, flags=re.DOTALL)

    content = re.sub(r'<ResponsiveContainer.*?<LineChart data=\{storageUsage\}>.*?</LineChart>\s*</ResponsiveContainer>', """<div style={{ height: 250, width: '100%' }}>
                    <Line
                        data={{
                            labels: storageUsage.map(d => d.month),
                            datasets: [{
                                label: 'Storage (GB)',
                                data: storageUsage.map(d => d.storage),
                                borderColor: '#ff6b35',
                                backgroundColor: '#fff',
                                pointBackgroundColor: '#fff',
                                pointBorderColor: '#ff6b35',
                                pointRadius: 4,
                                pointHoverRadius: 6
                            }]
                        }}
                        options={{ maintainAspectRatio: false }}
                    />
                </div>""", content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def migrate_admin_dashboard():
    path = r"d:\Vizzy Redesign\Vizzy Redesign\frontend\src\pages\admin\AdminDashboard.tsx"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Imports
    content = re.sub(r"import\s+\{\s*AreaChart,[^\}]*\}\s*from\s*'recharts';", """import {
    Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip as ChartTooltip, Legend as ChartLegend, Filler
} from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, ChartTooltip, ChartLegend, Filler
);""", content)

    # Charts
    content = re.sub(r'<ResponsiveContainer.*?<AreaChart data=\{userGrowthData\}>.*?</AreaChart>\s*</ResponsiveContainer>', """<div style={{ height: 250, width: '100%' }}>
                        <Line
                            data={{
                                labels: userGrowthData.map(d => d.month),
                                datasets: [{
                                    label: 'New Users',
                                    data: userGrowthData.map(d => d.newUsers),
                                    fill: true,
                                    backgroundColor: 'rgba(124, 58, 237, 0.2)',
                                    borderColor: '#7c3aed',
                                    tension: 0.4
                                },
                                {
                                    label: 'Active Users',
                                    data: userGrowthData.map(d => d.activeUsers),
                                    fill: true,
                                    backgroundColor: 'rgba(34, 197, 94, 0.2)',
                                    borderColor: '#22c55e',
                                    tension: 0.4
                                }]
                            }}
                            options={{ maintainAspectRatio: false }}
                        />
                    </div>""", content, flags=re.DOTALL)

    content = re.sub(r'<ResponsiveContainer.*?<PieChart>.*?</PieChart>\s*</ResponsiveContainer>', """<div style={{ height: 250, width: '100%' }}>
                        <Pie
                            data={{
                                labels: activityData.map(d => d.name),
                                datasets: [{
                                    data: activityData.map(d => d.value),
                                    backgroundColor: activityData.map(d => d.color),
                                }]
                            }}
                            options={{ maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }}
                        />
                    </div>""", content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

migrate_admin_analytics()
migrate_admin_dashboard()
