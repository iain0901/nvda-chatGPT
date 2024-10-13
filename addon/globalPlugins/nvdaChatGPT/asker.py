from typing import List, Optional, TypedDict
import addonHandler
from . import (
	languages as languages,
	messenger as messenger,
	configManager as configManager,
)

from . import utils as utils
from . import instructions as instructions
from logHandler import log
from .temporary_path import temporary_sys_path


with temporary_sys_path():
	from openai import OpenAI


try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning(
		"Unable to initialise translations." "This may be because the addon is running from NVDA scratchpad."
	)


def createAskMeaningPrompt(word: str):
	outputLanguageIndex = configManager.getConfig("outputLanguageIndex")

	return languages.ASK_MEANING_PROMPT_MODELS[outputLanguageIndex].format(word)


class Message(TypedDict):
	role: str
	content: str


def createMessage(prompt: str, pastConvo: Optional[List[Message]] = None):
	messages = (
		[
			{
				"role": "system",
				"content": "You are a helpful assistant",
			},
		]
		if pastConvo is None
		else pastConvo
	)

	messages.append(
		{
			"role": "user",
			"content": prompt,
		},
	)

	return messages

def askChatGPT(prompt: str, conversation=None):
    # 從配置中獲取模型版本
    gptVersion = configManager.getConfig("gptVersionSentenceIndex")
    
    # 根據不同版本選擇不同的模型
    if gptVersion == 5:
        model = "gpt-4-32k"  # GPT-4-32k (o1)
    elif gptVersion == 4:
        model = "gpt-4"
    elif gptVersion == 3:
        model = "gpt-3.5-turbo"
    else:
        model = "gpt-3"

    messages = createMessage(prompt, conversation)

    client = OpenAI(api_key=configManager.getConfig("apiKey"))

    try:
        completion = client.chat.completions.create(
            model=model,  # 傳遞選擇的模型
            messages=messages,
        )

        response = completion.choices[0].message.content

    except Exception as e:
        if e.type == "invalid_request_error":
            messenger.emitUiBrowseableMessage(instructions.API_KEY_INCORRECT_ERROR)
        elif e.type == "insufficient_quota":
            messenger.emitUiBrowseableMessage(instructions.INSUFFICIENT_QUOTA_ERROR)
        else:
            unexpectedErrorMessage = _(
                "Unexpected error occured. Please send the error message below to the add-on "
                "author's email address, lcong5946@gmail.com \n\n "
            )
        messenger.emitUiBrowseableMessage(unexpectedErrorMessage + str(e))

        return

    messenger.emitUiBrowseableMessage(response)

    messages.append({"role": "assistant", "content": response})

    return messages
