# This file is for create a thread and limit the total threads to 1.
import threading
from . import messenger as messenger


threadObj = None
THREAD_NAME = "askChatGPT"


def isProcessingOtherQuestion() -> bool:
	for th in threading.enumerate():
		if th.name == "askChatGPT":
			messenger.emitUiMessage("You are already asking something, wait for the response first")

			return True
	return False


def start_thread(
	target,
	startMessage: str,
	args: tuple = (),
	kwargs: dict = {},
):
	if isProcessingOtherQuestion():
		return

	messenger.emitUiMessage(startMessage)

	global threadObj

	threadObj = threading.Thread(target=target, args=args, kwargs=kwargs, name=THREAD_NAME)

	threadObj.start()
