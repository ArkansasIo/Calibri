import argparse
from src.agents import AgentOrchestrator

def main():
    parser = argparse.ArgumentParser(description="AetherForge multi-agent orchestrator")
    parser.add_argument("task", nargs="+")
    args = parser.parse_args()
    result = AgentOrchestrator().run(" ".join(args.task))
    print(result)

if __name__ == "__main__":
    main()
