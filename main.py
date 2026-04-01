
from src.pipeline import FlowIQPipeline

if __name__ == "__main__":
    text = """
    Before starting, ensure the machine is powered off.
    Open the access panel.
    Remove the old filter.
    Install the new filter securely.
    Close the panel and restart the machine.
    """

    pipeline = FlowIQPipeline()
    result = pipeline.run(text)

    from pprint import pprint
    pprint(result)
