"""Daily Weather Report."""


from weather_lk import Summary


def main():
    s = Summary()
    s.write()
    s.write_by_place()
    s.draw_charts_by_place()
    s.write_coverage()


if __name__ == "__main__":
    main()
