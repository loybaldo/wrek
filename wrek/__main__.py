import subprocess
import typer
from rich import box
from rich.console import Console
from rich.table import Table


console = Console()
app = typer.Typer()

def getProfiles() -> list[str]:
    profiles: list[str] = []

    meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
    data = meta_data.decode('utf-8', errors ="backslashreplace")
    data = data.split('\n')

    for i in data:
        if "All User Profile" in i :
            i = i.split(":")
            i = i[1]
            i = i[1:-1]
            profiles.append(i)

    return profiles


def getMoreInfo(SSID: str, keyInfo: str) -> str:
    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', SSID, 'key=clear'])
    results = results.decode('utf-8', errors = "backslashreplace")
    results = results.split('\n')
    keyValue = [b.split(":")[1][1:-1] for b in results if keyInfo in b][0]

    return keyValue


@app.command(short_help = "Get all saved wifi passwords.")
def getall():
    profiles = getProfiles()

    table = Table(show_header = True, header_style = "blue", box = box.SQUARE_DOUBLE_HEAD)
    table.add_column("SSID Name")
    table.add_column("Security")
    table.add_column("Password")
    table.add_column("Authentication")
    table.add_column("Data Limit")
    table.add_column("Cipher")
    table.add_column("Vendor")

    for profile in profiles:
        security = getMoreInfo(profile, "Security key")
        password = getMoreInfo(profile, "Key Content")
        auth = getMoreInfo(profile, "Authentication")
        dataLimit = getMoreInfo(profile, "Over Data Limit")
        cipher = getMoreInfo(profile, "Cipher")
        vendor = getMoreInfo(profile, "Vendor extension")

        table.add_row(profile, security, password, auth, dataLimit, cipher, vendor)

    console.print(table)


if __name__ == "__main__":
    app()
