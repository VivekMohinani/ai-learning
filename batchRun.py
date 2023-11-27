import sys
from model import runModeler
from data import genAndStoreData


# MAIN
def main():
    if len(sys.argv) != 3:
        print("No options selected, batchRun syntax included below.\n\n"
              "\033[1m\033[3m   `python3 batchRun.py <data entries - int> <modeling runs - int>`\033[0m\n"
              )
        return
    else:
        entries = int(sys.argv[1])
        runs = int(sys.argv[2])

        success = 0
        failure = 0
        for x in range(runs):
            text = f"Run: {x}"
            print("\n" + text.center(10, "~"))
            genAndStoreData(entries)
            if runModeler():
                success += 1
            else:
                failure += 1

        print(f"\n\033[32msuccesses: {success}\033[0m")
        print(f"\033[31mfailures: {failure}\033[0m")


if __name__ == "__main__":
    main()
