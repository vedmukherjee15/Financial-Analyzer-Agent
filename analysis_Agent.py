import os
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(root_dir)


from dotenv import load_dotenv

load_dotenv()


from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from scripts import base_tools,prompts,utils

from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

checkpointer = InMemorySaver()

model = ChatOpenAI(model='gpt-5.4-nano-2026-03-17')

async def get_tools():
    mcp_config = utils.load_mcp_config("google-sheets",'yahoo-finance')
    client = MultiServerMCPClient(mcp_config)

    mcp_tools = await client.get_tools()

    tools = mcp_tools + [base_tools.web_search, base_tools.get_weather]

    # Hide raw write tools for now. The model keeps generating mismatched
    # Google Sheets ranges for them, which causes consistent 400 errors.
    problematic_tools = ['update_cells', 'batch_update_cells']
    
    safe_tools = [tool for tool in tools if tool.name not in problematic_tools]

    print(len(safe_tools))
    print([tool.name for tool in safe_tools])

    return safe_tools


async def sheet_agent(query,thread_id='default'):

    tools = await get_tools()

    System_Message = prompts.GOOGLE_SHEETS_PROMPT

    config = {"configurable" : {"thread_id": thread_id}}

    agent = create_agent(
        model=model,
        tools=tools,
        checkpointer=checkpointer,
        system_prompt=System_Message
    )

    response = await agent.ainvoke({"messages": [HumanMessage(content=query)]}, config)

    result = response["messages"][-1].text

    print(result)

async def ask():
    print("Chat mode entered. Press 'q' or 'quit' to exit")

    while True:
        query = input("You: ").strip()

        if query.lower() in ['q','quit']:
            print("Exiting conversation")
            break


        await sheet_agent(query)


if __name__ == '__main__':
    asyncio.run(ask())

    





