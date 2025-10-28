from src.scripts.agents import agent

if __name__ == "__main__":
    input_string = input("Write your prompt here: ")
    result = agent.run_sync(input_string)
    print(result.output)
