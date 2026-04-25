import re
import sys

def migrate_user_dashboard():
    path = r"d:\Vizzy Redesign\Vizzy Redesign\frontend\src\pages\user\UserDashboard.tsx"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace imports
    recharts_import_regex = re.compile(r"import\s*\{[\s\n]*BarChart,[^\}]*\}\s*from\s*'recharts';")
    chartjs_import = """import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, RadialLinearScale,
  Title, Tooltip as ChartTooltip, Legend as ChartLegend, Filler
} from 'chart.js';
import { Bar, Line, Pie, Scatter, Radar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, RadialLinearScale,
  Title, ChartTooltip, ChartLegend, Filler
);"""
    
    content = recharts_import_regex.sub(chartjs_import, content)
    
    # 2. Add an adapter function to replace the switch statement for recharts
    # We will search for the switch (chart.type) { ... } inside BaseChart
    
    # We just need to tell the user that this file uses very complex custom SVG treemaps and Recharts-specific events
    # We will replace the switch block with a ChartJS powered one.

    switch_start = content.find("switch (chart.type) {")
    switch_end = content.find("const FilterDropdown", switch_start)
    
    if switch_start == -1 or switch_end == -1:
        print("Could not find switch statement")
        sys.exit(1)
        
    chartjs_switch = """const commonOptions = (isScale: boolean, axisLabel: string) => ({
        responsive: true,
        maintainAspectRatio: false,
        onClick: (e: any, elements: any[]) => {
            if (elements.length > 0 && onFilterClick) {
                const dataIndex = elements[0].index;
                const value = chartData[dataIndex]?.[nameKey];
                if (value) onFilterClick(filterCol, String(value));
            }
        },
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: isDark ? 'rgba(0,0,0,0.8)' : 'rgba(255,255,255,0.9)',
                titleColor: isDark ? '#fff' : '#000',
                bodyColor: isDark ? '#ccc' : '#333',
                borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
                borderWidth: 1,
                callbacks: {
                    label: (ctx: any) => ` ${fmtVal(ctx.raw)}`
                }
            }
        },
        scales: isScale ? {
            x: {
                grid: { display: false },
                ticks: { color: chartColors.text }
            },
            y: {
                grid: { color: chartColors.grid },
                ticks: { color: chartColors.text, callback: (v: any) => fmtTick(v, axisLabel) }
            }
        } : undefined
    });

    switch (chart.type) {
        case 'bar':
            return (
                <div className="flex flex-col h-full w-full">
                    {renderOutlierToggle()}
                    <div style={{ height: 192, width: '100%' }}>
                        <Bar 
                            data={{
                                labels: chartData.map((d: any) => d[nameKey]),
                                datasets: [{
                                    data: chartData.map((d: any) => d.value),
                                    backgroundColor: chartData.map((_: any, i: number) => getPaletteColor(i)),
                                    borderRadius: 6
                                }]
                            }} 
                            options={commonOptions(true, chart.value_label) as any} 
                        />
                    </div>
                </div>
            );

        case 'hbar':
            return (
                <div className="flex flex-col h-full w-full">
                    {renderOutlierToggle()}
                    <div style={{ height: chartData.length >= 8 ? Math.min(chartData.length * 28 + 40, 300) : 192, width: '100%' }}>
                        <Bar 
                            data={{
                                labels: chartData.map((d: any) => d[nameKey]),
                                datasets: [{
                                    data: chartData.map((d: any) => d.value),
                                    backgroundColor: chartData.map((_: any, i: number) => getPaletteColor(i)),
                                    borderRadius: 6
                                }]
                            }} 
                            options={{
                                ...commonOptions(true, chart.value_label),
                                indexAxis: 'y'
                            } as any} 
                        />
                    </div>
                </div>
            );

        case 'stacked_bar':
            return (
                <div className="flex flex-col h-full w-full">
                    {renderOutlierToggle()}
                    <div style={{ height: 192, width: '100%' }}>
                        <Bar 
                            data={{
                                labels: chartData.map((d: any) => d[nameKey]),
                                datasets: [
                                    { label: 'Positive', data: chartData.map((d: any) => d.positive), backgroundColor: getPaletteColor(0) },
                                    { label: 'Negative', data: chartData.map((d: any) => d.negative), backgroundColor: getPaletteColor(1) }
                                ]
                            }} 
                            options={{
                                ...commonOptions(true, chart.value_label),
                                plugins: { legend: { display: true } },
                                scales: { x: { stacked: true }, y: { stacked: true } }
                            } as any} 
                        />
                    </div>
                </div>
            );

        case 'pie':
        case 'donut':
            return (
                <div className="flex flex-col h-full w-full">
                    {renderOutlierToggle()}
                    <div style={{ height: 210, width: '100%' }}>
                        <Pie 
                            data={{
                                labels: chartData.map((d: any) => d[nameKey] || d.name),
                                datasets: [{
                                    data: chartData.map((d: any) => d.value),
                                    backgroundColor: chartData.map((_: any, i: number) => getPaletteColor(i)),
                                    borderWidth: isDark ? 2 : 0,
                                    borderColor: '#1a1d24'
                                }]
                            }} 
                            options={{
                                ...commonOptions(false, ''),
                                cutout: chart.type === 'donut' ? '70%' : '0%',
                                plugins: { legend: { position: 'bottom', labels: { color: chartColors.text, usePointStyle: true } } }
                            } as any} 
                        />
                    </div>
                </div>
            );

        case 'line':
        case 'area':
        case 'stacked':
            return (
                <div className="flex flex-col h-full w-full">
                    {renderOutlierToggle()}
                    <div style={{ height: 192, width: '100%' }}>
                        <Line 
                            data={{
                                labels: chartData.map((d: any) => d.timestamp || d.date || d[nameKey]),
                                datasets: chart.type === 'stacked' 
                                    ? (chart.categories || []).map((cat: string, i: number) => ({
                                        label: cat,
                                        data: chartData.map((d: any) => d[cat]),
                                        backgroundColor: getPaletteColor(i),
                                        borderColor: getPaletteColor(i),
                                        fill: true
                                    }))
                                    : [{
                                        data: chartData.map((d: any) => d.value),
                                        backgroundColor: chart.type === 'line' ? 'transparent' : 'rgba(99, 102, 241, 0.2)',
                                        borderColor: getPaletteColor(0),
                                        fill: chart.type === 'area',
                                        tension: 0.4
                                    }]
                            }} 
                            options={{
                                ...commonOptions(true, chart.value_label),
                                scales: chart.type === 'stacked' 
                                    ? { x: { stacked: true }, y: { stacked: true } }
                                    : commonOptions(true, chart.value_label).scales
                            } as any} 
                        />
                    </div>
                </div>
            );

        case 'scatter':
            return (
                <div className="flex flex-col h-full w-full">
                    {renderOutlierToggle()}
                    <div style={{ height: 192, width: '100%' }}>
                        <Scatter 
                            data={{
                                datasets: [{
                                    data: chartData.map((d: any) => ({ x: d.x, y: d.y })),
                                    backgroundColor: getPaletteColor(0)
                                }]
                            }} 
                            options={commonOptions(true, chart.y_axis || 'Y') as any} 
                        />
                    </div>
                </div>
            );
            
        case 'radar':
        case 'treemap':
            // Treemap/radar usually require specialized Chart.js plugins or adaptations.
            // Using a simple Bar fallback for Treemap when migrating to raw Chart.js
            return (
                <div className="flex flex-col h-full w-full">
                    {renderOutlierToggle()}
                    <div style={{ height: 192, width: '100%' }}>
                        <Bar 
                            data={{
                                labels: chartData.map((d: any) => d[nameKey] || d.name),
                                datasets: [{
                                    data: chartData.map((d: any) => d.value),
                                    backgroundColor: chartData.map((_: any, i: number) => getPaletteColor(i)),
                                }]
                            }} 
                            options={{
                                ...commonOptions(true, chart.value_label),
                                indexAxis: 'y'
                            } as any} 
                        />
                    </div>
                </div>
            );

        case 'geo_map':
            return (
                <div className="flex flex-col h-full w-full">
                    {renderOutlierToggle()}
                    <GeoMapCard data={chartData} mapType={chart.geo_meta?.map_type ?? 'world'} chartTitle={chart.title} formatType={chart.format_type} isDark={isDark} />
                </div>
            );

        default:
            return <div className="h-48 flex items-center justify-center text-themed-muted text-sm">Unsupported chart type</div>;
    }
};

// """
    
    final_content = content[:switch_start] + chartjs_switch + content[switch_end:]
    
    # Strip lingering Recharts imports if they missed the regex
    final_content = final_content.replace("import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,\n    AreaChart, Area, PieChart, Pie, Legend,\n    ScatterChart, Scatter, Cell,\n    RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';", "")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
migrate_user_dashboard()
