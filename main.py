import schedule
import time
import subprocess
import logging


logging.basicConfig(filename='daemon.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def schedule_scripts():
    with open("./scripts.txt", "r") as file:
        scripts = file.readlines()
        print("Scripts loaded:", scripts)

    for script in scripts:
        script = script.strip()
        if script:
            script_name, interval, env_name = script.split(",")
            interval = int(interval.strip())
            env_name = env_name.strip()
            print(f"Scheduling {script_name} to run every {interval} hours in environment {env_name}")
            schedule.every(interval).hours.do(lambda: run_script(script_name, env_name))
            run_script(script_name, env_name)


def run_script(script_name, env_name):
    print(f"Running script: {script_name} in environment: {env_name}")
    try:
        if env_name.lower() == "none":
            subprocess.run(["python", script_name], check=True)
        else:
            activate_env = f"{env_name}\\Scripts\\activate.bat && python {script_name}"
            process = subprocess.Popen(["cmd.exe", "/c", activate_env], shell=True)
            process.communicate()

        message = f"Script {script_name} executed successfully."
        print(message)
        logging.info(message)
    except subprocess.CalledProcessError as e:
        message = f"Script {script_name} execution failed: {e}"
        print(message)
        logging.error(message)


if __name__ == "__main__":
    schedule_scripts()

    while True:
        schedule.run_pending()
        print('Checking for scheduled tasks...')
        time.sleep(120)
