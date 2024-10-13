import config

module = "askChatGPT"


# configManager.py

def initConfiguration():
    confspec = {
        "apiKey": "string( default='')",  # API 金鑰
        "outputLanguageIndex": "integer( default=3, min=0, max=15)",  # 語言選擇
        "gptVersionSentenceIndex": "integer( default=0, min=0, max=5)",  # 新增 GPT-4-32k 選項
        "dontShowCaution": "boolean( default=False)",
    }
    config.conf.spec[module] = confspec


def getConfig(key):
    value = config.conf[module][key]
    return value


def setConfig(key, value):
    config.conf[module][key] = value
