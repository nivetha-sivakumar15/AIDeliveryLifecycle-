def load_inputs():
    with open("inputs/transcript.txt", "r") as f:
        transcript = f.read()

    with open("inputs/process.txt", "r") as f:
        process = f.read()

    return {
        "transcript": transcript,
        "process": process
    } 