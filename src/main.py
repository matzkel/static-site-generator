from textnode import TextNode


def main():
    a = TextNode("Hello, world!", "bold")
    b = TextNode("Google", "normal", "https://google.com")

    print(a)
    print(b)


if __name__ == "__main__":
    main()