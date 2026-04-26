with open('/home/pvrolo/duende_gist.py', 'r') as f:
    content = f.read()

bad = """                    if not skip:
                    if line.strip().startswith("[ROLO:"):
                        continue
                    if line.strip().startswith("**Para:") or line.strip().startswith("**Asunto:"):
                        continue
                        body_lines.append(line)"""

good = """                    if not skip:
                        if line.strip().startswith("[ROLO:"):
                            continue
                        if line.strip().startswith("**Para:") or line.strip().startswith("**Asunto:"):
                            continue
                        body_lines.append(line)"""

if bad in content:
    content = content.replace(bad, good)
    with open('/home/pvrolo/duende_gist.py', 'w') as f:
        f.write(content)
    print('OK - indentacion corregida')
else:
    print('NOT FOUND - mostrando contexto:')
    idx = content.find('body_lines.append(line)')
    print(repr(content[idx-300:idx+50]))
