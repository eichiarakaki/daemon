import os

class Notificator:
    def __init__(self):
        self.app_name = "FTR Bot"

    def notify(self, script_name, env_name, script_args):
        title = "Daemon Notifier"
        message = (
            f"Running script: {script_name} in environment: {env_name} with arguments: {script_args}"
        )
        self._send_notify(title, message)


    def _send_notify(self, title, message):
        if os.name == 'nt':  # Windows
            command = f'powershell -command "Add-Type -AssemblyName System.Windows.Forms; ' \
                      f'$notify = New-Object System.Windows.Forms.NotifyIcon; ' \
                      f'$notify.Icon = [System.Drawing.SystemIcons]::Information; ' \
                      f'$notify.BalloonTipTitle = \'{title}\'; ' \
                      f'$notify.BalloonTipText = \'{message}\'; ' \
                      f'$notify.Visible = $true; ' \
                      f'$notify.ShowBalloonTip(10000)"'
            os.system(command)
        elif os.name == 'posix':  # macOS
            command = f'osascript -e \'display notification "{message}" with title "{title}"\''
            os.system(command)


