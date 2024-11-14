import subprocess
import time
import random

def run_command():
    # 定义你要执行的命令
    command = ["/www/wwwroot/Python-Project/Dingding/dingding_env/bin/python", "/www/wwwroot/Python-Project/Dingding/main.py"]
    
    try:
        # 使用 subprocess.run 执行命令
        result = subprocess.run(command, capture_output=True, text=True)
        # 输出命令执行的结果
        print("Command output:", result.stdout)
        if result.stderr:
            print("Command error:", result.stderr)
    except Exception as e:
        print(f"An error occurred while executing the command: {e}")

def main():
    while True:
        # 随机生成一个 1 到 5 分钟的时间间隔（以秒为单位）
        wait_time = random.randint(100, 600)
        print(f"Waiting for {wait_time // 60} minutes...")
        
        # 等待随机时间间隔
        time.sleep(wait_time)
        
        # 执行命令
        run_command()

if __name__ == "__main__":
    main()