import os
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from dotenv import load_dotenv

load_dotenv()


def get_model() -> ChatOpenAI:
    """Get the chat model based on the environment variable."""
    # Initialize the chat model
    mode = os.environ.get("MODEL_MODE", "local")
    if mode == "local":
        llm = os.environ.get("LLM_MODEL_NAME")
        base_url = os.environ.get("LLM_BASE_URL")
        return ChatOpenAI(
            model_name=llm,
            openai_api_base=base_url,
            openai_api_key="",
        )
    elif mode == "remote":
        # API key in .env is mandatory
        return ChatOpenAI()
    else:
        raise ("MODEL_MODE environment variable should be local/remote")


def get_chatbot_with_history(llm: ChatOpenAI) -> RunnableWithMessageHistory:
    """
    Create a chat model with message history handling.
    This function sets up a chat model that can handle conversation history
    using a file-based chat message history.
    """
    # Create a prompt template
    prompt = ChatPromptTemplate(
        # Only content as input, history is handled separately
        input_variables=["content"],
        messages=[
            MessagesPlaceholder(
                variable_name="history"
            ),  # Placeholder for conversation history
            HumanMessagePromptTemplate.from_template("{content}"),
        ],
    )
    # Build the base chain (without memory)
    chain = prompt | llm

    # Create a single chat history instance
    chat_history = FileChatMessageHistory("messages.json")

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        """Return the chat history (ignoring session_id for simplicity)."""
        return chat_history

    # Wrap the chain with message history handling
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="content",
        history_messages_key="history",
    )


def start_chatbot():
    # Main conversation loop
    llm = get_model()
    chain_with_history = get_chatbot_with_history(llm)
    while True:
        content = input(">> ")

        # Exit condition
        if content.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Run the chain with automatic history management
        result = chain_with_history.invoke(
            {"content": content},
            config={
                "configurable": {"session_id": "default"}
            },  # Required by RunnableWithMessageHistory API
        )

        print(result.content)


if __name__ == "__main__":
    start_chatbot()
