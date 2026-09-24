from main.llm import LocalLLM

def main() -> None:
    llm = LocalLLM()
    response = llm.generate(
        "Explain retrieval-augmented generation to me"
    )

    print(response)

if __name__ == "__main__":
    main()
