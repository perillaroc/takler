import takler


def main():
    client = takler.Client()
    client.queue("/suite1")
    

if __name__ == "__main__":
    main()
