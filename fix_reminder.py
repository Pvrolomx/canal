with open('/home/pvrolo/duende_gist.py', 'r') as f:
    content = f.read()

old = '    # 3. Verificar recordatorio Cinthia\n    print("  Verificando recordatorio Cinthia...")\n    if check_cinthia_reminder(tokens):'
new = '    # 3. Verificar recordatorio Cinthia (DESACTIVADO)\n    # print("  Verificando recordatorio Cinthia...")\n    if False and check_cinthia_reminder(tokens):'

if old in content:
    content = content.replace(old, new)
    with open('/home/pvrolo/duende_gist.py', 'w') as f:
        f.write(content)
    print('OK - recordatorio Cinthia desactivado')
else:
    print('NOT FOUND')
