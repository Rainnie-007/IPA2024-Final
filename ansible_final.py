import subprocess

def showrun(student_id, router_name):
    command = ['ansible-playbook', '/home/devasc/Desktop/Final/final193/IPA2024-Final/playbook.yaml']
    result = subprocess.run(command, capture_output=True, text=True)
    
    
    print("Standard Output:\n", result.stdout)
    print("Standard Error:\n", result.stderr)
    
    
    if result.returncode == 0:  # Ansible success returns 0
        return f'show_run_{student_id}_{router_name}.txt'
    else:
        return 'Error: Ansible'

student_id = '65070193'
router_name = 'IPA2024-Pod1-4'
output_file = showrun(student_id, router_name)
print(output_file)