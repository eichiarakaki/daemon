import schedule
import time
import subprocess
import logging
import json
from notifier import Notificator

logging.basicConfig(filename='daemon.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def schedule_scripts(notificator):
    with open("./scripts.json", "r") as file:
        data = json.load(file)
        scripts = data["scripts"]
        print("Scripts loaded:", scripts)

    for script in scripts:
        try:
            script_name = script['script_name']
            interval = script['interval']
            env_name = script['env_name']
            script_args = script.get('script_args', "")
            print(f"Scheduling {script_name} to run every {interval} hours in environment {env_name} with arguments {script_args}")
            schedule.every(interval).hours.do(run_script, script_name, env_name, script_args)
            run_script(script_name, env_name, script_args)
            notificator.notify(script_name, env_name, script_args)
        except KeyError as e:
            print(f"Error in the script configuration: {script} - Missing key: {e}")
            logging.error(f"Error in the script configuration: {script} - Missing key: {e}")

def run_script(script_name, env_name, script_args):
    print(f"Running script: {script_name} in environment: {env_name} with arguments: {script_args}")
    try:
        if env_name.lower() == "none":
            command = ["python", script_name] + script_args.split()
        else:
            activate_env = f'{env_name}\\Scripts\\activate.bat && python {script_name} {script_args}'
            command = ["cmd.exe", "/c", activate_env]

        process = subprocess.Popen(command, shell=True)
        process.communicate()

        message = f"Script {script_name} executed successfully."
        print(message)
        logging.info(message)
    except subprocess.CalledProcessError as e:
        message = f"Script {script_name} execution failed: {e}"
        print(message)
        logging.error(message)

if __name__ == "__main__":
    notificator = Notificator()
    schedule_scripts(notificator)

    while True:
        schedule.run_pending()
        print('Checking for scheduled tasks...')
        time.sleep(120)
