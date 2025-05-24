# import streamlit as st
# from textwrap import dedent
# import dotenv

# from agno.agent import Agent
# from agno.models.openai import OpenAIChat
# from agno.tools.yfinance import YFinanceTools

# dotenv.load_dotenv()

# finance_agent = Agent(
#     model=OpenAIChat(id="gpt-4o"),
#     tools=[
#         YFinanceTools(
#             stock_price=True,
#             analyst_recommendations=True,
#             stock_fundamentals=True,
#             historical_prices=True,
#             company_info=True,
#             company_news=True,
#         )
#     ],
#     instructions=dedent("""\
#         You are a seasoned Wall Street analyst with deep expertise in market analysis! 📊

#         Follow these steps for comprehensive financial analysis:
#         1. Market Overview
#            - Latest stock price
#            - 52-week high and low
#         2. Financial Deep Dive
#            - Key metrics (P/E, Market Cap, EPS)
#         3. Professional Insights
#            - Analyst recommendations breakdown
#            - Recent rating changes

#         4. Market Context
#            - Industry trends and positioning
#            - Competitive analysis
#            - Market sentiment indicators

#         Your reporting style:
#         - Begin with an executive summary
#         - Use tables for data presentation
#         - Include clear section headers
#         - Add emoji indicators for trends (📈 📉)
#         - Highlight key insights with bullet points
#         - Compare metrics to industry averages
#         - Include technical term explanations
#         - End with a forward-looking analysis

#         Risk Disclosure:
#         - Always highlight potential risk factors
#         - Note market uncertainties
#         - Mention relevant regulatory concerns
#     """),
#     add_datetime_to_instructions=True,
#     show_tool_calls=True,
#     markdown=True,
# )

# def main():
#     st.title("🗞️ Finance Agent - Your Personal Market Analyst!")
#     st.markdown(
#         """
#         Enter your query about stocks, companies, or market analysis.
        
#         Examples:
#         - What's the latest news and financial performance of Apple (AAPL)?
#         - Give me a detailed analysis of Tesla's (TSLA) current market position
#         - How are Microsoft's (MSFT) financials looking? Include analyst recommendations
#         """
#     )
    
#     user_query = st.text_area("Ask your finance agent:", height=100)
    
#     if st.button("Analyze") and user_query.strip():
#         output_container = st.empty()
#         response_text = ""
#         started_output = False  # Flag to start output only after "Market Overview"

#         try:
#             chunks = finance_agent.run(user_query, stream=True)
#             for chunk in chunks:
#                 text_chunk = getattr(chunk, "text", None) or getattr(chunk, "content", None) or str(chunk)
                
#                 response_text += text_chunk
                
#                 # Start displaying only after "Market Overview" appears
#                 if not started_output:
#                     if "Market Overview" in response_text:
#                         started_output = True
#                         # Optionally trim the response_text to start exactly from "Market Overview"
#                         response_text = response_text[response_text.index("Market Overview") :]
#                     else:
#                         continue  # skip displaying until we get "Market Overview"
                
#                 output_container.markdown(response_text)

#         except Exception as e:
#             st.error(f"Error while fetching response: {e}")

# if __name__ == "__main__":
#     main()
import streamlit as st
from textwrap import dedent
import dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools

dotenv.load_dotenv()

# Agent 1: Quick Company Description
description_agent = Agent(
    model=OpenAIChat(id="gpt-4.1"),
    instructions=dedent("""\
        You are a knowledgeable financial researcher. Provide a concise and professional
        one-paragraph description of the company based on its stock ticker or name.
        Include key highlights such as business summary, industry, and core activities.
    """),
    add_datetime_to_instructions=True,
    markdown=True,
)

# Agent 2: Detailed Financial Analysis (unchanged)
finance_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            historical_prices=True,
            company_info=True,
            company_news=True,
        )
    ],
    instructions=dedent("""\
        You are a seasoned Wall Street analyst with deep expertise in market analysis! 📊

        Follow these steps for comprehensive financial analysis:
        1. Market Overview
           - Latest stock price
           - 52-week high and low
        2. Financial Deep Dive
           - Key metrics (P/E, Market Cap, EPS)
        3. Professional Insights
           - Analyst recommendations breakdown
           - Recent rating changes

        4. Market Context
           - Industry trends and positioning
           - Competitive analysis
           - Market sentiment indicators

        Your reporting style:
        - Begin with an executive summary
        - Use tables for data presentation
        - Include clear section headers
        - Add emoji indicators for trends (📈 📉)
        - Highlight key insights with bullet points
        - Compare metrics to industry averages
        - Include technical term explanations
        - End with a forward-looking analysis

        Risk Disclosure:
        - Always highlight potential risk factors
        - Note market uncertainties
        - Mention relevant regulatory concerns
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

def main():
    st.title("🗞️ Finance Agent - Your Personal Market Analyst!")
    st.markdown(
        """
        Enter your query about stocks, companies, or market analysis.

        Examples:
        - What's the latest news and financial performance of Apple (AAPL)?
        - Give me a detailed analysis of Tesla's (TSLA) current market position
        - How are Microsoft's (MSFT) financials looking? Include analyst recommendations
        """
    )

    user_query = st.text_area("Ask your finance agent:", height=100)

    if st.button("Analyze") and user_query.strip():
        # Two separate containers for output
        description_container = st.empty()
        analysis_container = st.empty()

        try:
            # Run first agent: Quick company description (no streaming)
            desc_response_obj = description_agent.run(user_query)
            desc_response = (
                getattr(desc_response_obj, "text", None)
                or getattr(desc_response_obj, "content", None)
                or str(desc_response_obj)
            )
            description_container.markdown("### 📝 Quick Company Description\n" + desc_response)

            analysis_container.markdown("---")  # visual separator

            # Run second agent: Detailed financial analysis (streaming)
            response_text = ""
            started_output = False

            chunks = finance_agent.run(user_query, stream=True)
            for chunk in chunks:
                text_chunk = getattr(chunk, "text", None) or getattr(chunk, "content", None) or str(chunk)
                response_text += text_chunk

                if not started_output:
                    if "Market Overview" in response_text:
                        started_output = True
                        response_text = response_text[response_text.index("Market Overview") :]
                    else:
                        continue

                analysis_container.markdown(response_text)

        except Exception as e:
            st.error(f"Error while fetching response: {e}")

if __name__ == "__main__":
    main()
