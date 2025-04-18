import time
from intercept import stop_mitmdump, start_mitmdump
from auto_hold import hold_folder, print_red


def main_auto():
    open("image_cache", "w").close()  # 清空缓存文件
    # 启动子进程
    mitmdump_process = start_mitmdump()  # 启动 mitmdump
    time.sleep(10)
    print("mitmdump 已启动，等待 10 秒......")
    try:
        open("image_cache", "w").close()  # 清空缓存文件

        print("开始运行主程序--\t hold_folder() ")
        print("-" * 60)
        time.sleep(3)
        hold_folder()  # 主进程
    except Exception as e:
        print_red(f"hold_folder() 函数运行时发生异常: {e}")
    finally:
        # 关闭子进程
        time.sleep(15)
        print("-" * 60)
        stop_mitmdump(mitmdump_process)  # 关闭 mitmdump
        print("关闭 mitmdump 子进程\t 主进程结束运行...")


if __name__ == "__main__":
    main_auto()
