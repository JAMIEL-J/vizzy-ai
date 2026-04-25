import re

def fix_syntax():
    user_dashboard_path = r"d:\Vizzy Redesign\Vizzy Redesign\frontend\src\pages\user\UserDashboard.tsx"
    with open(user_dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Revert back the commented out ThemedTooltip
    content = content.replace('// const ThemedTooltip = ({', 'const ThemedTooltip = ({')

    with open(user_dashboard_path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_syntax()
