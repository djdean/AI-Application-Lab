from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

def main():
    #Go over the SDK and how to connect to AOAI programatically using the API. 
    project = AIProjectClient(
        endpoint="https://AIWorkshopTest.services.ai.azure.com/api/projects/test-project",  # Replace with your endpoint
        credential=DefaultAzureCredential()
    )
    model = "gpt-5.2-chat"
    openai_client = project.get_openai_client()
    question = ""
    while True:
        question = input("\nEnter a question to ask "+model+ " or 'exit' to quit:\n")
        if question == "exit":
             exit(0)
        answer = answer_question(question,openai_client,model)
        print("Answer:\n\n"+answer["content"]+"\n\n")
def answer_question(question,client, model):
    response = client.responses.create(
        model=model,
        input="question: " + question,
    )
    result = {
        "content": response.output_text
    }
    return result
           
if __name__ == "__main__":
    main()

