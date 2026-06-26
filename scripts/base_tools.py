import os
import json

from langchain.tools import tool
import ollama
import requests

# -------------------------
# MCP Config Loader
# -------------------------



# -------------------------
# Web Search Tool
# -------------------------
# @tool('live_web_search', description='Perform live search using Ollama.')
@tool
def web_search(query: str):
    """
    Perform a live web search using Ollama Cloud Web Search API for real-time information and news.

    Input:
        query: search query string

    Output:
        JSON string of top results (max_results=2).
    """

    response = ollama.web_search(query=query, max_results=2)
    response = response.results

    return response


# -------------------------
# Weather Tool
# -------------------------
@tool
def get_weather(location: str):
    """Get current weather for a location using WeatherAPI.com.
    
    Use for queries about weather, temperature, or conditions in any city.
    Examples: "weather in Paris", "temperature in Tokyo", "is it raining in London"
    
    Args:
        location: City name (e.g., "New York", "London", "Tokyo")
        
    Returns:
        Current weather information including temperature and conditions.
    """

    url = f"http://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHER_API_KEY')}&q={location}&aqi=no"

    response = requests.get(url=url, timeout=10)
    response.raise_for_status()

    data = response.json()

    return data


@tool
def calculator(a:int,b:int,operation:str):
    """Perform basic arithmetic operations.
    
    Use for queries that require mathematical calculations, such as "What is 2 + 2?" 
    
    Args:
        a: First number
        b: Second number
        operation: The arithmetic operation to perform ('add', 'subtract', 'multiply', 'divide')
        
    Returns:
        The result of the calculation.
    """
    if operation == 'add':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        if b != 0:
            return a / b
        else:
            return "Error: Division by zero is not allowed."
    else:
        return "Error: Unsupported operation. Please use add, subtract, multiply, or divide."
