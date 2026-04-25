import re

def fix_duplicates():
    user_dashboard_path = r"d:\Vizzy Redesign\Vizzy Redesign\frontend\src\pages\user\UserDashboard.tsx"
    with open(user_dashboard_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # We will find the identical commonOptions function block and remove the second one.
    
    # Actually, we can just look for the second occurrence of `const commonOptions = `
    first_idx = -1
    second_idx = -1
    for i, line in enumerate(lines):
        if "const commonOptions =" in line:
            if first_idx == -1:
                first_idx = i
            else:
                second_idx = i
                break
                
    if second_idx != -1:
        # Find where the second one ends. Probably ends with '    });'
        end_idx = -1
        for i in range(second_idx+1, len(lines)):
            if lines[i].strip() == '});':
                end_idx = i
                break
        
        if end_idx != -1:
            del lines[second_idx:end_idx+1]
            
            with open(user_dashboard_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
                
fix_duplicates()
