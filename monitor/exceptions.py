class MaxRequestAttempts(Exception):
    def __init__(self, message=""):
        if not message:
            message = "Max request attempts reached."

        Exception.__init__(self, message)