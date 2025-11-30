from textnode import TextNode, TextType

def main():
    node1 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    node2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    node3 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(f"Node 1: {node1}")
    print(f"Node 2: {node2}")
    print(f"Node 3: {node3}")
    print(f"Node 2 == Node 3: {node2==node3}")
    print(f"Node 1 == Node 3: {node1==node3}")


if __name__ == '__main__':
    main()