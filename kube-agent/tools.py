def termination_message(msg):
    """
    Checks if the message contains the termination string.

    :param msg: Message dictionary to check.
    :return: Boolean indicating if termination condition is met.
    """
    return msg.get("content") is not None and "TERMINATE" in msg["content"]
