from app.services.llm import get_llm


def test_llm():

    llm = get_llm()

    response = llm.invoke(
        "Explain in one sentence what a recruiter does."
    )

    print("\nGemini via LangChain:")
    print(response.content)

    assert response.content