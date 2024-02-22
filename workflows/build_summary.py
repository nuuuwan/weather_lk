from weather_lk import Summary
def main():
    s = Summary()
    s.write()
    s.write_by_place()



if __name__ == "__main__":
    main()