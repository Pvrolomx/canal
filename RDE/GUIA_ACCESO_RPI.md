# 🐝 GUÍA DE ACCESO AL RPi - Para Duendes Nuevos
## DATOS DE CONEXIÓN
| Campo | Valor |
|-------|-------|
| **IP** | `192.168.1.91` |
| **Usuario** | `pvrolo` |
| **Autenticación** | Key SSH (ver TOKENS.md) |
| **Puerto** | 22 (SSH) |

---

## MÉTODO: SSH via Git (Beach House)

El acceso al RPi usa autenticación por key SSH — no password en texto plano.
La key de Beach House ya está registrada en el RPi.

```powershell
$result = [System.Diagnostics.Process]::new()
$result.StartInfo.FileName = "C:\Program Files\Git\usr\bin\ssh.exe"
$result.StartInfo.Arguments = '-o StrictHostKeyChecking=no -o BatchMode=yes pvrolo@192.168.1.91 "echo CONECTADO"'
$result.StartInfo.RedirectStandardOutput = $true
$result.StartInfo.RedirectStandardError = $true
$result.StartInfo.UseShellExecute = $false
$result.Start() | Out-Null
$stdout = $result.StandardOutput.ReadToEnd()
$result.WaitForExit()
Write-Host $stdout
```

Si ves `CONECTADO`, estás dentro. Reemplaza `"echo CONECTADO"` con el comando que necesites.

### ⚠️ IMPORTANTE:
- Este método funciona desde **Beach House únicamente** — la key está registrada en esa máquina
- Desde otra máquina (Liberada, Cosota) la key no está registrada — no conectará
- Usar siempre PowerShell con `[System.Diagnostics.Process]` para capturar el output correctamente
- **Nunca usar password en texto plano en documentos del repo**

---

## UBICACIONES IMPORTANTES EN EL RPi
| Ruta | Descripción |
|------|-------------|
| `/home/pvrolo/` | Home del usuario |
| `/home/pvrolo/colmena/` | Archivos de La Colmena |
| `/home/pvrolo/repos/canal/` | Repo principal — scripts y RDE |
| `/home/pvrolo/repos/fantasma/` | Observatorio Fantasma |
| `/mnt/ssd/` | SSD externo (938GB) |

---

## VERIFICACIÓN RÁPIDA
Ejecuta el bloque de PowerShell arriba con `"echo CONECTADO"`.
Si responde `CONECTADO` — estás dentro. 🐝

---

**Creado:** Mayo 2026
**IP anterior:** 192.168.1.79 (ya no funciona)
**IP actual:** 192.168.1.91
**Método anterior:** plink + password (reemplazado por seguridad)
