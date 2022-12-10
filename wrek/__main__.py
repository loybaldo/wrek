import subprocess
import typer
from rich import box
from rich.console import Console
from rich.table import Table


console = Console()
app = typer.Typer()

@app.command(short_help = "Get all saved wifi passwords.")
def getall():
    meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
    data = meta_data.decode('utf-8', errors ="backslashreplace")
    data = data.split('\n')

    profiles = []
    
    for i in data:
        if "All User Profile" in i :
            i = i.split(":")
            i = i[1]
            i = i[1:-1]
            profiles.append(i)

    table = Table(show_header = True, header_style = "blue", box = box.SQUARE_DOUBLE_HEAD)
    table.add_column("Wi-Fi Name")
    table.add_column("Security")
    table.add_column("Password")
    table.add_column("Authentication")
    table.add_column("Data Limit")
    table.add_column("Cipher")
    table.add_column("Vendor")

    for i in profiles:
        try:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
            results = results.decode('utf-8', errors = "backslashreplace")
            results = results.split('\n')

            secKeys = [b.split(":")[1][1:-1] for b in results if "Security key" in b]
            passwords = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            authentications = [b.split(":")[1][1:-1] for b in results if "Authentication" in b]
            maxDataLimits = [b.split(":")[1][1:-1] for b in results if "Over Data Limit" in b]
            vendors = [b.split(":")[1][1:-1] for b in results if "Vendor extension" in b]
            ciphers = [b.split(":")[1][1:-1] for b in results if "Cipher" in b]

            table.add_row(i, secKeys[0], passwords[0], authentications[0], maxDataLimits[0], ciphers[0], vendors[0])

        except subprocess.CalledProcessError:
            print("Encoding Error Occurred")

    console.print(table)


if __name__ == "__main__":
    app()
