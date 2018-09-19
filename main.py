import data_fetcher
from custom_writers import stingy_writer
from data_writer import write_data
from custom_writers.caps_writer import write as caps_write

def main():
    print("Hello World")
    data = data_fetcher.fetch_data()
    write_data(data)
    caps_write("Oi, como vai você?")
    stingy_writer.write("Tem alguém ai?")

if __name__ == "__main__":
    main()
