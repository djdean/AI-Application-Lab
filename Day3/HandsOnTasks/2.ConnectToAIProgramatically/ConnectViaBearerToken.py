from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main():
    #Go over the SDK and how to connect to AOAI programatically using the API. 
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )

    client = OpenAI(  
        base_url = "https://AIWorkshopTest.openai.azure.com/openai/v1/",  
        api_key=token_provider,
    )
    print("Done!\n\n")
    model = "gpt-5.2-chat"
    question = ""
    while True:
        question = input("\nEnter a question to ask "+model+ " or 'exit' to quit:\n")
        if question == "exit":
            exit(0)
        answer = answer_question(question,client,model)
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

